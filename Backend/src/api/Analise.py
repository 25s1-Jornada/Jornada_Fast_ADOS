from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.OS import OS


router = APIRouter(prefix="/OS")

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
       await db.close()

@router.get("/bets")
async def list_bets(AsyncSession = Depends(get_db)):
    return [1]