from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.models.OS import OS
from datetime import date

async def create_OS(
    id: int,
    cod_cliente: str,
    cod_tecnico: str,
    cod_vendedor: str,
    numserie: str,
    categoria_chamado: str,
    observacao_chamado: str,
    custo_deslocamento: float,
    custo_hr: float,
    custo_km: float,
    data_primeira_visita: date,
    data_segunda_visita: date,
    despesa_materiais: float,
    qtd_materiais: int,
    custo_materiais: float,
    valor_total: float,
    categoria_defeito: str,
    peca_defeito: str,
    cod_peca_defeito: str,
    cod_peca_nova: str,
    db: AsyncSession
):
    new_os = OS(
        id=id,
        cod_cliente=cod_cliente,
        cod_tecnico=cod_tecnico,
        cod_vendedor=cod_vendedor,
        numserie=numserie,
        categoria_chamado=categoria_chamado,
        observacao_chamado=observacao_chamado,
        custo_deslocamento=custo_deslocamento,
        custo_hr=custo_hr,
        custo_km=custo_km,
        data_primeira_visita=data_primeira_visita,
        data_segunda_visita=data_segunda_visita,
        despesa_materiais=despesa_materiais,
        qtd_materiais=qtd_materiais,
        custo_materiais=custo_materiais,
        valor_total=valor_total,
        categoria_defeito=categoria_defeito,
        peca_defeito=peca_defeito,
        cod_peca_defeito=cod_peca_defeito,
        cod_peca_nova=cod_peca_nova,
    )

    db.add(new_os)
    await db.commit()
    await db.refresh(new_os)
    return new_os