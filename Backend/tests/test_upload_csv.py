# tests/test_upload_csv.py

import os
from datetime import date
from fastapi.testclient import TestClient
import src.main
import pytest # Importar pytest para usar @pytest.mark.asyncio

# A app FastAPI e o TestClient são definidos aqui no arquivo
app = src.main.app
client = TestClient(app)

# Helper para caminho dos arquivos de teste
BASE_DIR = os.path.dirname(__file__)
TEST_FILES_DIR = os.path.join(BASE_DIR, "test_files")

# --- Testes que passaram anteriormente (mantidos ativos) ---

def test_upload_csv_arquivo_errado():
    file_path = os.path.join(TEST_FILES_DIR, "arquivo_errado.txt")
    with open(file_path, "rb") as file:
        response = client.post("/fast/OS/upload_csv", files={"file": ("arquivo_errado.txt", file, "text/plain")})
    print("❌ Resposta API (Arquivo Não é CSV):", response.status_code, response.json())
    assert response.status_code == 400

def test_upload_csv_valores_errados():
    file_path = os.path.join(TEST_FILES_DIR, "valores_errados.csv")
    with open(file_path, "rb") as file:
        response = client.post("/fast/OS/upload_csv", files={"file": ("valores_errados.csv", file, "text/csv")})
    print("❌ Resposta API (Valores Errados):", response.status_code, response.json())
    assert response.status_code == 500


### Testes Separados para Criação (POST) e Consulta (GET)

# Dados comuns para os testes de OS
# ATENÇÃO: Se o banco de dados não for limpo entre os testes,
# você pode precisar de IDs únicos ou uma fixture para limpar o DB.
OS_TEST_ID = 99999
CURRENT_DATE_STR = str(date.today())

OS_PAYLOAD = {
    "id": OS_TEST_ID,
    "cod_cliente": "CLI_TESTE_API_01",
    "cod_tecnico": "TEC_TESTE_API_01",
    "cod_vendedor": "VEN_TESTE_API_01",
    "numserie": "SN_TESTE_API_01",
    "categoria_chamado": "Instalacao de Software",
    "observacao_chamado": "Instalacao do pacote Office 2024",
    "custo_deslocamento": 50.50,
    "custo_hr": 75.00,
    "custo_km": 2.10,
    "data_primeira_visita": CURRENT_DATE_STR,
    "data_segunda_visita": CURRENT_DATE_STR,
    "despesa_materiais": 120.00,
    "qtd_materiais": 2,
    "custo_materiais": 60.00,
    "valor_total": 247.60,
    "categoria_defeito": "Software",
    "peca_defeito": "Office Suite",
    "cod_peca_defeito": "SW001",
    "cod_peca_nova": "SW002"
}

@pytest.mark.asyncio
async def test_create_os():
    """
    Testa a criação de uma nova OS via endpoint POST /newOS.
    """
    print("\n--- INICIANDO TESTE: Criação de OS via API (POST) ---")

    print(f"DEBUG: Enviando POST para /fast/OS/newOS com ID: {OS_TEST_ID}")
    # Usando 'params=' se o endpoint espera query parameters, ou 'json=' se espera um corpo JSON
    response_post = client.post("/fast/OS/newOS", params=OS_PAYLOAD)

    print("✅ Resposta API (POST /newOS):", response_post.status_code, response_post.json())

    assert response_post.status_code == 200, \
        f"POST /newOS falhou com status {response_post.status_code}: {response_post.json()}"
    
    # Verifica algumas chaves essenciais na resposta
    assert response_post.json()["id"] == OS_PAYLOAD["id"]
    assert response_post.json()["cod_cliente"] == OS_PAYLOAD["cod_cliente"]
    assert response_post.json()["numserie"] == OS_PAYLOAD["numserie"]
    assert response_post.json()["valor_total"] == OS_PAYLOAD["valor_total"]
    
    print("--- TESTE CONCLUÍDO: Criação de OS via API (POST) ---")


@pytest.mark.asyncio
async def test_get_os_after_creation():
    """
    Testa a consulta de uma OS via endpoint GET /analise após sua criação.
    Este teste assume que a OS criada em test_create_os ainda existe no DB.
    """
    print("\n--- INICIANDO TESTE: Consulta de OS via API (GET) após Criação ---")

    # Para garantir que a OS existe antes de consultar,
    # uma boa prática seria limpar o DB no início do teste e criá-la aqui,
    # ou usar uma fixture de setup/teardown.
    # Por enquanto, estamos assumindo que test_create_os foi executado e foi bem-sucedido.
    
    current_year = date.today().year
    current_month = date.today().month

    print(f"DEBUG: Enviando GET para /fast/OS/analise para Ano: {current_year}, Mês: {current_month}")
    response_get = client.get("/fast/OS/analise", params={"ano": current_year, "mes": current_month})

    print("🔎 Resposta API (GET /analise):", response_get.status_code, response_get.json())

    assert response_get.status_code == 200, \
        f"GET /analise falhou com status {response_get.status_code}: {response_get.json()}"
    
    analise_data = response_get.json()

    # Verifica se o tipo da resposta é um dicionário, como esperado para /analise
    assert isinstance(analise_data, dict) 

    # Verifica se há dados para o mês específico
    month_key = f"{current_year}-{current_month:02d}"
    assert analise_data["quantidade_por_mes"].get(month_key) is not None
    assert analise_data["valor_total_por_mes"].get(month_key) is not None

    # Verifica se a categoria de defeito e peça de defeito da OS testada aparecem
    # (Pode precisar de ajustes se houver muitos dados no DB e o item específico não for top)
    assert any(item[0] == OS_PAYLOAD["categoria_defeito"] for item in analise_data["categoria_defeitos_mais_comuns"])
    assert any(item[0] == OS_PAYLOAD["peca_defeito"] for item in analise_data["pecas_defeito_mais_comuns"])

    print("--- TESTE CONCLUÍDO: Consulta de OS via API (GET) após Criação ---")