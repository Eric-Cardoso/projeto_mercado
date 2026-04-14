from fastapi import APIRouter
from services import usuario_service, auth_service
from models import Usuario
from fastapi import status, Depends
from schemas.schema_usuario import UsuarioPublico, CriarUsuario
from schemas.schema_auth import LoginUsuario, TokenPublico
from dependencias import sessao
from sqlalchemy.orm import Session

# Configurar a rota de autenticação
auth_rota = APIRouter(prefix='/auth', tags=['auth'])

@auth_rota.get('/')
def auth_principal():
    return {'status': '200, tudo certo com as rotas'}

@auth_rota.post(
        path='/registrar', 
        response_model=UsuarioPublico, 
        status_code=status.HTTP_201_CREATED
)
def criar_usuario(
    usuario: CriarUsuario, 
    sessao: Session = Depends(sessao)
) -> Usuario:
    
    return usuario_service.criar_usuario(usuario=usuario, sessao=sessao)

@auth_rota.post(
        path='/login', 
        response_model=TokenPublico, 
        status_code=status.HTTP_200_OK
)
def login(usuario: LoginUsuario, sessao: Session = Depends(sessao)) -> dict:
    return auth_service.login(usuario=usuario, sessao=sessao)

