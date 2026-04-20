from sqlalchemy.orm import Session
from models import Usuario, Produtos
from repos import repo_produtos
from schemas.schema_produto import AdicionarProduto

def adicionar_produto(
        dados: AdicionarProduto, 
        usuario: Usuario, 
        sessao: Session
):
    
    # Pega os dados em forma de dicionário
    db_dados = dados.model_dump()

    # Define a qual usuário o produto pertence
    db_dados['id_usuario'] = usuario.id

    # Pega os dados em forma de objeto
    db_produto = Produtos(**db_dados)

    # Adiciona o produto ao banco e salva
    repo_produtos.adicionar(produto=db_produto, sessao=sessao)

    return db_produto





