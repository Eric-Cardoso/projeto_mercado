from fastapi import APIRouter, status, Depends, Response
from services import produtos_service
from schemas import schema_usuario, schema_admin
from dependencias import sessao, verificar_token
from sqlalchemy.orm import Session
from models import Usuario
from schemas.schema_produto import ProdutoPublico, AdicionarProduto


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
):
    
    return produtos_service.adicionar_produto(
        dados=dados, 
        usuario=usuario, 
        sessao=sessao
)
