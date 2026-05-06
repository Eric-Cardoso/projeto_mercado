from sqlalchemy.orm import Session

from models import Carrinho


def criar(carrinho: Carrinho, sessao: Session) -> None:

    # Adiciona o carrinho ao banco
    sessao.add(carrinho)

    # Salva as alterações
    sessao.commit()

    # Atualiza o objeto
    sessao.refresh(carrinho)


def atualizar(carrinho: Carrinho, sessao: Session) -> None:

    # Salva as alterações
    sessao.commit()

    # Atualiza o objeto
    sessao.refresh(carrinho)
