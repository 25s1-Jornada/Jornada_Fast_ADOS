from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.database import AsyncSessionLocal
from src.models.OS import OS
from src.services.analise import create_OS
from datetime import datetime
import pandas as pd
from io import StringIO

router = APIRouter(prefix="/OS")

# Dependency para obter a sessão do banco assíncrona
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/newOS")
async def create_os_endpoint(
    id: int,
    solicitante: str,
    data: str,
    servico: str,
    valor: int,
    status: str,
    numserie: str,
    db: AsyncSession = Depends(get_db)
):
    new_os = await create_OS(id, solicitante, data, servico, valor, status, numserie, db)
    return {
        "id": new_os.id,
        "solicitante": new_os.solicitante,
        "data": new_os.data,
        "servico": new_os.servico,
        "valor": new_os.valor,
        "status": new_os.status,
        "numserie": new_os.numserie
    }

@router.get("/analise")
async def analise_tendencia(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OS))
    ordens = result.scalars().all()

    if not ordens:
        return {"mensagem": "Nenhuma OS encontrada para análise."}

    os_data = [
        {
            "id": os.id,
            "solicitante": os.solicitante,
            "data": os.data,
            "servico": os.servico,
            "valor": os.valor,
            "status": os.status,
            "numserie": os.numserie
        }
        for os in ordens
    ]

    df = pd.DataFrame(os_data)
    df["data"] = pd.to_datetime(df["data"])
    df["mes"] = df["data"].dt.to_period("M").astype(str)
    tendencia = df.groupby("mes").agg(qtd_OS=("id", "count"), total_valor=("valor", "sum")).reset_index()

    return {"tendencia_OS": tendencia.to_dict(orient="records")}

@router.post("/upload_csv")
async def upload_os_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um CSV.")

    try:
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode("utf-8")))

        required_columns = {"solicitante", "data", "servico", "valor", "status", "numserie"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail=f"CSV deve conter as colunas: {required_columns}")

        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df = df.dropna(subset=["data"])

        for _, row in df.iterrows():
            os = OS(
                solicitante=row["solicitante"],
                data=row["data"].date(),
                servico=row["servico"],
                valor=row["valor"],
                status=row["status"],
                numserie=row["numserie"]
            )
            db.add(os)

        await db.commit()
        return {"message": f"{len(df)} ordens de serviço inseridas com sucesso."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
