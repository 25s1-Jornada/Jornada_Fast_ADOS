import sys
import os

# Adiciona a pasta Backend no sys.path para o import funcionar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import main  # agora esse import funciona normalmente
from fastapi.testclient import TestClient
import pytest

app = main.app
client = TestClient(app)

BASE_DIR = os.path.dirname(__file__)
TEST_FILES_DIR = os.path.join(BASE_DIR, "test_files")


def test_upload_csv_arquivo_errado():
    """
    Testa o endpoint de upload de CSV com um arquivo de tipo incorreto (ex: .txt).
    Espera uma resposta de status 400 (Bad Request).
    """
    file_path = os.path.join(TEST_FILES_DIR, "arquivo_errado.txt")
    with open(file_path, "rb") as file:
        response = client.post("/fast/OS/upload_csv", files={"file": ("arquivo_errado.txt", file, "text/plain")})
    print("❌ Resposta API (Arquivo Não é CSV):", response.status_code, response.json())
    assert response.status_code == 400
    assert "O arquivo deve ser um CSV." in response.json().get("detail", "")


def test_upload_csv_valores_errados():
    """
    Testa o endpoint de upload de CSV com um arquivo CSV que contém valores inválidos.
    Espera uma resposta de status 500 (Internal Server Error) devido a problemas de processamento.
    """
    file_path = os.path.join(TEST_FILES_DIR, "valores_errados.csv")
    with open(file_path, "rb") as file:
        response = client.post("/fast/OS/upload_csv", files={"file": ("valores_errados.csv", file, "text/csv")})
    print("❌ Resposta API (Valores Errados):", response.status_code, response.json())
    assert response.status_code == 500

    expected_message_part = "erro interno ao processar o arquivo csv."
    actual_message = response.json().get("detail", "").lower()
    assert expected_message_part in actual_message
