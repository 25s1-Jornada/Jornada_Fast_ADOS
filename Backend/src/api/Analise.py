from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.OS import OS
from src.services.analise import create_OS


router = APIRouter(prefix="/OS")

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
       await db.close()

@router.get("/Analise")
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
