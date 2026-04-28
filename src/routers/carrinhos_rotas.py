from fastapi import APIRouter, status, Depends
from schemas.schema_carrinho import ListarCarrinho
from models import Usuario
from dependencias import verificar_token, sessao
from sqlalchemy.orm import Session
from services import carrinho_service

carrinho_rota = APIRouter(prefix='/carrinho', tags=['carrinho'])

@carrinho_rota.get(
        path='/me', 
        response_model=ListarCarrinho, 
        status_code=status.HTTP_200_OK
    )
def listar_carrinho(
        usuario: Usuario = Depends(verificar_token), 
        sessao: Session = Depends(sessao), 
        offset: int = 0, 
        limit: int = 100
    ) -> ListarCarrinho:

    return carrinho_service.listar_carrinho(
        usuario=usuario, 
        sessao=sessao, 
        offset=offset,
        limit=limit
    )

@carrinho_rota.get(
        path='/me/cancelar', 
        response_model=ListarCarrinho, 
        status_code=status.HTTP_200_OK
    )
def cancelar_compra(
        usuario: Usuario = Depends(verificar_token),
        sessao: Session = Depends(sessao), 
        offset: int = 0, 
        limit: int = 100
    ):

    return carrinho_service.cancelar_compra(
        usuario=usuario, 
        sessao=sessao, 
        offset=offset, 
        limit=limit
    )