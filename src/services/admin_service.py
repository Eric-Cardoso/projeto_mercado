from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Usuario


def obter_usuario(
        id_usuario: int, 
        usuario: Usuario,  
        sessao: Session
) -> Usuario:
    
    # Tenta pegar o usuário de acordo com o id
    db_usuario = sessao.scalar(select(Usuario).where(Usuario.id == id_usuario))

    # Verifica se o usuário é admin
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
)
    # Verifica se o usuário foi encontrado
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado'
)
    
    return db_usuario
    
    