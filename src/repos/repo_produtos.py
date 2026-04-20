from models import Produtos
from sqlalchemy.orm import Session

def adicionar(produto: Produtos, sessao: Session) -> None:
    # Adiciona o produto ao banco
    sessao.add(produto)
    
    # Salva as alterações
    sessao.commit()
    
    # Atualiza o objeto
    sessao.refresh(produto)