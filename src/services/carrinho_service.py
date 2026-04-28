from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Usuario, Carrinho, Produto
from repos import repo_carrinho
from schemas.schema_carrinho import ListarCarrinho

def solicitar_carrinho(usuario: Usuario, sessao: Session) -> Carrinho:

    # Cria um carrinho para o usuário logado
    db_carrinho = Carrinho(id_usuario = usuario.id)

    # Adiciona o carrinho ao banco e salva
    repo_carrinho.criar(carrinho=db_carrinho, sessao=sessao)

    return db_carrinho

def listar_carrinho(
        usuario: Usuario, 
        sessao: Session, 
        offset: int, 
        limit: int
    ) -> ListarCarrinho:
    
    # Tenta pegar o carrinho do usuario logado
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == usuario.id)
    )

    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Carrinho não encontrado. Adicione um produto para criar um.'
        )
    
    # Pega todos os produtos existentes no banco
    db_produtos = sessao.scalars(
        select(Produto)
        .where(Produto.id_carrinho == db_carrinho.id)
        .offset(offset=offset)
        .limit(limit=limit)
    ).all()
    
    # Quantidade de produtos que tem no carrinho
    db_carrinho.quantidade_produtos = len(db_produtos)
    
    return {
        'carrinho': db_carrinho,
        'produtos': db_produtos
    }

def cancelar_compra(
        usuario: Usuario, 
        sessao: Session, 
        offset: int, 
        limit: int
    ) -> ListarCarrinho:
    
    # Tenta pegar o carrinho do usuario logado
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == usuario.id)
    )

    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Carrinho não encontrado. Adicione um produto para criar um.'
        )
    
    # Pega todos os produtos existentes no banco
    db_produtos = sessao.scalars(
        select(Produto)
        .where(Produto.id_carrinho == db_carrinho.id)
        .offset(offset=offset)
        .limit(limit=limit)
    ).all()
    
    # Quantidade de produtos que tem no carrinho
    db_carrinho.quantidade_produtos = len(db_produtos)

    # Muda o status do carrinho para cancelado
    db_carrinho.status = 'CANCELADO'

    # Atualiza o status do carrinho e salva
    repo_carrinho.atualizar(carrinho=db_carrinho, sessao=sessao)
    
    return {
        'carrinho': db_carrinho,
        'produtos': db_produtos
    }

def finalizar_compra(
        usuario: Usuario, 
        sessao: Session, 
        offset: int, 
        limit: int
    ) -> ListarCarrinho:
    
    # Tenta pegar o carrinho do usuario logado
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == usuario.id)
    )

    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Carrinho não encontrado. Adicione um produto para criar um.'
        )
    
    # Pega todos os produtos existentes no banco
    db_produtos = sessao.scalars(
        select(Produto)
        .where(Produto.id_carrinho == db_carrinho.id)
        .offset(offset=offset)
        .limit(limit=limit)
    ).all()
    
    # Quantidade de produtos que tem no carrinho
    db_carrinho.quantidade_produtos = len(db_produtos)

    # Muda o status do carrinho para finalizado
    db_carrinho.status = 'FINALIZADO'

    # Atualiza o status do carrinho e salva
    repo_carrinho.atualizar(carrinho=db_carrinho, sessao=sessao)
    
    return {
        'carrinho': db_carrinho,
        'produtos': db_produtos
    }