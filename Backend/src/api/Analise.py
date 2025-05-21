#from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.OS import OS
from src.services.analise import create_OS
import pandas as pd
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from io import StringIO

router = APIRouter(prefix="/OS")

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
       await db.close()

@router.get("/newOS")
async def list_bets(id: int,solicitante: str,data:str,servico:str,valor: int,status:str, numserie: str,db:Session = Depends(get_db)):
    id=id
    solicitante=solicitante
    data=data
    servico=servico
    valor=valor
    status=status
    numserie=numserie
    new_OS= await create_OS(id,solicitante,data,servico,valor,status,numserie,db)
    return {
        "id": new_OS.id,
        "solicitante":new_OS.solicitante,
        "data":new_OS.data,
        "servico":new_OS.servico,
        "valor":new_OS.valor,
        "status":new_OS.status,
        "numserie":new_OS.numserie
    }

@router.get("/analise")
async def analise_tendencia(db:Session = Depends(get_db)):
# realisação da analise de tendencia de OS
    
    result = await db.execute(select(OS))
    ordens = result.scalars().all()

    # Transformar os dados em uma lista de dicionários
    os_data = [
        {
            "id": os.id,
            "solicitante": os.solicitante,
            "data": os.data,
            "servico": os.servico,
            "valor": os.valor,
            "status": os.status,
            "numserie": os.numserie
        }
        for os in ordens
    ]

    if not os_data:
        return {"mensagem": "Nenhuma OS encontrada para análise."}

    # Criar DataFrame
    df = pd.DataFrame(os_data)

    # Converter data para datetime se necessário
    df["data"] = pd.to_datetime(df["data"])

    # Criar coluna com ano-mês
    df["mes"] = df["data"].dt.to_period("M").astype(str)

    # Agrupar por mês: contar OS e somar valores
    tendencia = df.groupby("mes").agg(qtd_OS=("id", "count"), total_valor=("valor", "sum")).reset_index()

    # Converter para dicionário (JSON serializável)
    tendencia_dict = tendencia.to_dict(orient="records")

    return {"tendencia_OS": tendencia_dict}

@router.post("/OS/upload_csv")
async def upload_os_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um CSV.")

    try:
        # Lê o conteúdo do arquivo CSV para string
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode("utf-8")))

        # Verifica se as colunas esperadas estão presentes
        required_columns = {"solicitante", "data", "servico", "valor", "status", "numserie"}
        if not required_columns.issubset(set(df.columns)):
            raise HTTPException(status_code=400, detail=f"CSV deve conter as colunas: {required_columns}")

        # Converte a coluna de data e ignora linhas inválidas
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df = df.dropna(subset=["data"])  # Remove linhas com data inválida

        # Insere no banco de dados
        for _, row in df.iterrows():
            os = OrdemServico(
                solicitante=row["solicitante"],
                data=row["data"].date() if isinstance(row["data"], datetime) else None,
                servico=row["servico"],
                valor=row["valor"],
                status=row["status"],
                numserie=row["numserie"]
            )
            db.add(os)
        db.commit()

        return {"message": f"{len(df)} ordens de serviço inseridas com sucesso."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))