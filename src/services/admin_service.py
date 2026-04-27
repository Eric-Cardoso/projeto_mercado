from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from models import Usuario, Carrinho, Produto
from schemas import schema_admin, schema_produto
from repos import repo_usuario, repo_produtos

def obter_usuario(
        id_usuario: int, 
        usuario: Usuario,  
        sessao: Session
) -> Usuario:
    
    # Tenta pegar o usuário de acordo com o id
    db_usuario = sessao.scalar(select(Usuario).where(Usuario.id == id_usuario))

    # Verifica se o usuário é admin
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
)
    # Verifica se o usuário foi encontrado
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado'
)
    
    return db_usuario

def obter_usuarios(
        usuario: Usuario, 
        sessao: Session, 
        offset: int, 
        limit: int
) -> list[dict]:
    
    # Pega todos os usuários existentes no banco
    db_usuarios = sessao.scalars(
        select(Usuario).offset(offset=offset).limit(limit=limit)
).all()
    
    # Verifica se o usuário é um admin
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
)

    # Verifica se os usuários foram encontrados
    if not db_usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuários não encontrados'
)
    
    return {'usuarios': db_usuarios}

def atualizar_usuario(
        id_usuario: int, 
        dados: schema_admin.AtualizarUsuario, 
        usuario: Usuario, 
        sessao: Session
) -> Usuario:
    
    # Verifica se o usuário é um admin
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
)
    
    # Tenta pegar o usuário de acordo com o id
    db_usuario = sessao.scalar(select(Usuario).where(Usuario.id == id_usuario))

    # Verifica se o usuário foi encontrado
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado'
)
    
    # Altera o valor do campo ativo
    db_usuario.ativo = dados.ativo
    
    # Altera o valor do campo admin
    db_usuario.admin = dados.admin

    # Atualiza os dados do usuário e salva 
    repo_usuario.atualizar(usuario=db_usuario, sessao=sessao)

    return db_usuario

def deletar_usuario(
        id_usuario: int, 
        usuario: Usuario, 
        sessao: Session
) -> Response:

    # Verifica se o usuário é um admin
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
)
    
    # Tenta pegar o usuário de acordo com o id
    db_usuario = sessao.scalar(select(Usuario).where(Usuario.id == id_usuario))

    # Verifica se o usuário foi encontrado
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Usuário não encontrado'
)
    # Deleta o usuário e salva
    repo_usuario.deletar(usuario=db_usuario, sessao=sessao)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

def listar_produto(
        id_usuario: int,
        id_produto: int,
        usuario: Usuario, 
        sessao: Session
) -> Produto:
    
    # Verifica se o usuário logado é admin
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
        )
    
    # Tenta pegar o usuário através do id
    db_usuario = sessao.scalar(select(Usuario).where(Usuario.id == id_usuario))

    # Verifica se o usuário foi encontrado
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Usuário não encontrado'
)
    # Tenta pegar o carrinho do usuário
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == db_usuario.id)
)
    
    # Tenta pegar o produto no carrinho do usuário de acordo com o id
    db_produto = sessao.scalar(
        select(Produto).where(Produto.id == id_produto)
)
    # Verifica se o carrinho ou o produto foi encontrado
    if not db_carrinho or not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Nenhum produto encontrado'
)
    return db_produto

def listar_produtos(
        id_usuario: int, 
        usuario: Usuario, 
        sessao: Session, 
        offset: int, 
        limit: int
    ) -> schema_produto.ListarProdutos:

    # Verifica se o usuário logado é admin
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
)
    
    # Tenta pegar o usuário através do id
    db_usuario = sessao.scalar(select(Usuario).where(Usuario.id == id_usuario))

    # Verifica se o usuário foi encontrado
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Usuário não encontrado'
)
    # Tenta pegar o carrinho do usuário
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == db_usuario.id))
    
    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Carrinho não encontrado'
        )
    
    # Pega todos os produtos daquele usuário
    db_produtos = sessao.scalars(
        select(Produto)
        .where(Produto.id_carrinho == db_carrinho.id)
        .offset(offset=offset)
        .limit(limit=limit)
    ).all()

    # Verifica se os produtos foram encontrados
    if not db_produtos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Nenhum produto encontrado'
        )
    
    return {
        'produtos': db_produtos
    }

def atualizar_produto(
        id_usuario: int, 
        id_produto: int,
        dados: schema_admin.AtualizarProduto,
        usuario: Usuario, 
        sessao: Session
    ) -> schema_produto.ProdutoPublico:

    # Verifica se o usuário logado é admin
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Acesso negado'
        )
    
    # Tenta pegar o usuário através do id
    db_usuario = sessao.scalar(select(Usuario).where(Usuario.id == id_usuario))

    # Verifica se o usuário foi encontrado
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Usuário não encontrado'
        )
    
    # Tenta pegar o carrinho do usuário
    db_carrinho = sessao.scalar(
        select(Carrinho).where(Carrinho.id_usuario == db_usuario.id)
    )
    
    # Verifica se o carrinho foi encontrado
    if not db_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Carrinho não encontrado'
        )
    
    # Tenta pegar o produto do usuário através do id
    db_produto = sessao.scalar(
        select(Produto).where(Produto.id == id_produto)
    )

    # Verifica se o produto foi encontrado
    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Produto não encontrado'
        )
    
    # Pega os dados em forma de dict
    db_dados = dados.model_dump(exclude_unset=True)

    # Atualiza os dados do produto
    for campo, valor in db_dados.items():
        setattr(db_produto, campo, valor)

    # Calcula o valor total do preço do produto
    db_carrinho.calcular_preco()

    # Calcula o valor total do desconto
    db_carrinho.calcular_desconto()
    
    # Atualiza os dados e salva
    repo_produtos.atualizar(produto=db_produto, sessao=sessao)

    return db_produto
    
    



    

    
    
    
    