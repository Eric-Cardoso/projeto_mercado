from fastapi import APIRouter
from services import usuario_service
from models import Usuario
from fastapi import status, Depends
from schemas.schema_usuario import UsuarioPublico, CriarUsuario
from dependencias import sessao, verificar_token
from sqlalchemy.orm import Session

usuarios_rota = APIRouter(prefix='/usuarios', tags=['usuários'])

@usuarios_rota.post(
        path='/registrar', 
        response_model=UsuarioPublico, 
        status_code=status.HTTP_201_CREATED
)
def criar_usuario(
    usuario: CriarUsuario, 
    sessao: Session = Depends(sessao)
) -> Usuario:
    
    return usuario_service.criar_usuario(usuario=usuario, sessao=sessao)

@usuarios_rota.get(
    path='/eu', 
    response_model=UsuarioPublico, 
    status_code=status.HTTP_200_OK
)
def obter_usuario(
    usuario: Usuario = Depends(verificar_token),  
    sessao: Session = Depends(sessao)
) -> Usuario:
    return usuario_service.obter_usuario(usuario=usuario, sessao=sessao)