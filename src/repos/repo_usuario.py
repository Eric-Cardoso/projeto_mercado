from models import Usuario
from sqlalchemy.orm import Session

def criar(usuario: Usuario, sessao: Session) -> None:
    # Adiciona o usuário ao banco
    sessao.add(usuario)
    # Salva as alterações
    sessao.commit()
    # Atualiza o objeto
    sessao.refresh(usuario)

def atualizar(usuario: Usuario, sessao: Session) -> None:
    # Salva as alterações
    sessao.commit()
    # Atualiza o objeto
    sessao.refresh(usuario)

def deletar(usuario: Usuario, sessao: Session) -> None:
    # Deleta o usuário do banco
    sessao.delete(usuario)
    # Salva as alterações
    sessao.commit()

    