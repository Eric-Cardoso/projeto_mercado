from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from dependencias import sessao, verificar_token
from models import Usuario
from schemas.schema_usuario import (
    AtualizarUsuario,
    CriarUsuario,
    UsuarioPublico,
)
from services import usuario_service

# Configurar a rota de usuarios
usuarios_rota = APIRouter(prefix='/usuarios', tags=['usuários'])


@usuarios_rota.post(
    path='/registrar',
    response_model=UsuarioPublico,
    status_code=status.HTTP_201_CREATED,
)
def criar_usuario(
    usuario: CriarUsuario, sessao: Session = Depends(sessao)
) -> Usuario:

    return usuario_service.criar_usuario(usuario=usuario, sessao=sessao)


@usuarios_rota.get(
    path='/me', response_model=UsuarioPublico, status_code=status.HTTP_200_OK
)
def obter_usuario(
    usuario: Usuario = Depends(verificar_token),
    sessao: Session = Depends(sessao),
) -> Usuario:

    return usuario_service.obter_usuario(usuario=usuario, sessao=sessao)


@usuarios_rota.patch(
    path='/me', response_model=UsuarioPublico, status_code=status.HTTP_200_OK
)
def atualizar_usuario(
    dados: AtualizarUsuario,
    usuario: Usuario = Depends(verificar_token),
    sessao: Session = Depends(sessao),
) -> Usuario:

    return usuario_service.atualizar_dados(
        dados=dados, usuario=usuario, sessao=sessao
    )


@usuarios_rota.delete(path='/me', status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(
    usuario: Usuario = Depends(verificar_token),
    sessao: Session = Depends(sessao),
) -> Response:

    return usuario_service.deletar_usuario(usuario=usuario, sessao=sessao)
