from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Usuario
from fastapi import HTTPException, status
from core.seguranca import bcrypt_context
from core.seguranca import gerar_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

def login_form(usuario: OAuth2PasswordRequestForm, sessao: Session) -> dict:
    # Tenta pegar o usuário de acordo com o email
    db_usuario = sessao.scalar(
        select(Usuario).where(Usuario.email == usuario.username)
)
    # Verifica se o usuário foi encontrado
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Email ou senha incorretos'
)
    # Verifica se a senha está correta
    elif not bcrypt_context.verify(usuario.password, db_usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Email ou senha incorretos'
)
    # Cria o token de acesso 
    token_acesso = gerar_token(db_usuario.id)
    
    # Cria o token de atualização
    token_de_atualizacao = gerar_token(
        id_usuario=db_usuario.id, 
        duracao_do_token=timedelta(days=7)
)

    return {
        'access_token': token_acesso,
        'refresh_token': token_de_atualizacao,
        'token_type': 'Bearer'
}

def refresh(usuario: Usuario):
    # Cria o token de acesso
    token_acesso = gerar_token(usuario.id)

    return {
        'access_token': token_acesso,
        'token_type': 'Bearer'
    }

