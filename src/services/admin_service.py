from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Usuario
from schemas.schema_admin import AtualizarUsuario
from repos import repo_usuario

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

def obter_usuarios(
        usuario: Usuario, 
        sessao: Session, 
        offset: int, 
        limit: int
) -> list[dict]:
    
    # Pega todos os usuários existentes no banco
    db_usuarios = sessao.scalars(
        select(Usuario).offset(offset=offset).limit(limit=limit)
).all()
    
    # Verifica se o usuário é um admin
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
)

    # Verifica se os usuários foram encontrados
    if not db_usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuários não encontrados'
)
    
    return {'usuarios': db_usuarios}

def atualizar_usuario(
        id_usuario: int, 
        dados: AtualizarUsuario, 
        usuario: Usuario, 
        sessao: Session
) -> Usuario:
    
    # Verifica se o usuário é um admin
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
)
    
    # Tenta pegar o usuário de acordo com o id
    db_usuario = sessao.scalar(select(Usuario).where(Usuario.id == id_usuario))

    # Verifica se o usuário foi encontrado
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado'
)
    
    # Altera o valor do campo ativo
    db_usuario.ativo = dados.ativo
    
    # Altera o valor do campo admin
    db_usuario.admin = dados.admin

    # Atualiza os dados do usuário e salva 
    repo_usuario.atualizar(usuario=db_usuario, sessao=sessao)

    return db_usuario




    

    
    
    
    