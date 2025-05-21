from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.OS import OS
from src.services.analise import create_OS
import pandas as pd
from datetime import datetime

router = APIRouter(prefix="/OS")

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
       await db.close()

@router.get("/newOS")
async def list_bets(id: int,solicitante: str,data:str,servico:str,valor: int,status:str, numserie: int,db:Session = Depends(get_db)):
    id=id,
    solicitante=solicitante,
    data=data,
    servico=servico,
    valor=valor,
    status=status,
    numserie=numserie
    new_OS= await create_OS(db,id,solicitante,data,servico,valor,status,numserie)
    return {
        "id": new_OS.id,
        "solicitante":new_OS.solicitante,
        "data":new_OS.data,
        "servico":new_OS.servico,
        "valor":new_OS.valor,
        "status":new_OS.status,
        "numserie":new_OS.numserie
    }

@router.get("/analise")
async def analise_tendencia(db:Session = Depends(get_db)):
# realisação da analise de tendencia de OS
    
    result = await db.execute(select(OS))
    ordens = result.scalars().all()

    # Transformar os dados em uma lista de dicionários
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

    if not os_data:
        return {"mensagem": "Nenhuma OS encontrada para análise."}

    # Criar DataFrame
    df = pd.DataFrame(os_data)

    # Converter data para datetime se necessário
    df["data"] = pd.to_datetime(df["data"])

    # Criar coluna com ano-mês
    df["mes"] = df["data"].dt.to_period("M").astype(str)

    # Agrupar por mês: contar OS e somar valores
    tendencia = df.groupby("mes").agg(qtd_OS=("id", "count"), total_valor=("valor", "sum")).reset_index()

    # Converter para dicionário (JSON serializável)
    tendencia_dict = tendencia.to_dict(orient="records")

    return {"tendencia_OS": tendencia_dict}