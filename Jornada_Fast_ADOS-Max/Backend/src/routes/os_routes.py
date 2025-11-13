from fastapi import APIRouter, Query
from typing import Optional
from src.services import os_service

router = APIRouter(prefix="/os", tags=["Ordens de Serviço"])

@router.get("/resumo-geral")
def get_resumo_geral():
    return os_service.resumo_geral()

@router.get("/total-por-periodo")
def get_total_por_periodo():
    return os_service.total_os_por_periodo()

@router.get("/principais-causas")
def get_principais_causas():
    return os_service.principais_causas()

@router.get("/por-tecnico")
def get_os_por_tecnico():
    return os_service.os_por_tecnico()

@router.get("/filtrar")
def filtrar_os(
    tecnico: Optional[str] = Query(None),
    departamento: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    conclusao: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    filtros = {
        "tecnico": tecnico,
        "departamento": departamento,
        "area": area,
        "conclusao": conclusao,
        "status": status,
    }
    return os_service.os_filtrados(filtros)
