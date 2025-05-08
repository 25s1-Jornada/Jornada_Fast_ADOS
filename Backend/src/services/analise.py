from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.models.OS import OS

async def create_OS(db: Session, id: int,solicitante: str,data:str,servico:str,valor: int,status:str, numserie: int):

    new_OS =  OS(id=id,solicitante=solicitante,data=data,servico=servico,valor=valor,status=status,numserie=numserie)
    db.add(new_OS)
    await db.commit()
    await db.refresh(new_OS)
    return new_OS