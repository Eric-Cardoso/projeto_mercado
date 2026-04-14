from models import Usuario
from sqlalchemy.orm import Session

def criar(usuario: Usuario, sessao: Session) -> Usuario:
    # Adiciona o usuário ao banco
    sessao.add(usuario)
    # Salva as alterações
    sessao.commit()
    # Atualiza o objeto
    sessao.refresh(usuario)
    