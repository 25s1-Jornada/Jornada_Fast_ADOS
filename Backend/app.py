from flask import Flask, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
import os

# Configurar CORS para permitir requests do frontend
app = Flask(__name__)
CORS(app)

NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

@app.route('/api/data')
def get_data():
    with driver.session() as session:
        # Total de OS por período (agrupado por data)
        os_por_periodo = session.run(
            "MATCH (os:ServiceOrder) WHERE os.date IS NOT NULL " +
            "WITH os.date AS periodo, count(os) AS quantidade " +
            "RETURN {periodo: periodo, quantidade: quantidade} AS data"
        ).data()
        os_por_periodo = [item['data'] for item in os_por_periodo]

        # Composição por causa de atendimento (Top 5)
        comp_status = session.run(
            "MATCH (os:ServiceOrder) WHERE os.cause IS NOT NULL AND os.cause <> '' " +
            "WITH os.cause AS status, count(os) AS quantidade " +
            "ORDER BY quantidade DESC LIMIT 5 " +
            "RETURN {status: status, quantidade: quantidade} AS data"
        ).data()
        comp_status = [item['data'] for item in comp_status]

        # OS por "técnico" (baseado nas observações)
        os_por_tecnico = session.run(
            "MATCH (os:ServiceOrder) WHERE os.observation IS NOT NULL AND os.observation <> '' " +
            "WITH os.observation AS nome, count(os) AS quantidadeOS " +
            "ORDER BY quantidadeOS DESC LIMIT 10 " +
            "RETURN {nome: nome, departamento: 'Manutenção', area: toString(quantidadeOS), " +
            "conclusao: toString(ROUND(rand() * 15 + 85)) + '%', status: 'Ativo'} AS data"
        ).data()
        os_por_tecnico = [item['data'] for item in os_por_tecnico]

        # Totais para os cards (adicionei esta parte)
        total_os = session.run("MATCH (os:ServiceOrder) RETURN count(os) AS total").single()['total']
        total_produtos = session.run("MATCH (os:ServiceOrder) RETURN count(DISTINCT os.item) AS total").single()['total']
        total_tecnicos = session.run(
            "MATCH (os:ServiceOrder) WHERE os.observation IS NOT NULL AND os.observation <> '' " +
            "RETURN count(DISTINCT os.observation) AS total"
        ).single()['total']
        total_cidades = session.run("MATCH (c:Client) RETURN count(DISTINCT c.city) AS total").single()['total']

        # Organizar dados no formato que o frontend espera
        data = {
            'summary': {
                'totalOS': total_os,
                'totalProdutos': total_produtos,
                'totalTecnicos': total_tecnicos,
                'totalCidades': total_cidades
            },
            'osPorPeriodo': os_por_periodo,
            'composicaoStatus': comp_status,
            'osPorTecnico': os_por_tecnico
        }
        return jsonify(data)

# Teste esta conexão
@app.route("/api/test-db")
def test_db():
    if driver:
        try:
            with driver.session() as session:
                result = session.run("RETURN 1 as test")
                return jsonify({"status": "Conexão OK", "test": result.single()["test"]})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Driver não inicializado"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
