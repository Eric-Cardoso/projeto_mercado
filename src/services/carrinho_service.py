from sqlalchemy.orm import Session
from models import Usuario, Carrinho
from repos import repo_carrinho

def solicitar_carrinho(usuario: Usuario, sessao: Session):

    # Cria um carrinho para o usuário logado
    db_carrinho = Carrinho(id_usuario = usuario.id)

    # Adiciona o carrinho ao banco e salva
    repo_carrinho.criar(carrinho=db_carrinho, sessao=sessao)

    return db_carrinho
