from fastapi import APIRouter
from services.auth_criar import auth_criar
from models.models import Usuario
from fastapi import status, Depends
from schemas.usuario import UsuarioPublico, CriarUsuario
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
    
    return auth_criar(usuario=usuario, sessao=sessao)

