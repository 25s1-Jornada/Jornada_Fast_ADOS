from src.neo4j_connection import neo4j_db

def resumo_geral():
    query = """
    MATCH (o:OS)
    RETURN count(o) AS total_os
    """
    result = neo4j_db.query(query)
    return result[0] if result else {}

def total_os_por_periodo():
    query = """
    MATCH (o:OS)
    WITH apoc.date.format(o.data_criacao, 'ms', 'yyyy-MM') AS periodo, count(o) AS total
    RETURN periodo, total
    ORDER BY periodo
    """
    return neo4j_db.query(query)

def principais_causas():
    query = """
    MATCH (o:OS)
    RETURN o.causa AS causa, count(o) AS total
    ORDER BY total DESC
    LIMIT 10
    """
    return neo4j_db.query(query)

def os_por_tecnico():
    query = """
    MATCH (o:OS)
    RETURN o.tecnico AS tecnico, count(o) AS total
    ORDER BY total DESC
    """
    return neo4j_db.query(query)

def os_filtrados(filtros: dict):
    # Permite filtrar por tecnico, departamento, area, conclusao, status
    query = """
    MATCH (o:OS)
    WHERE ($tecnico IS NULL OR o.tecnico = $tecnico)
    AND ($departamento IS NULL OR o.departamento = $departamento)
    AND ($area IS NULL OR o.area = $area)
    AND ($conclusao IS NULL OR o.conclusao = $conclusao)
    AND ($status IS NULL OR o.status = $status)
    RETURN o
    ORDER BY o.data_criacao DESC
    LIMIT 100
    """
    return neo4j_db.query(query, filtros)
