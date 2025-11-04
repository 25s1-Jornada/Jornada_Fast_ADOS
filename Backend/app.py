import os
import logging
from flask import Flask, jsonify, send_from_directory

# Configuração de Logging para Flask
logging.basicConfig(level=logging.INFO)

# Tentativa de importação do Neo4j
try:
    from neo4j import GraphDatabase, basic_auth
except ImportError:
    logging.error(
        "O pacote 'neo4j' não está instalado. Certifique-se de que está no requirements.txt."
    )

    # Define classes dummy para evitar erros de importação se o ambiente for ruim
    class GraphDatabase:
        @staticmethod
        def driver(*args, **kwargs):
            return None

    basic_auth = lambda *args: None

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define o caminho do frontend
TEMPLATE_PATH = '/app/frontend'
app = Flask(__name__)

# --- Configuração de Conexão com o Neo4j ---
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://db:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

driver = None
try:
    # A conexão é estabelecida, mas a verificação pode falhar se o Neo4j estiver lento
    driver = GraphDatabase.driver(
        NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD)
    )
    # Tenta verificar a conectividade imediatamente
    driver.verify_connectivity()
    logging.info("Conexão com o Neo4j estabelecida e verificada com sucesso!")
except Exception as e:
    # Se a conexão falhar, o erro é capturado e driver permanece None
    logging.error(
        f"Erro Crítico ao conectar com o Neo4j: {e}. A API não poderá buscar dados."
    )
    driver = None


@app.route("/")
def index():
    """ROTA PRINCIPAL: Serve o index.html diretamente."""
    try:
        logging.info(f"Servindo index.html do caminho: {TEMPLATE_PATH}")
        # Verifica se a pasta existe
        if os.path.exists(TEMPLATE_PATH):
            logging.info(f"✅ Pasta frontend encontrada! Conteúdo: {os.listdir(TEMPLATE_PATH)}")
        else:
            logging.error(f"❌ Pasta {TEMPLATE_PATH} não existe!")
            return jsonify({"error": "Frontend não montado"}), 500
            
        return send_from_directory(TEMPLATE_PATH, 'index.html')
    except Exception as e:
        logging.error(f"Erro ao servir 'index.html': {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/<path:filename>")
def serve_static(filename):
    """Serve arquivos estáticos do frontend."""
    try:
        return send_from_directory(TEMPLATE_PATH, filename)
    except Exception as e:
        logging.error(f"Erro ao servir arquivo estático '{filename}': {e}")
        return jsonify({"error": "Arquivo não encontrado"}), 404


@app.route("/api/data")
def get_data():
    """Endpoint da API para buscar os dados consolidados do Neo4j."""
    if not driver:
        # Retorna um erro amigável se o Neo4j não estiver pronto
        return (
            jsonify(
                {
                    "error": "Conexão com o Neo4j não estabelecida. Verifique os logs do contêiner 'Jornada_FAST'."
                }
            ),
            500,
        )

    # ... (O restante da sua lógica de query Cypher continua aqui)
    cypher_query = """
        OPTIONAL MATCH (os:OrdemServico)
        WITH count(os) AS totalOS
        OPTIONAL MATCH (p:Produto)
        WITH totalOS, count(p) AS totalProdutos
        OPTIONAL MATCH (t:Tecnico)
        WITH totalOS, totalProdutos, count(t) AS totalTecnicos
        OPTIONAL MATCH (c:Cidade)
        WITH totalOS, totalProdutos, totalTecnicos, count(c) AS totalCidades
        
        RETURN 
             totalOS, 
             totalProdutos, 
             totalTecnicos, 
             totalCidades
    """

    summary = {}
    try:
        with driver.session() as session:
            result = session.run(cypher_query)
            record = result.single()
            if record:
                summary = {
                    "summary": {
                        "totalOS": record["totalOS"],
                        "totalProdutos": record["totalProdutos"],
                        "totalTecnicos": record["totalTecnicos"],
                        "totalCidades": record["totalCidades"],
                    },
                    "osPorPeriodo": [],
                    "composicaoStatus": [],
                    "osPorTecnico": [],
                }
    except Exception as e:
        logging.error(f"Erro ao executar a query no Neo4j: {e}", exc_info=True)
        return (
            jsonify(
                {
                    "error": f"Erro ao executar a query no banco de dados. Consulte os logs.",
                    "details": str(e),
                }
            ),
            500,
        )

    return jsonify(summary)


if __name__ == "__main__":
    # Adicionar host="0.0.0.0" para que o Flask seja acessível no Docker.
    # O modo debug NÃO deve ser usado em produção
    app.run(host="0.0.0.0", port=8000)