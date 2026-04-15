from fastapi import APIRouter
from services import auth_service
from models import Usuario
from fastapi import status, Depends
from schemas.schema_auth import (
    LoginUsuario, 
    TokenPublico, 
    TokenForm, 
    TokenRefresh
)
from dependencias import sessao, verificar_token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

# Configurar a rota de autenticação
auth_rota = APIRouter(prefix='/auth', tags=['auth'])

@auth_rota.get('/')
def auth_principal():
    return {'status': '200, tudo certo com as rotas'}

@auth_rota.post(
        path='/login', 
        response_model=TokenPublico, 
        status_code=status.HTTP_200_OK
)
def login(usuario: LoginUsuario, sessao: Session = Depends(sessao)) -> dict:
    return auth_service.login(usuario=usuario, sessao=sessao)

@auth_rota.post(
    path='/login-form', 
    response_model=TokenForm, 
    status_code=status.HTTP_200_OK
)
def login_form(
    usuario: OAuth2PasswordRequestForm = Depends(), 
    sessao: Session = Depends(sessao)
) -> dict:
    return auth_service.login_form(usuario=usuario, sessao=sessao)

@auth_rota.get(
    path='/refresh', 
    response_model=TokenRefresh, 
    status_code=status.HTTP_200_OK
)
def refresh(usuario: Usuario = Depends(verificar_token)) -> dict:
    return auth_service.refresh(usuario=usuario)
