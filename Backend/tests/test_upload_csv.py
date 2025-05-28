import os
from fastapi.testclient import TestClient
import src.main

app = src.main.app
client = TestClient(app)

# 🟢 Teste de upload válido
def test_upload_csv_valido():
    file_path = "tests/test_files/testeUpload.csv"

    with open(file_path, "rb") as file:
        response = client.post("/fast/OS/upload_csv", files={"file": ("ordens_servico.csv", file, "text/csv")})

    print("✅ Resposta API (Upload Válido):", response.status_code, response.json())

    assert response.status_code == 200
    assert "ordens de serviço inseridas com sucesso" in response.json()["message"]

# 🔴 Teste de upload com colunas erradas
def test_upload_csv_colunas_erradas():
    file_path = "tests/test_files/colunas_erradas.csv"

    with open(file_path, "rb") as file:
        response = client.post("/fast/OS/upload_csv", files={"file": ("colunas_erradas.csv", file, "text/csv")})

    print("❌ Resposta API (Colunas Erradas):", response.status_code, response.json())

    assert response.status_code == 400  # A API deve rejeitar o arquivo com colunas erradas

# 🔴 Teste de upload de arquivo que não é CSV
def test_upload_csv_arquivo_errado():
    file_path = "tests/test_files/arquivo_errado.txt"

    with open(file_path, "rb") as file:
        response = client.post("/fast/OS/upload_csv", files={"file": ("arquivo_errado.txt", file, "text/plain")})

    print("❌ Resposta API (Arquivo Não é CSV):", response.status_code, response.json())

    assert response.status_code == 400  # A API deve rejeitar arquivos que não são CSV

# 🔴 Teste de upload com valores errados (menos a data)
def test_upload_csv_valores_errados():
    file_path = "tests/test_files/valores_errados.csv"

    with open(file_path, "rb") as file:
        response = client.post("/fast/OS/upload_csv", files={"file": ("valores_errados.csv", file, "text/csv")})

    print("❌ Resposta API (Valores Errados):", response.status_code, response.json())

    assert response.status_code == 500  # A API deve falhar ao tentar inserir valores inválidos

# 🔎 Teste de consulta de OS para verificar inserção no banco
def test_consulta_os():
    response = client.get("/fast/OS/analise")  # Confirme o endpoint correto

    print("🔎 Dados do banco:", response.status_code, response.json())

    assert response.status_code == 200  # O endpoint de consulta deve funcionar corretamente
