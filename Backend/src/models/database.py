import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # declarative_base

load_dotenv() # Garanta que suas variáveis de ambiente estão sendo carregadas, se usadas

DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "senha123")
DB_HOST = os.getenv("DB_HOST", "db") # <-- ESTE É O PONTO CHAVE: 'db'
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "Fast_ADOS") # <-- ESTE É O NOME DO SEU DB

#DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DATABASE_URL = f"postgresql+asyncpg://admin:senha123@localhost:5432/Fast_ADOS"


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
