from flask import Flask, jsonify
from neo4j import GraphDatabase
import os

app = Flask(__name__)

NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

@app.route('/apidata')
def get_data():
    with driver.session() as session:
        # Exemplo: obter total de OS por período
        os_por_periodo = session.run(
            "MATCH (o:OS) RETURN o.periodo AS periodo, COUNT(o) AS quantidade"
        ).data()

        # Exemplo: composição de status
        comp_status = session.run(
            "MATCH (o:OS) RETURN o.status AS status, COUNT(o) AS quantidade"
        ).data()

        # Exemplo: OS por técnico
        os_por_tecnico = session.run(
            "MATCH (t:Técnico)-[:FEZ]->(o:OS) RETURN t.nome AS nome, t.departamento AS departamento, t.area AS area, o.conclusao AS conclusao, o.status AS status"
        ).data()

        # Organizar dados
        data = {
            'osPorPeriodo': os_por_periodo,
            'composicaoStatus': comp_status,
            'osPorTecnico': os_por_tecnico
        }
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')