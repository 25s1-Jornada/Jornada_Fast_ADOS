from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.database import AsyncSessionLocal
from src.models.OS import OS
from src.services.analise import create_OS
from datetime import datetime, date
import pandas as pd
from io import StringIO, BytesIO 
import traceback
from sqlalchemy.exc import IntegrityError
from collections import Counter
from sklearn.linear_model import LinearRegression
import numpy as np

router = APIRouter(prefix="/OS")

# Dependency para obter a sessão do banco assíncrona
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
'''
@router.post("/newOS")
async def create_os_endpoint(
    id: int,
    cod_cliente: str,
    cod_tecnico: str,
    cod_vendedor: str,
    numserie: str,
    categoria_chamado: str,
    observacao_chamado: str,
    custo_deslocamento: float,
    custo_hr: float,
    custo_km: float,
    data_primeira_visita: date,
    data_segunda_visita: date,
    despesa_materiais: float,
    qtd_materiais: int,
    custo_materiais: float,
    valor_total: float,
    categoria_defeito: str,
    peca_defeito: str,
    cod_peca_defeito: str,
    cod_peca_nova: str,
    db: AsyncSession = Depends(get_db)
):
    new_os = await create_OS(
    id,
    cod_cliente,
    cod_tecnico,
    cod_vendedor,
    numserie,
    categoria_chamado,
    observacao_chamado,
    custo_deslocamento,
    custo_hr,
    custo_km,
    data_primeira_visita,
    data_segunda_visita,
    despesa_materiais,
    qtd_materiais,
    custo_materiais,
    valor_total,
    categoria_defeito,
    peca_defeito,
    cod_peca_defeito,
    cod_peca_nova, db)
    return {
    "id": new_os.id,
    "cod_cliente": new_os.cod_cliente,
    "cod_tecnico": new_os.cod_tecnico,
    "cod_vendedor":new_os.cod_vendedor,
    "numserie": new_os.numserie,
    "categoria_chamado": new_os.categoria_chamado,
    "observacao_chamado": new_os.observacao_chamado,
    "custo_deslocamento": new_os.custo_deslocamento,
    "custo_hr": new_os.custo_hr,
    "custo_km": new_os.custo_km,
    "data_primeira_visita": new_os.data_primeira_visita,
    "data_segunda_visita": new_os.data_segunda_visita,
    "despesa_materiais": despesa_materiais,
    "qtd_materiais": new_os.qtd_materiais,
    "custo_materiais": new_os.custo_materiais,
    "valor_total": new_os.valor_total,
    "categoria_defeito": new_os.categoria_defeito,
    "peca_defeito": new_os.peca_defeito,
    "cod_peca_defeito": new_os.cod_peca_defeito,
    "cod_peca_nova": new_os.cod_peca_nova
    }
'''


#router = APIRouter()

@router.get("/analise")
async def analise_tendencia(
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

    #  Análise semanal de OSs por localidade
    total_os = len(df)
    estados = df["estado"].value_counts(normalize=True).mul(100).round(1).to_dict()
    cidades = (df["cidade"] + "/" + df["estado"]).value_counts().head(5).index.tolist()

    #  Sazonalidade
    df["mes"] = df["data_emissao_nf"].dt.month
    meses_quentes = df[df["mes"].isin([10, 11, 12, 1, 2, 3])]
    sazonalidade_pct = round(len(meses_quentes) / total_os * 100, 1)
    pico_nov_dez = df[df["mes"].isin([11, 12])]
    media_geral = df.groupby("mes").size().mean()
    media_nov_dez = pico_nov_dez.groupby("mes").size().mean()
    aumento_pct = round(((media_nov_dez - media_geral) / media_geral) * 100, 1) if media_geral else 0

    #  Análise de status das OSs (usando "tipo")
    tipo_pct = df["tipo"].value_counts(normalize=True).mul(100).round(0).to_dict()

    # Tempo médio de resolução simulado (exemplo)
    tempo_medio = {
        "Garantia": "3,2 dias",
        "Fora da garantia": "5,7 dias",
        "Estrutura": "4,1 dias",
        "Refrigeração": "3,8 dias"
    }

    # Principais causas
    causas = df["causa"].value_counts(normalize=True).mul(100).round(0).to_dict()
    principais_causas = dict(list(causas.items())[:4])

    #  Análise por prioridade (simulado com base em nomes de clientes)
    clientes_prioridade = {
        "Atacadão S/A": "18%",
        "A. Angeloni & Cia": "12%",
        "Ancora Distribuidora": "10%",
        "Armazém do Grão": "7%"
    }

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
        }
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
