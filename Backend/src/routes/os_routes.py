from fastapi import APIRouter
from src.services import os_service

router = APIRouter(prefix="/os", tags=["Ordens de Serviço"])

@router.get("/")
def listar_os():
    """
    Lista as ordens de serviço registradas no Neo4j.
    """
    return os_service.listar_os()

@router.post("/")
def criar_os(dados: dict):
    """
    Cria uma nova ordem de serviço no Neo4j.
    """
    return os_service.criar_os(dados)

@router.get("/cidade/{cidade}")
def buscar_por_cidade(cidade: str):
    """
    Busca ordens de serviço por cidade.
    """
    return os_service.buscar_os_por_cidade(cidade)
