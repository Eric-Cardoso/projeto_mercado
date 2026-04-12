from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from core.configuracoes import Base

# Criar uma tabela no banco e configurar ela
class Usuario(Base):
    # Define o nome da tabela
    __tablename__ = 'usuarios'

    # Configura cada campo da tabela
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=True)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    admin = Column(Boolean, nullable=False, default=False)

# Criar uma tabela no banco e configurar ela
class Produtos(Base):
    # Define o nome da tabela
    __tablename__ = 'produtos'

    # Configura cada campo da tabela
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(ForeignKey('usuarios.id'), nullable=False)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    categoria = Column(String, nullable=False)
    preco_unitario = Column(Float, nullable=False, default=0)


 