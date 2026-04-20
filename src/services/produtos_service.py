from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Usuario, Produtos
from repos import repo_produtos
from schemas.schema_produto import AdicionarProduto

def adicionar_produto(
        dados: AdicionarProduto, 
        usuario: Usuario, 
        sessao: Session
) -> Produtos:
    
    # Pega os dados em forma de dicionário
    db_dados = dados.model_dump()

    # Define a qual usuário o produto pertence
    db_dados['id_usuario'] = usuario.id

    # Pega os dados em forma de objeto
    db_produto = Produtos(**db_dados)

    # Adiciona o produto ao banco e salva
    repo_produtos.adicionar(produto=db_produto, sessao=sessao)

    return db_produto

def listar_produto(
        id_produto: int, 
        usuario: Usuario, 
        sessao: Session
) -> Produtos:
      
      db_produto = sessao.scalar(
        select(Produtos).where(Produtos.id == id_produto)
)
      
      if not db_produto: 
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND, 
               detail='Produto não encontrado'
)
      if db_produto.id_usuario != usuario.id:
           raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Acesso negado'
)
      return db_produto


