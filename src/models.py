from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
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
class Carrinho(Base):
    # Define o nome da tabela
    __tablename__ = 'carrinhos'

    # Configura cada campo da tabela
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(ForeignKey('usuarios.id'))
    status = Column(String, nullable=False, default='PENDENTE')
    desconto_total = Column(Float, nullable=False, default=0)
    preco_total = Column(Float, nullable=False, default=0)
    quantidade_produtos = Column(Integer, nullable=False, default=0)
    produtos = relationship('Produto', cascade='all, delete')

    def calcular_preco(self):
        self.preco_total = sum(
                produto.quantidade * produto.preco_unitario - produto.desconto 
                for produto in self.produtos
        )
    
    def calcular_desconto(self):
        self.desconto_total = sum(
            produto.desconto for produto in self.produtos
        )


# Criar uma tabela no banco e configurar ela
class Produto(Base):
    # Define o nome da tabela
    __tablename__ = 'produtos'

    # Configura cada campo da tabela
    id = Column(Integer, primary_key=True, index=True)
    id_carrinho = Column(ForeignKey('carrinhos.id'), nullable=False)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    categoria = Column(String, nullable=False)
    preco_unitario = Column(Float, nullable=False, default=0)
    desconto = Column(Float, nullable=False, default=0)


 