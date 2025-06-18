from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


'''
class OS(Base):
    __tablename__ = "os"

    id = Column(Integer, primary_key=True, index=True)
    solicitante = Column(String, unique=True, index=True)
    data = Column(String)
    servico = Column(String)
    valor = Column(Integer)
    status = Column(String)
    numserie = Column(String)  
'''

'''
    id = Column(Integer, primary_key=True, index=True)

    cod_cliente = Column(String, index=True)
    cod_tecnico = Column(String)
    cod_vendedor = Column(String)

    numserie = Column(String)  # Número de série do equipamento

    categoria_chamado = Column(String)
    observacao_chamado = Column(String)

    custo_deslocamento = Column(Float)
    custo_hr = Column(Float)
    custo_km = Column(Float)

    data_primeira_visita = Column(Date)
    data_segunda_visita = Column(Date)

    despesa_materiais = Column(Float)
    qtd_materiais = Column(Integer)
    custo_materiais = Column(Float)

    valor_total = Column(Float)

    categoria_defeito = Column(String)
    peca_defeito = Column(String)
    cod_peca_defeito = Column(String)
    cod_peca_nova = Column(String)
'''


class OS(Base):
    __tablename__ = "os"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date)	
    numero_chamado	= Column(String)
    cod_cliente	= Column(String)
    nome_cliente	= Column(String)
    cidade	= Column(String)
    estado	= Column(String)
    numserie	= Column(String)
    item	= Column(String)
    data_fabricacao	= Column(Date)
    data_emissao_nf = Column(Date)
    tipo	= Column(String)
    causa	= Column(String)	
    observacao = Column(String)