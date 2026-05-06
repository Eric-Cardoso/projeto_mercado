from datetime import datetime, timezone

from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Carrinho, Produto, Usuario
from repos import repo_produtos
from schemas.schema_produto import AdicionarProduto, AtualizarProdutoParcial
from services.carrinho_service import solicitar_carrinho


def verificar_desconto(produto: Produto) -> None:
    # Verifica se o desconto é um valor nulo
    if produto.desconto is None:
        produto.desconto = 0


def aplicar_desconto(produto: Produto):
    # Pega o dia da semana
    dia_semana = datetime.weekday(datetime.now(timezone.utc))

    # Verifica se é segunda-feira e se a categoria do produto é refrigerados
    if dia_semana == 0 and produto.categoria == 'refrigerados':
        # Calcula o desconto
        produto.desconto = (produto.preco_unitario * 0.2) * produto.quantidade

    # Verifica se é terça-feira e se a categoria do produto é hortifruti
    elif dia_semana == 1 and produto.categoria == 'hortifruti':
        # Calcula o desconto
        produto.desconto = (produto.preco_unitario * 0.5) * produto.quantidade

    # Verifica se é quarta-feira e se a categoria do produto é açougue
    elif dia_semana == 2 and produto.categoria == 'açougue':
        # Calcula o desconto
        produto.desconto = (produto.preco_unitario * 0.3) * produto.quantidade

    # Verifica se é quinta-feira e se a categoria do produto é padaria
    elif dia_semana == 3 and produto.categoria == 'padaria':
        # Calcula o desconto
        produto.desconto = (produto.preco_unitario * 0.4) * produto.quantidade

    # Verifica se é sexta-feira e se a categoria do produto é bebidas
    elif dia_semana == 4 and produto.categoria == 'bebidas':
        # Calcula o desconto
        produto.desconto = (produto.preco_unitario * 0.5) * produto.quantidade

    # Verifica se é sabado
    elif dia_semana == 5:
        # Calcula o desconto
        produto.desconto = (produto.preco_unitario * 0.2) * produto.quantidade

    return produto


def adicionar_produto(
    dados: AdicionarProduto, usuario: Usuario, sessao: Session
) -> Produto:

    # Verifica se o usuário ja possui um carrinho
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == usuario.id)
    )

    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        db_carrinho = solicitar_carrinho(usuario=usuario, sessao=sessao)

    # Pega os dados em forma de dicionário
    db_dados = dados.model_dump(exclude_none=True)

    # Define a qual usuário o produto pertence
    db_dados['id_carrinho'] = db_carrinho.id

    # Pega os dados em forma de objeto
    db_produto = Produto(**db_dados)

    # Verifica se o desconto ta vindo nulo
    verificar_desconto(produto=db_produto)

    # Calcula o desconto do produto
    aplicar_desconto(produto=db_produto)

    # Adiciona o produto ao carrinho
    db_carrinho.produtos.append(db_produto)

    # Calcula o valor total do preço do produto
    db_carrinho.calcular_preco()

    # Calcula o valor total do desconto
    db_carrinho.calcular_desconto()

    # Adiciona os produtos ao banco e salva
    repo_produtos.adicionar(produto=db_produto, sessao=sessao)

    return db_produto


def listar_produtos(
    usuario: Usuario, sessao: Session, offset: int, limit: int
) -> list[dict]:

    # Tenta pegar o carrinho do usuário
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == usuario.id)
    )
    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum carrinho encontrado. '
            'Adicione um produto para criar um.',
        )

    # Pega todos os produtos existentes no banco
    db_produtos = sessao.scalars(
        select(Produto)
        .where(Produto.id_carrinho == db_carrinho.id)
        .offset(offset=offset)
        .limit(limit=limit)
    ).all()

    # Verifica se algum produto foi encontrado
    if not db_produtos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum produto encontrado',
        )
    return {'produtos': db_produtos}


def listar_produto(
    id_produto: int, usuario: Usuario, sessao: Session
) -> Produto:

    # Tenta pegar o carrinho do usuário
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == usuario.id)
    )
    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum carrinho encontrado. '
            'Adicione um produto para criar um.',
        )

    # Tenta pegar o produtos de acordo com seu id
    db_produto = sessao.scalar(select(Produto).where(Produto.id == id_produto))

    # Verifica se o produto foi encontrado
    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Produto não encontrado',
        )

    # Verifica se o produto é do usuário logado
    if db_produto.id_carrinho != db_carrinho.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Acesso negado'
        )
    return db_produto


def atualizar_produto(
    id_produto: int, dados: AdicionarProduto, usuario: Usuario, sessao: Session
) -> Produto:

    # Tenta pegar o carrinho do usuário
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == usuario.id)
    )
    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum carrinho encontrado. '
            'Adicione um produto para criar um.',
        )

    # Tenta pegar o produto de acordo com o id
    db_produto = sessao.scalar(select(Produto).where(Produto.id == id_produto))

    # Verifica se o produto foi encontrado
    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Produto não encontrado',
        )
    # Verifica se o produto pertence ao usuário logado
    if db_produto.id_carrinho != db_carrinho.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Acesso negado'
        )
    # Pega os dados em forma de dict
    db_dados = dados.model_dump()

    # Atualiza os dados do produto
    for campo, valor in db_dados.items():
        setattr(db_produto, campo, valor)

    # Calcula o desconto do produto
    aplicar_desconto(produto=db_produto)

    # Calcula o valor total do preço do produto
    db_carrinho.calcular_preco()

    # Calcula o valor total do desconto
    db_carrinho.calcular_desconto()

    # Atualiza os dados e salva
    repo_produtos.atualizar(produto=db_produto, sessao=sessao)

    return db_produto


def atualizar_produto_parcial(
    id_produto: int,
    dados: AtualizarProdutoParcial,
    usuario: Usuario,
    sessao: Session,
) -> Produto:

    # Tenta pegar o carrinho do usuário
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == usuario.id)
    )
    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum carrinho encontrado. '
            'Adicione um produto para criar um.',
        )

    # Tenta pegar o produto de acordo com o id
    db_produto = sessao.scalar(select(Produto).where(Produto.id == id_produto))
    # Verifica se o produto foi encontrado
    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Produto não encontrado',
        )
    # Verifica se o produto pertence ao usuário logado
    if db_produto.id_carrinho != db_carrinho.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Acesso negado'
        )

    # Pega os dados em forma de dict
    db_dados = dados.model_dump(exclude_unset=True)

    # Atualiza os dados do produto
    for campo, valor in db_dados.items():
        setattr(db_produto, campo, valor)

    # Calcula o desconto do produto
    aplicar_desconto(produto=db_produto)

    # Calcula o valor total do preço do produto
    db_carrinho.calcular_preco()

    # Calcula o valor total do desconto
    db_carrinho.calcular_desconto()

    # Atualiza os dados e salva
    repo_produtos.atualizar(produto=db_produto, sessao=sessao)

    return db_produto


def deletar_produto(
    id_produto: int, usuario: Usuario, sessao: Session
) -> Response:

    # Tenta pegar o carrinho do usuário
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == usuario.id)
    )
    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum carrinho encontrado. '
            'Adicione um produto para criar um.',
        )

    # Tenta pegar o produto de acordo com o id
    db_produto = sessao.scalar(select(Produto).where(Produto.id == id_produto))

    # Verifica se o produto foi encontrado
    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Produto não encontrado',
        )

    # Verifica se o produto pertence ao usuário logado
    if db_produto.id_carrinho != db_carrinho.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Acesso negado'
        )

    # Remove o produto do carrinho
    db_carrinho.produtos.remove(db_produto)

    # Deleta o produto
    sessao.delete(db_produto)

    # Calcula o valor total do preço do produto
    db_carrinho.calcular_preco()

    # Calcula o valor total do desconto
    db_carrinho.calcular_desconto()

    # Salva no banco
    sessao.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
