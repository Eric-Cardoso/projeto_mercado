from schemas.schema_usuario import CriarUsuario
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Usuario
from core.seguranca import bcrypt_context, validar_senha
from repos.repo_usuario import criar

def criar_usuario(
        usuario: CriarUsuario, sessao: Session
) -> Usuario:
    
    # Verifica se ja existe um usuário com o mesmo email no banco
    db_usuario = sessao.scalar(
        select(Usuario).where(Usuario.email == usuario.email)
)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail='Já existe um usuário com este email.'
)
    # Pega os dados do usuário
    dados = usuario.model_dump()

    # Valida a senha
    validar_senha(senha=dados['senha'])

    # Criptografa a senha
    dados['senha'] = bcrypt_context.hash(dados['senha'])

    # Pega o usuário
    db_usuario = Usuario(**dados)

    # Adiciona o usuário ao banco e salva
    criar(usuario=db_usuario, sessao=sessao)

    return db_usuario


    
