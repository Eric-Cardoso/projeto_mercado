from models import Carrinho
from sqlalchemy.orm import Session

def criar(carrinho: Carrinho, sessao: Session) -> None:
    
    # Adiciona o carrinho ao banco
    sessao.add(carrinho)
    
    # Salva as alterações
    sessao.commit()
    
    # Atualiza o objeto
    sessao.refresh(carrinho)