from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.configuracoes import ALGORITMO, CHAVE_SECRETA, Sessionlocal
from core.seguranca import oauth2_schema
from models import Usuario


# Empresta a sessao do banco de dados sempre que necessário
def sessao():
    sessao_local = Sessionlocal()
    try:
        yield sessao_local
    finally:
        sessao_local.close()


def verificar_token(
    token: str = Depends(oauth2_schema), sessao: Session = Depends(sessao)
) -> Usuario:
    try:
        # Descodifica o token
        dict_info = jwt.decode(token, CHAVE_SECRETA, ALGORITMO)

        # Pega o id do usuário
        id_usuario = int(dict_info.get('sub'))

        # Tenta pegar o usuário de acordo com o id
        db_usuario = sessao.scalar(
            select(Usuario).where(Usuario.id == id_usuario)
        )
        # Verifica se o usuário foi encontrado
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Usuário não encontrado',
            )
        return db_usuario

    # Caso ocorra algum erro ao descodificar o token, será levantada uma exceção
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email ou senha incorretos',
        )
