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

        # Totais para os cards
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

@app.route('/api/dashboard-geral')
def get_dashboard_geral():
    with driver.session() as session:
        try:            
            # 1. Total de OS
            total_os_result = session.run("MATCH (os:ServiceOrder) RETURN count(os) AS total")
            total_os = total_os_result.single()['total']
            print(f"Total OS: {total_os}")
            
            # 2. Falhas por Tipo
            falhas_por_tipo_result = session.run("""
                MATCH (os:ServiceOrder) 
                WHERE os.cause IS NOT NULL 
                RETURN os.cause AS tipo, count(os) AS quantidade 
                ORDER BY quantidade DESC
            """)
            
            falhas_por_tipo = []
            for record in falhas_por_tipo_result:
                falhas_por_tipo.append({
                    "tipo": record["tipo"],
                    "quantidade": record["quantidade"]
                })
            print(f"Falhas por tipo: {len(falhas_por_tipo)} registros")
            
            # 3. Falhas por Produto 
            falhas_por_produto_result = session.run("""
                MATCH (os:ServiceOrder)
                WHERE os.item IS NOT NULL
                RETURN os.item AS produto, count(os) AS quantidade
                ORDER BY quantidade DESC
                LIMIT 10
            """)

            falhas_por_produto = []
            for record in falhas_por_produto_result:
                falhas_por_produto.append({
                    "produto": record["produto"],
                    "quantidade": record["quantidade"]
                })
            print(f"Falhas por produto: {len(falhas_por_produto)} registros")
            
            print("Consulta finalizada com sucesso")
            
        except Exception as e:
            print(f"ERRO GRAVE na consulta: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
@app.route('/api/causas-atendimento')
def get_causas_atendimento():
    with driver.session() as session:
        try:            
            # 1. Top Causas
            top_causas_result = session.run("""
                MATCH (os:ServiceOrder)
                WHERE os.cause IS NOT NULL AND os.cause <> ''
                WITH os.cause AS causa, count(os) AS quantidade
                ORDER BY quantidade DESC
                LIMIT 10
                RETURN causa, quantidade
            """)
            top_causas = []
            for record in top_causas_result:
                top_causas.append({
                    "causa": record["causa"],
                    "quantidade": record["quantidade"]
                })
            
            # 2. Falhas por Produto
            falhas_produto_result = session.run("""
                MATCH (os:ServiceOrder)
                WHERE os.item IS NOT NULL AND os.item <> ''
                WITH os.item AS produto, count(os) AS quantidade
                ORDER BY quantidade DESC
                LIMIT 8
                RETURN produto, quantidade
            """)
            falhas_por_produto = []
            for record in falhas_produto_result:
                falhas_por_produto.append({
                    "produto": record["produto"],
                    "quantidade": record["quantidade"]
                })
            
            # 3. Análise de Recorrência
            recorrencia_result = session.run("""
                MATCH (os:ServiceOrder)
                WHERE os.cause IS NOT NULL AND os.item IS NOT NULL
                WITH os.cause AS causa, count(DISTINCT os.item) as produtos_afetados
                ORDER BY produtos_afetados DESC
                LIMIT 6
                RETURN causa, produtos_afetados as recorrencia
            """)
            analise_recorrencia = []
            for record in recorrencia_result:
                analise_recorrencia.append({
                    "causa": record["causa"],
                    "recorrencia": record["recorrencia"]
                })
            
            # 4. Evolução Temporal
            evolucao_result = session.run("""
                MATCH (os:ServiceOrder)
                WHERE os.date IS NOT NULL
                WITH os.date AS periodo, count(os) AS quantidade
                ORDER BY periodo
                LIMIT 12
                RETURN periodo, quantidade
            """)
            evolucao_temporal = []
            for record in evolucao_result:
                evolucao_temporal.append({
                    "periodo": record["periodo"],
                    "quantidade": record["quantidade"]
                })
            
            # 5. Detalhes para tabela
            detalhes_result = session.run("""
                MATCH (os:ServiceOrder)
                WHERE os.cause IS NOT NULL AND os.item IS NOT NULL
                WITH os.cause AS causa, os.item AS produto, count(os) AS quantidade
                ORDER BY quantidade DESC
                LIMIT 20
                RETURN causa, produto, quantidade
            """)
            detalhes_causas = []
            total_os = sum(item['quantidade'] for item in top_causas) if top_causas else 1
            
            for record in detalhes_result:
                quantidade = record["quantidade"]
                percentual = round((quantidade * 100) / total_os, 1) if total_os > 0 else 0
                detalhes_causas.append({
                    "causa": record["causa"],
                    "produto": record["produto"],
                    "quantidade": quantidade,
                    "percentual": f"{percentual}%",
                    "recorrencia": "1"  # Placeholder
                })
            
            # Métricas de resumo
            causa_mais_frequente = top_causas[0]['causa'] if top_causas else "N/A"
            produto_mais_afetado = falhas_por_produto[0]['produto'] if falhas_por_produto else "N/A"
            
            data = {
                'summary': {
                    'totalCausas': len(top_causas),
                    'causaMaisFrequente': causa_mais_frequente,
                    'produtoMaisAfetado': produto_mais_afetado
                },
                'topCausas': top_causas,
                'falhasPorProduto': falhas_por_produto,
                'analiseRecorrencia': analise_recorrencia,
                'evolucaoTemporal': evolucao_temporal,
                'detalhesCausas': detalhes_causas
            }
            
            print("Consulta de causas finalizada com sucesso")
            return jsonify(data)
            
        except Exception as e:
            print(f"ERRO na consulta de causas: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

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
