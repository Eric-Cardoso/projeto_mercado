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

def listar_produtos(
        usuario: Usuario, 
        sessao: Session, 
        offset: int, 
        limit: int
) -> list[dict]:
     
    # Pega todos os produtos existentes no banco
     db_produtos = sessao.scalars(
        select(Produtos)
        .where(Produtos.id_usuario == usuario.id)
        .offset(offset=offset)
        .limit(limit=limit)
).all()
     
     # Verifica se algum produto foi encontrado
     if not db_produtos:
        raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND, 
               detail='Nenhum produto encontrado'
)
     return {'produtos': db_produtos}


def listar_produto(
        id_produto: int, 
        usuario: Usuario, 
        sessao: Session
) -> Produtos:
      
      # Tenta pegar o produtos de acordo com seu id
      db_produto = sessao.scalar(
          select(Produtos).where(Produtos.id == id_produto)
)
      
      # Verifica se o produto foi encontrado
      if not db_produto: 
          raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Produto não encontrado'
)
      
      # Verifica se o produto é do usuário logado
      if db_produto.id_usuario != usuario.id:
          raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Acesso negado'
)
      return db_produto

def atualizar_produto(
        id_produto: int, 
        dados: AdicionarProduto, 
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
    db_dados = dados.model_dump()

    for campo, valor in db_dados.items():
        setattr(db_produto, campo, valor)

    repo_produtos.atualizar(produto=db_produto, sessao=sessao) 

    return db_produto                                   



