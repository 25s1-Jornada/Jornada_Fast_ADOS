from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.database import AsyncSessionLocal
from src.models.OS import OS
from src.services.analise import create_OS
from datetime import datetime, date
import pandas as pd
from io import StringIO
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

@router.get("/analise")
async def analise_tendencia(
    ano: int = Query(..., ge=2000, le=2100), 
    mes: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(OS))
    ordens = result.scalars().all()

    if not ordens:
        raise HTTPException(status_code=404, detail="Nenhuma ordem de serviço encontrada.")

    # Extrai os dados para DataFrame
    data = []
    for os in ordens:
        data.append({
            "data_primeira_visita": os.data_primeira_visita,
            "valor_total": os.valor_total,
            "categoria_defeito": os.categoria_defeito,
            "peca_defeito": os.peca_defeito,
            "cod_peca_defeito": os.cod_peca_defeito,
        })

    df = pd.DataFrame(data)
    df["data_primeira_visita"] = pd.to_datetime(df["data_primeira_visita"], errors="coerce")
    df = df.dropna(subset=["data_primeira_visita"])

    # 🔍 Filtro por ano e mês
    df = df[(df["data_primeira_visita"].dt.year == ano) & (df["data_primeira_visita"].dt.month == mes)]

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhuma ordem de serviço encontrada para o ano e mês fornecidos.")

    df["mes"] = df["data_primeira_visita"].dt.to_period("M").astype(str)

    # Tendência de quantidade por mês
    qtd_por_mes = df.groupby("mes").size().to_dict()

    # Tendência de valor total por mês
    valor_total_mes = df.groupby("mes")["valor_total"].sum().to_dict()

    # Categorias de defeito mais comuns
    categoria_defeitos_mais_comuns = Counter(df["categoria_defeito"].dropna()).most_common()

    # Peças com maior ocorrência de defeitos
    pecas_defeito_mais_comuns = Counter(df["peca_defeito"].dropna()).most_common()

    # 🔮 Previsão de peças que podem estragar
    df_peça_mes = df.dropna(subset=["mes", "peca_defeito"])
    forecast = {}

    for peca, grupo in df_peça_mes.groupby("peca_defeito"):
        contagem_mes = grupo.groupby("mes").size().sort_index()
        if len(contagem_mes) >= 3:
            X = np.arange(len(contagem_mes)).reshape(-1, 1)
            y = contagem_mes.values
            model = LinearRegression().fit(X, y)
            next_month = np.array([[len(contagem_mes)]])
            predicted = model.predict(next_month)[0]
            if predicted >= 1:
                forecast[peca] = round(predicted)

    return {
        "quantidade_por_mes": qtd_por_mes,
        "valor_total_por_mes": valor_total_mes,
        "categoria_defeitos_mais_comuns": categoria_defeitos_mais_comuns,
        "pecas_defeito_mais_comuns": pecas_defeito_mais_comuns,
        "previsao_pecas_com_risco": forecast
    }

@router.post("/upload_csv")
async def upload_os_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um CSV.")

    try:
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode("utf-8")), sep=",")
        df.columns = df.columns.str.strip().str.lower()

        required_columns = {
            "cod cliente", "cod tecnico", "cod vendedor", "n serie", "categoria chamado",
            "observacao chamado", "custo deslocamento", "custo hr", "custo km",
            "data primeira visita", "data segunda visita", "despesa materiais",
            "qtd materiais", "custo materiais", "valor total", "categoria defeito",
            "peca defeito", "cod peca defeito", "cod peca nova"
        }

        if not required_columns.issubset(df.columns):
            raise HTTPException(
                status_code=400,
                detail=f"CSV deve conter as colunas: {required_columns}"
            )

        erros = []
        for i, row in df.iterrows():
            try:
                os = OS(
#                    id=int(row["id"]),
                    cod_cliente=str(row["cod cliente"]),
                    cod_tecnico=str(row["cod tecnico"]),
                    cod_vendedor=str(row["cod vendedor"]),
                    numserie=str(row["n serie"]),
                    categoria_chamado=str(row["categoria chamado"]),
                    observacao_chamado=str(row["observacao chamado"]),
                    custo_deslocamento=float(row["custo deslocamento"]),
                    custo_hr=float(row["custo hr"]),
                    custo_km=float(row["custo km"]),
                    data_primeira_visita=datetime.strptime(str(row["data primeira visita"]), "%Y-%m-%d").date(),
                    data_segunda_visita=datetime.strptime(str(row["data segunda visita"]), "%Y-%m-%d").date(),
                    despesa_materiais=float(row["despesa materiais"]),
                    qtd_materiais=int(row["qtd materiais"]),
                    custo_materiais=float(row["custo materiais"]),
                    valor_total=float(row["valor total"]),
                    categoria_defeito=str(row["categoria defeito"]),
                    peca_defeito=str(row["peca defeito"]),
                    cod_peca_defeito=str(row["cod peca defeito"]),
                    cod_peca_nova=str(row["cod peca nova"])
                )
                db.add(os)

            except Exception as e:
                traceback.print_exc()
                erros.append({"linha": i + 1, "erro": str(e)})

        try:
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Erro de integridade ao salvar no banco. Verifique duplicatas ou chaves únicas.")

        if erros:
            return {
                "message": f"{len(df) - len(erros)} OS inseridas com sucesso.",
                "erros": erros
            }

        return {"message": f"{len(df)} OS inseridas com sucesso."}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro interno ao processar o arquivo CSV.")
