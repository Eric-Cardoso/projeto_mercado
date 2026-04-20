from fastapi import APIRouter, status, Depends
from services import produtos_service
from dependencias import sessao, verificar_token
from sqlalchemy.orm import Session
from models import Usuario, Produtos
from schemas.schema_produto import (
    ProdutoPublico, 
    AdicionarProduto, 
    ListarProdutos
)


# Configurar a rota de produtos
produtos_rota = APIRouter(prefix='/produtos', tags=['produtos'])

@produtos_rota.get('/')
def produtos_principal():
    return {'status': 'produtos ok'}

@produtos_rota.post(
    path='/adicionar', 
    response_model=ProdutoPublico, 
    status_code=status.HTTP_201_CREATED
)
def adicionar_produto(
    dados: AdicionarProduto,
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao)
) -> Produtos:
    
    return produtos_service.adicionar_produto(
        dados=dados, 
        usuario=usuario, 
        sessao=sessao
)

@produtos_rota.get(
    path='/me', 
    response_model=ListarProdutos, 
    status_code=status.HTTP_200_OK
)
def listar_produtos(
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session =  Depends(sessao),
    offset: int = 0,
    limit: int = 100
) -> list[dict]:
    
    return produtos_service.listar_produtos(
        usuario=usuario, 
        sessao=sessao, 
        offset=offset, 
        limit=limit
)

@produtos_rota.get(
    path='/{id_produto}', 
    response_model=ProdutoPublico, 
    status_code=status.HTTP_200_OK
)
def listar_produto(
    id_produto: int, 
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao)
) -> Produtos:
    
    return produtos_service.listar_produto(
        id_produto=id_produto, 
        usuario=usuario, 
        sessao=sessao
)

@produtos_rota.put(
    path='/{id_produto}', 
    response_model=ProdutoPublico, 
    status_code=status.HTTP_200_OK
)
def atualizar_produto(
    id_produto: int, 
    dados: AdicionarProduto, 
    usuario: Usuario = Depends(verificar_token), 
    sessao: Session = Depends(sessao)
):
    
    return produtos_service.atualizar_produto(
        dados=dados, 
        id_produto=id_produto, 
        usuario=usuario, 
        sessao=sessao
)



