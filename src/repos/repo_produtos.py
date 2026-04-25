from models import Produto
from sqlalchemy.orm import Session

def adicionar(produto: Produto, sessao: Session) -> None:
    
    # Adiciona o produto ao banco
    sessao.add(produto)
    
    # Salva as alterações
    sessao.commit()
    
    # Atualiza o objeto
    sessao.refresh(produto)

def atualizar(produto: Produto, sessao: Session) -> None:
    
    # Salva as alterações
    sessao.commit()
    
    # Atualiza o objeto
    sessao.refresh(produto)