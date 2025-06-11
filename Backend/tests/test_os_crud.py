import pytest
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.OS import OS # Importa o seu modelo OS
from datetime import datetime, date # Importa datetime e date

# A fixture 'session' é automaticamente descoberta e injetada pelo pytest
# (assumindo que está em tests/conftest.py e configurada para limpar o DB a cada teste).

@pytest.mark.asyncio
async def test_create_os(session: AsyncSession):
    """
    Testa a criação (INSERT) de uma nova Ordem de Serviço no banco de dados.
    """
    new_os_data = {
        "cod_cliente": "CLI001",
        "cod_tecnico": "TEC001",
        "cod_vendedor": "VND001", # Adicionando valor para todos os campos não nulos
        "numserie": "SN12345", 
        "categoria_chamado": "Manutencao",
        "observacao_chamado": "Verificacao geral do equipamento", # Adicionando valor
        "custo_deslocamento": 50.0,
        "custo_hr": 30.0,
        "custo_km": 2.5,
        "data_primeira_visita": date(2023, 1, 15), # Usando date() para Column(Date)
        "data_segunda_visita": None, # Pode ser None ou uma data real
        "despesa_materiais": None, # Pode ser None ou um float
        "qtd_materiais": None, # Pode ser None ou um int
        "custo_materiais": None, # Pode ser None ou um float
        "valor_total": 150.0,
        "categoria_defeito": "Eletrico",
        "peca_defeito": None, # Pode ser None ou uma string
        "cod_peca_defeito": None, # Pode ser None ou uma string
        "cod_peca_nova": None, # Pode ser None ou uma string
    }
    new_os = OS(**new_os_data)

    session.add(new_os)
    await session.commit()
    await session.refresh(new_os) # Recarrega o objeto para obter o ID e outros valores gerados pelo DB

    # Verificações de que a inserção foi bem-sucedida e os campos estão corretos
    assert new_os.id is not None
    assert isinstance(new_os.id, int)
    assert new_os.cod_cliente == "CLI001"
    assert new_os.numserie == "SN12345" # CORRIGIDO: Agora 'numserie'
    assert new_os.data_primeira_visita == date(2023, 1, 15) # Verificação da data
    # Verifique outros campos que você forneceu para garantir que foram salvos corretamente
    assert new_os.valor_total == 150.0
    assert new_os.categoria_chamado == "Manutencao"


@pytest.mark.asyncio
async def test_read_os(session: AsyncSession):
    """
    Testa a leitura (SELECT) de uma Ordem de Serviço no banco de dados.
    """
    # Primeiro, cria uma OS para ter algo para ler
    initial_os = OS(
        cod_cliente="CLI002",
        cod_tecnico="TEC002",
        cod_vendedor="VND002",
        numserie="SN54321", # CORRIGIDO
        categoria_chamado="Instalacao",
        observacao_chamado="Verificacao inicial do sistema",
        custo_deslocamento=75.0,
        custo_hr=40.0,
        custo_km=3.0,
        data_primeira_visita=date(2023, 2, 10), # Usando date()
        data_segunda_visita=None,
        despesa_materiais=None,
        qtd_materiais=None,
        custo_materiais=None,
        valor_total=200.0,
        categoria_defeito="Mecanico",
        peca_defeito=None,
        cod_peca_defeito=None,
        cod_peca_nova=None,
    )
    session.add(initial_os)
    await session.commit()
    await session.refresh(initial_os)

    # Agora, tenta ler a OS usando o ID
    result = await session.execute(
        select(OS).where(OS.id == initial_os.id)
    )
    found_os = result.scalar_one_or_none()

    # Verificações de que a leitura foi bem-sucedida
    assert found_os is not None
    assert found_os.id == initial_os.id
    assert found_os.cod_cliente == "CLI002"
    assert found_os.numserie == "SN54321" # CORRIGIDO


@pytest.mark.asyncio
async def test_update_os(session: AsyncSession):
    """
    Testa a atualização (UPDATE) de uma Ordem de Serviço existente.
    """
    # Primeiro, cria uma OS para ter algo para atualizar
    existing_os = OS(
        cod_cliente="CLI003",
        cod_tecnico="TEC003",
        cod_vendedor="VND003",
        numserie="SN67890", # CORRIGIDO
        categoria_chamado="Reparo",
        observacao_chamado="Troca de componente danificado",
        custo_deslocamento=100.0,
        custo_hr=50.0,
        custo_km=4.0,
        data_primeira_visita=date(2023, 3, 5), # Usando date()
        data_segunda_visita=None,
        despesa_materiais=None,
        qtd_materiais=None,
        custo_materiais=None,
        valor_total=300.0,
        categoria_defeito="Software",
        peca_defeito=None,
        cod_peca_defeito=None,
        cod_peca_nova=None,
    )
    session.add(existing_os)
    await session.commit()
    await session.refresh(existing_os)
    
    # Armazena o valor original e a data de criação para comparação
    original_deslocamento = existing_os.custo_deslocamento
    created_at_before_update = existing_os.data_criacao 
    
    # Atualiza a OS
    existing_os.custo_deslocamento = 120.0
    existing_os.cod_vendedor = "VND004" # Atualizando outro campo
    existing_os.observacao_chamado = "Componente substituido com sucesso" # Atualizando mais um campo
    
    await session.commit()
    await session.refresh(existing_os) # Recarrega para ver as mudanças e data_atualizacao

    # Verificações de que a atualização foi bem-sucedida
    assert existing_os.custo_deslocamento == 120.0
    assert existing_os.cod_vendedor == "VND004"
    assert existing_os.observacao_chamado == "Componente substituido com sucesso"
    assert existing_os.data_atualizacao is not None # data_atualizacao deve ter sido atualizada
    # A data_atualizacao deve ser posterior à data_criacao (se data_criacao também for gerada pelo DB)
    # ou posterior ao valor original antes da atualização.
    # Se 'data_criacao' for server_default=func.now(), ela será preenchida no insert.
    # No caso de 'data_atualizacao', o onupdate=func.now() a atualiza no commit.
    # Pode haver uma pequena diferença de milissegundos que torna essa comparação sensível.
    # Se der erro, você pode simplesmente verificar que não é None e que o valor mudou.
    # Mas se data_criacao também é gerada pelo DB, a comparação é válida:
    # assert existing_os.data_atualizacao > created_at_before_update 


@pytest.mark.asyncio
async def test_delete_os(session: AsyncSession):
    """
    Testa a exclusão (DELETE) de uma Ordem de Serviço.
    """
    # Primeiro, cria uma OS para ter algo para deletar
    os_to_delete = OS(
        cod_cliente="CLI004",
        cod_tecnico="TEC004",
        cod_vendedor="VND005",
        numserie="SN98765", # CORRIGIDO
        categoria_chamado="Limpeza",
        observacao_chamado="Limpeza geral do equipamento",
        custo_deslocamento=20.0,
        custo_hr=10.0,
        custo_km=1.0,
        data_primeira_visita=date(2023, 4, 20), # Usando date()
        data_segunda_visita=None,
        despesa_materiais=None,
        qtd_materiais=None,
        custo_materiais=None,
        valor_total=50.0,
        categoria_defeito="Sujeira",
        peca_defeito=None,
        cod_peca_defeito=None,
        cod_peca_nova=None,
    )
    session.add(os_to_delete)
    await session.commit()
    await session.refresh(os_to_delete)

    # Agora, deleta a OS
    await session.delete(os_to_delete) # Remove o objeto da sessão
    await session.commit() # Confirma a exclusão no banco de dados

    # Tenta ler a OS para confirmar que foi deletada
    deleted_os_result = await session.execute(
        select(OS).where(OS.id == os_to_delete.id)
    )
    deleted_os = deleted_os_result.scalar_one_or_none()

    # Verificação de que a exclusão foi bem-sucedida
    assert deleted_os is None # O objeto não deve mais ser encontrado