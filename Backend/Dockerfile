FROM python:3.10

# Define o diretório de trabalho DENTRO do container.
WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código da pasta Backend para /app
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para rodar o FastAPI
CMD ["gunicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
