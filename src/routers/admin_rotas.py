from fastapi import APIRouter, status, Depends
from services import admin_service
from schemas.schema_usuario import UsuarioPublico 
from dependencias import sessao, verificar_token
from sqlalchemy.orm import Session
from models import Usuario


admin_rota = APIRouter(prefix='/admin', tags=['admin'])

@admin_rota.get(
    path='/{id_usuario}', 
    response_model=UsuarioPublico, 
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