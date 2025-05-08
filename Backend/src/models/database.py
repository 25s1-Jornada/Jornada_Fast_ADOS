import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # declarative_base

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Criar a engine assíncrona do SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Criar a sessão assíncrona
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, 
    autocommit=False, 
    autoflush=False
)

# Base para os modelos do SQLAlchemy
Base = declarative_base()

from src.models.OS import OS

# Função para criar as tabelas no banco de dados ao iniciar a aplicação
async def init_db():
    async with engine.begin() as conn:
        print("criando tabelas")
        await conn.run_sync(Base.metadata.create_all)
        print("tabelas criadas")
