from sqlalchemy import Column, Integer, String, Float
from .database import Base

class OS(Base):
    __tablename__ = "os"

    id = Column(Integer, primary_key=True, index=True)
    solicitante = Column(String, unique=True, index=True)
    data = Column(Float, default=100.0)
    servico = Column(String)
    valor = Column(Integer)
    status = Column(String)
    numserie = Column(String)  