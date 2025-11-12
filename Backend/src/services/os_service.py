from src.neo4j_connection import neo4j_db

def criar_os(dados: dict):
    """
    Cria um novo nó OS no banco Neo4j.
    """
    query = """
    CREATE (o:OS {
        id: randomUUID(),
        numero_chamado: $numero_chamado,
        nome_cliente: $nome_cliente,
        cidade: $cidade,
        estado: $estado,
        tipo: $tipo,
        causa: $causa,
        observacao: $observacao
    })
    RETURN o
    """
    result = neo4j_db.query(query, dados)
    return result[0]["o"] if result else None


def listar_os():
    """
    Retorna todos os nós OS do banco.
    """
    query = "MATCH (o:OS) RETURN o LIMIT 50"
    result = neo4j_db.query(query)
    return [r["o"] for r in result]


def buscar_os_por_cidade(cidade: str):
    """
    Busca OS por cidade.
    """
    query = "MATCH (o:OS {cidade: $cidade}) RETURN o"
    result = neo4j_db.query(query, {"cidade": cidade})
    return [r["o"] for r in result]
