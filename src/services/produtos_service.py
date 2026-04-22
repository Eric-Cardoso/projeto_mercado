from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Usuario, Produto
from repos import repo_produtos
from schemas.schema_produto import AdicionarProduto, AtualizarProdutoParcial

def adicionar_produto(
        dados: AdicionarProduto, 
        usuario: Usuario, 
        sessao: Session
) -> Produto:
    
    # Pega os dados em forma de dicionário
    db_dados = dados.model_dump()

    # Define a qual usuário o produto pertence
    db_dados['id_carrinho'] = usuario.id

    # Pega os dados em forma de objeto
    db_produto = Produto(**db_dados)

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
        select(Produto)
        .where(Produto.id_carrinho == usuario.id)
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
) -> Produto:
      
      # Tenta pegar o produtos de acordo com seu id
      db_produto = sessao.scalar(
          select(Produto).where(Produto.id == id_produto)
)
      
      # Verifica se o produto foi encontrado
      if not db_produto: 
          raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Produto não encontrado'
)
      
      # Verifica se o produto é do usuário logado
      if db_produto.id_carrinho != usuario.id:
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
) -> Produto:
    
    # Tenta pegar o produto de acordo com o id
    db_produto = sessao.scalar(
        select(Produto).where(Produto.id == id_produto)
)
    
    # Verifica se o produto foi encontrado
    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Produto não encontrado'
)
    # Verifica se o produto pertence ao usuário logado
    if db_produto.id_carrinho != usuario.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
)
    # Pega os dados em forma de dict
    db_dados = dados.model_dump()

    # Atualiza os dados do produto
    for campo, valor in db_dados.items():
        setattr(db_produto, campo, valor)

    # Atualiza os dados e salva
    repo_produtos.atualizar(produto=db_produto, sessao=sessao) 

    return db_produto 

def atualizar_produto_parcial(
        id_produto: int, 
        dados: AtualizarProdutoParcial, 
        usuario: Usuario, 
        sessao: Session
) -> Produto:
    
    db_produto = sessao.scalar(
        select(Produto).where(Produto.id == id_produto)
)
    # Verifica se o produto foi encontrado
    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Produto não encontrado'
)
    # Verifica se o produto pertence ao usuário logado
    if db_produto.id_carrinho != usuario.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
)
    
    # Pega os daods em forma de dict
    db_dados = dados.model_dump(exclude_unset=True)

    # Atualiza os dados do produto
    for campo, valor in db_dados.items():
        setattr(db_produto, campo, valor)

    # Atualiza os dados e salva
    repo_produtos.atualizar(produto=db_produto, sessao=sessao)

    return db_produto



