from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.os_routes import router as os_router
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(os_router)

app = FastAPI(
    title="ADOS - Análise de Dados de Ordens de Serviço",
    description="API para gerenciamento e análise de OSs da Fast Gôndolas",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(os_router)

@app.get("/")
def root():
    return {"message": "API ADOS funcionando! 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok", "database": "neo4j"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
