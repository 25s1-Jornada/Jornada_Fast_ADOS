from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.database import AsyncSessionLocal
from src.models.OS import OS
from src.services.analise import create_OS
from datetime import datetime
import pandas as pd
from io import StringIO
import traceback
from sqlalchemy.exc import IntegrityError
from collections import Counter

router = APIRouter(prefix="/OS")

# Dependency para obter a sessão do banco assíncrona
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/newOS")
async def create_os_endpoint(
    id: int,
    solicitante: str,
    data: str,
    servico: str,
    valor: int,
    status: str,
    numserie: str,
    db: AsyncSession = Depends(get_db)
):
    new_os = await create_OS(id, solicitante, data, servico, valor, status, numserie, db)
    return {
        "id": new_os.id,
        "solicitante": new_os.solicitante,
        "data": new_os.data,
        "servico": new_os.servico,
        "valor": new_os.valor,
        "status": new_os.status,
        "numserie": new_os.numserie
    }

@router.get("/analise")
async def analise_tendencia(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OS))
    ordens = result.scalars().all()

    if not ordens:
        return {"message": "Nenhuma ordem de serviço encontrada."}

    # Converte os dados para DataFrame
    data = [{
        "data": os.data,
        "valor": os.valor,
        "servico": os.servico,
        "status": os.status
    } for os in ordens]

    df = pd.DataFrame(data)

    # Converte "data" para datetime
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df.dropna(subset=["data"])
    df["mes"] = df["data"].dt.to_period("M").astype(str)  # Ex: "2024-05"

    # Tendência de quantidade por mês
    qtd_por_mes = df.groupby("mes").size().to_dict()

    # Tendência de valor total por mês
    valor_total_mes = df.groupby("mes")["valor"].sum().to_dict()

    # Status mais comuns
    status_mais_comuns = Counter(df["status"]).most_common()

    # (Opcional) Tendência por serviço
    servicos_mais_comuns = Counter(df["servico"]).most_common()

    return {
        "quantidade_por_mes": qtd_por_mes,
        "valor_total_por_mes": valor_total_mes,
        "status_mais_comuns": status_mais_comuns,
        "servicos_mais_comuns": servicos_mais_comuns
    }

@router.post("/upload_csv") 
async def upload_os_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um CSV.")

    try:
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode("latin-1")), sep=";")
        df.columns = df.columns.str.strip().str.lower()

        required_columns = {"solicitante", "data", "servico", "valor", "status", "numserie"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail=f"CSV deve conter as colunas: {required_columns}")

        # Converte a coluna data
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df = df.dropna(subset=["data"])

        erros = []
        for i, row in df.iterrows():
            try:
                print(f"Processando linha {i}: {row.to_dict()}")

                os = OS(
                    solicitante=str(row["solicitante"]),
                    data=row["data"].strftime("%Y-%m-%d"),  # salva como string no modelo
                    servico=str(row["servico"]),
                    valor=int(float(row["valor"])),  # força conversão
                    status=str(row["status"]),
                    numserie=str(row["numserie"])
                )
                db.add(os)

            except Exception as e:
                print(f"Erro ao processar linha {i}: {e}")
                traceback.print_exc()
                erros.append({"linha": i, "erro": str(e)})

        try:
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            print("Erro de integridade ao salvar no banco:", e)
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Erro ao salvar dados no banco. Verifique duplicatas ou restrições.")

        if erros:
            return {
                "message": f"{len(df) - len(erros)} ordens de serviço inseridas com sucesso.",
                "erros": erros
            }

        return {"message": f"{len(df)} ordens de serviço inseridas com sucesso."}

    except Exception as e:
        print("Erro inesperado no upload:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro interno ao processar o arquivo CSV.")

