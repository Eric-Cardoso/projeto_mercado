from fastapi import APIRouter, status, Depends
from services import admin_service
from schemas import schema_usuario, schema_admin
from dependencias import sessao, verificar_token
from sqlalchemy.orm import Session
from models import Usuario

admin_rota = APIRouter(prefix='/admin', tags=['admin'])

@admin_rota.get(
    path='/usuarios', 
    response_model=schema_admin.UsuariosPublicos, 
    status_code=status.HTTP_200_OK
)
def obter_usuarios(
    usuario: Usuario = Depends(verificar_token), 
    offset: int = 0, 
    limit: int = 100, 
    sessao: Session = Depends(sessao)
) -> list[dict]:
    
    return admin_service.obter_usuarios(
        usuario=usuario,
        offset=offset, 
        limit=limit, 
        sessao=sessao
)

@admin_rota.get(
    path='/{id_usuario}', 
    response_model=schema_usuario.UsuarioPublico, 
    status_code=status.HTTP_200_OK
)
def obter_usuario(
    id_usuario: int, 
    usuario: Usuario = Depends(verificar_token),
    sessao: Session = Depends(sessao)
) -> Usuario:
    
    return admin_service.obter_usuario(
        id_usuario=id_usuario, 
        usuario=usuario, 
        sessao=sessao
)

@admin_rota.put(
    path='/{id_usuario}', 
    response_model=schema_admin.UsuarioPublico, 
    status_code=status.HTTP_201_CREATED
)
def atualizar_usuario(
    id_usuario: int, 
    dados: schema_admin.AtualizarUsuario,
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao)
) -> Usuario:
    
    return admin_service.atualizar_usuario(
        id_usuario=id_usuario, 
        usuario=usuario, 
        dados=dados, 
        sessao=sessao
)
