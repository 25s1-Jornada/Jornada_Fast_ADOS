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
    ano: int = Query(..., ge=2000, le=2100), 
    mes: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(OS))
    ordens = result.scalars().all()

    if not ordens:
        raise HTTPException(status_code=404, detail="Nenhuma ordem encontrada.")

    # Extrair dados
    data = []
    for os in ordens:
        data.append({
            "data_emissao_nf": os.data_emissao_nf,
            "dt_fabricacao": os.data_fabricacao,
            "causa": os.causa,
            "item": os.item,
        })

    df = pd.DataFrame(data)
    df["data_emissao_nf"] = pd.to_datetime(df["data_emissao_nf"], errors="coerce")
    df = df.dropna(subset=["data_emissao_nf"])
    
    # Criar coluna "mes" para análise temporal
    df["mes"] = df["data_emissao_nf"].dt.to_period("M").astype(str)

    # Filtro por ano e mês
    df_mes = df[
        (df["data_emissao_nf"].dt.year == ano) & 
        (df["data_emissao_nf"].dt.month == mes)
    ]

    if df_mes.empty:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado para o ano e mês fornecidos.")

    # Estatísticas
    qtd_por_mes = df_mes.groupby("mes").size().to_dict()
    causa_mais_comum = Counter(df_mes["causa"].dropna()).most_common()
    item_mais_comum = Counter(df_mes["item"].dropna()).most_common()

    # Tendência de falhas por item ao longo do tempo
    forecast = {}
    df_forecast = df.dropna(subset=["mes", "item"])

    for item, grupo in df_forecast.groupby("item"):
        contagem = grupo.groupby("mes").size().sort_index()
        if len(contagem) >= 3:
            X = np.arange(len(contagem)).reshape(-1, 1)
            y = contagem.values
            model = LinearRegression().fit(X, y)
            predicted = model.predict(np.array([[len(contagem)]]))[0]
            if predicted >= 1:
                forecast[item] = round(predicted)

    return {
        "quantidade_por_mes": qtd_por_mes,
        "causas_mais_comuns": causa_mais_comum,
        "itens_mais_comuns": item_mais_comum,
        "previsao_itens_em_risco": forecast
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
