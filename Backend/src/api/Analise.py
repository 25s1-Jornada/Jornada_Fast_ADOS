from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.database import AsyncSessionLocal
from src.models.OS import OS
from datetime import datetime
import pandas as pd
from io import BytesIO 
import traceback
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/OS")

# Dependency para obter a sessão do banco assíncrona
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/analise")
async def analise_tendencia(
    ano:int,
    mes:int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(OS))
    ordens = result.scalars().all()

    if not ordens:
        raise HTTPException(status_code=404, detail="Nenhuma ordem encontrada.")

    # Transformar em DataFrame
    data = [{
        "data_emissao_nf": os.data_emissao_nf,
        "estado": os.estado,
        "cidade": os.cidade,
        "tipo": os.tipo,
        "causa": os.causa,
        "nome_cliente": os.nome_cliente
    } for os in ordens]

    df = pd.DataFrame(data)
    df["data_emissao_nf"] = pd.to_datetime(df["data_emissao_nf"], errors="coerce")
    df = df.dropna(subset=["data_emissao_nf"])

    # Filtro por ano se necessário
    df = df[df["data_emissao_nf"].dt.year == ano]

    # 1. Análise semanal de OSs por localidade
    total_os = len(df)
    estados = df["estado"].value_counts(normalize=True).mul(100).round(1).to_dict()
    cidades = (df["cidade"] + "/" + df["estado"]).value_counts().head(5).index.tolist()

    # 2. Sazonalidade
    df["mes"] = df["data_emissao_nf"].dt.month
    meses_quentes = df[df["mes"].isin([10, 11, 12, 1, 2, 3])]
    sazonalidade_pct = round(len(meses_quentes) / total_os * 100, 1) if total_os else 0
    pico_nov_dez = df[df["mes"].isin([11, 12])]
    media_geral = df.groupby("mes").size().mean()
    media_nov_dez = pico_nov_dez.groupby("mes").size().mean()
    aumento_pct = round(((media_nov_dez - media_geral) / media_geral) * 100, 1) if media_geral else 0

    # 3. Análise de status das OSs (usando "tipo")
    tipo_pct = df["tipo"].value_counts(normalize=True).mul(100).round(0).to_dict()

    # Tempo médio simulado
    tempo_medio = {
        "Garantia": "3,2 dias",
        "Fora da garantia": "5,7 dias",
        "Estrutura": "4,1 dias",
        "Refrigeração": "3,8 dias"
    }

    # Principais causas
    causas = df["causa"].value_counts(normalize=True).mul(100).round(0).to_dict()
    principais_causas = dict(list(causas.items())[:4])

    # 4. Clientes com maior prioridade (simulado)
    clientes_prioridade = {
        "Atacadão S/A": "18%",
        "A. Angeloni & Cia": "12%",
        "Ancora Distribuidora": "10%",
        "Armazém do Grão": "7%"
    }

    # 5. Contagem mensal de O.S para gráfico
    contagem_mensal = df.groupby(df["data_emissao_nf"].dt.month).size().to_dict()
    meses_nomes = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    contagem_mensal_formatada = {meses_nomes[k]: v for k, v in contagem_mensal.items()}

    # Retorno final
    return {
        "  Análise semanal de OSs por localidade": {
            "Distribuição geográfica": {
                estado: f"{pct}% das OSs" for estado, pct in estados.items()
            },
            "Principais cidades com mais OSs": cidades
        },
        "   Sazonalidade": {
            "Maior volume em meses quentes": f"{sazonalidade_pct}%",
            "Pico em nov/dez": f"{aumento_pct}% de aumento na média"
        },
        "    Análise de status das OSs": {
            "Distribuição": tipo_pct,
            "Tempo médio de resolução": tempo_medio,
            "Principais causas": principais_causas
        },
        " Análise por prioridade": {
            "Clientes que demandam maior atenção": clientes_prioridade
        },
        "Total O.S por mês": contagem_mensal_formatada
    }




@router.post("/upload_xlsx")
async def upload_os_xlsx(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um XLSX.")

    try:
        content = await file.read()
        df = pd.read_excel(BytesIO(content))
        df.columns = df.columns.str.strip().str.lower()

        required_columns = {
            "nrchamado", "codcliente", "nomecliente", "cidade", "estado",
            "nrserie", "item", "dtfabricacao", "dtemissão nf", "tipo", "causa", "observacao"
        }

        if not required_columns.issubset(df.columns):
            raise HTTPException(
                status_code=400,
                detail=f"XLSX deve conter as colunas: {required_columns}"
            )

        erros = []
        for i, row in df.iterrows():
            try:
                os = OS(
                    numero_chamado=str(row["nrchamado"]),
                    cod_cliente=str(row["codcliente"]),
                    nome_cliente=str(row["nomecliente"]),
                    cidade=str(row["cidade"]),
                    estado=str(row["estado"]),
                    numserie=str(row["nrserie"]),
                    item=str(row["item"]),
                    data_fabricacao=pd.to_datetime(row["dtfabricacao"]).date() if not pd.isna(row["dtfabricacao"]) else None,
                    data_emissao_nf=pd.to_datetime(row["dtemissão nf"]).date() if not pd.isna(row["dtemissão nf"]) else None,
                    tipo=str(row["tipo"]),
                    causa=str(row["causa"]),
                    observacao=str(row["observacao"])
                )
                db.add(os)

            except Exception as e:
                traceback.print_exc()
                erros.append({"linha": i + 1, "erro": str(e)})

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Erro de integridade ao salvar no banco.")

        if erros:
            return {
                "message": f"{len(df) - len(erros)} registros inseridos com sucesso.",
                "erros": erros
            }

        return {"message": f"{len(df)} registros inseridos com sucesso."}

    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro interno ao processar o arquivo XLSX.")
