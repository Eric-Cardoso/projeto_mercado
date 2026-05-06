from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencias import sessao, verificar_token
from models import Usuario
from schemas.schema_carrinho import ListarCarrinho
from services import carrinho_service

# Configurar a rota de carrinhos
carrinho_rota = APIRouter(prefix='/carrinho', tags=['carrinho'])


@carrinho_rota.get(
    path='/me', response_model=ListarCarrinho, status_code=status.HTTP_200_OK
)
def listar_carrinho(
    usuario: Usuario = Depends(verificar_token),
    sessao: Session = Depends(sessao),
    offset: int = 0,
    limit: int = 100,
) -> ListarCarrinho:

    return carrinho_service.listar_carrinho(
        usuario=usuario, sessao=sessao, offset=offset, limit=limit
    )


@carrinho_rota.patch(
    path='/me/cancelar',
    response_model=ListarCarrinho,
    status_code=status.HTTP_200_OK,
)
def cancelar_compra(
    usuario: Usuario = Depends(verificar_token),
    sessao: Session = Depends(sessao),
    offset: int = 0,
    limit: int = 100,
) -> ListarCarrinho:

    return carrinho_service.cancelar_compra(
        usuario=usuario, sessao=sessao, offset=offset, limit=limit
    )


@carrinho_rota.patch(
    path='/me/finalizar',
    response_model=ListarCarrinho,
    status_code=status.HTTP_200_OK,
)
def finalizar_compra(
    usuario: Usuario = Depends(verificar_token),
    sessao: Session = Depends(sessao),
    offset: int = 0,
    limit: int = 100,
) -> ListarCarrinho:

    return carrinho_service.finalizar_compra(
        usuario=usuario, sessao=sessao, offset=offset, limit=limit
    )
