from fastapi import FastAPI
from src.routes import os_routes

app = FastAPI(title="API - OS com Neo4j")

# Rotas principais
app.include_router(os_routes.router)

@app.get("/")
def root():
    return {"mensagem": "API com Neo4j está funcionando 🚀"}
