from fastapi import APIRouter, status, Depends, Response
from services import admin_service
from schemas import (
    schema_usuario, 
    schema_admin, 
    schema_produto, 
    schema_carrinho
)
from dependencias import sessao, verificar_token
from sqlalchemy.orm import Session
from models import Usuario, Produto

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
    path='/usuarios/{id_usuario}/produtos', 
    response_model=schema_produto.ListarProdutos, 
    status_code=status.HTTP_200_OK
)
def listar_produtos(
    id_usuario: int, 
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao), 
    offset: int = 0, 
    limit: int = 100
) -> list[schema_produto.ListarProdutos]:
    
    return admin_service.listar_produtos(
        id_usuario=id_usuario, 
        usuario=usuario, 
        sessao=sessao, 
        offset=offset, 
        limit=limit
    )


@admin_rota.get(
    path='/usuarios/{id_usuario}', 
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


@admin_rota.patch(
    path='/usuarios/{id_usuario}/carrinho/cancelar', 
    response_model=schema_carrinho.ListarCarrinho, 
    status_code=status.HTTP_200_OK
)
def cancelar_compra(
    id_usuario: int, 
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao), 
    offset: int = 0, 
    limit: int = 100
) -> schema_carrinho.ListarCarrinho:

    return admin_service.cancelar_compra(
        id_usuario=id_usuario, 
        usuario=usuario, 
        sessao=sessao, 
        offset=offset, 
        limit=limit
    )


@admin_rota.get(
    path='/usuarios/{id_usuario}/carrinho', 
    response_model=schema_carrinho.ListarCarrinho, 
    status_code=status.HTTP_200_OK
)
def listar_carrinho(
    id_usuario: int, 
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao), 
    offset: int = 0, 
    limit: int = 100
) -> schema_carrinho.ListarCarrinho:

    return admin_service.listar_carrinho(
        id_usuario=id_usuario, 
        usuario=usuario, 
        sessao=sessao, 
        offset=offset, 
        limit=limit
    )


@admin_rota.get(
    path='/usuarios/{id_usuario}/produtos/{id_produto}', 
    response_model=schema_produto.ProdutoPublico, 
    status_code=status.HTTP_200_OK
)
def listar_produto(
    id_usuario: int, 
    id_produto: int,
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao)
) -> Produto:
    
    return admin_service.listar_produto(
        id_usuario=id_usuario, 
        id_produto=id_produto, 
        usuario=usuario, 
        sessao=sessao
    )


@admin_rota.put(
    path='/usuarios/{id_usuario}', 
    response_model=schema_admin.UsuarioPublico, 
    status_code=status.HTTP_200_OK
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


@admin_rota.patch(
    path='/usuarios/{id_usuario}/produtos/{id_produto}', 
    response_model=schema_produto.ProdutoPublico, 
    status_code=status.HTTP_200_OK
)
def atualizar_produto(
    id_usuario: int, 
    id_produto: int, 
    dados: schema_admin.AtualizarProduto, 
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao)
) -> schema_produto.ProdutoPublico:

    return admin_service.atualizar_produto(
        id_usuario=id_usuario, 
        id_produto=id_produto, 
        usuario=usuario, 
        dados=dados, 
        sessao=sessao
    )


@admin_rota.delete(
    path='/usuarios/{id_usuario}/produtos/{id_produto}', 
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_produto(
    id_usuario: int, 
    id_produto: int, 
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao)
) -> Response:
    
    return admin_service.deletar_produto(
        id_usuario=id_usuario, 
        id_produto=id_produto, 
        usuario=usuario, 
        sessao=sessao
    )


@admin_rota.delete(
    path='/usuarios/{id_usuario}', 
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_usuario(
    id_usuario: int, 
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao)
) -> Response:
    
    return admin_service.deletar_usuario(
        id_usuario=id_usuario, 
        usuario=usuario, 
        sessao=sessao
)