# tests/conftest.py

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models.database import Base # Importa a Base do seu modelo ORM
import asyncio

# --- CONFIGURAÇÃO DO BANCO DE DADOS DE TESTE ---
# Você tem duas opções populares para o banco de dados de teste:

# OPÇÃO 1: SQLite em memória (muito rápido, não precisa de Docker)
# Ideal para testes unitários/integração que só precisam de um DB simples.
# TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# OPÇÃO 2: PostgreSQL no Docker (mais fiel ao ambiente de produção)
# Se você quer testar a integração com um PostgreSQL real, use esta URL.
# Certifique-se de que seu contêiner PostgreSQL Docker esteja rodando na porta 5432.
TEST_DATABASE_URL = "postgresql+asyncpg://admin:senha123@localhost:5432/Fast_ADOS"
# Se você criou um banco de dados de teste separado no Docker, use o nome dele:
# TEST_DATABASE_URL = "postgresql+asyncpg://admin:senha123@localhost:5432/Fast_ADOS_TEST"


# Cria o motor de banco de dados para os testes
engine = create_async_engine(TEST_DATABASE_URL, echo=False)

# Cria uma classe de sessão para os testes
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --- FIXTURE DE SESSÃO DO BANCO DE DADOS ---
# Esta fixture será usada por todos os seus testes que precisam de uma sessão de DB.
@pytest.fixture(name="session")
async def session_fixture():
    # Antes de cada teste, dropa todas as tabelas e as recria.
    # Isso garante um estado limpo para cada teste.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Fornece uma nova sessão de banco de dados para o teste.
    async with TestingSessionLocal() as session:
        yield session # O controle é passado para o teste

    # Após o teste, dropa as tabelas novamente para garantir a limpeza (opcional, mas seguro).
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# --- FIXTURE DE EVENT LOOP PARA TESTES ASYNC ---
# Necessário para algumas configurações antigas do pytest-asyncio,
# ou se você precisar de controle explícito sobre o loop de eventos.
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()