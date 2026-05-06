from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from password_strength import PasswordPolicy

from core.configuracoes import ALGORITMO, CHAVE_SECRETA, TEMPO_EXPIRACAO_TOKEN

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')


def validar_senha(senha: str) -> None:
    # Configura os requisitos para a senha ser válida
    policy = PasswordPolicy.from_names(
        length=8, uppercase=1, numbers=1, special=1
    )
    # Coleta os erros que a senha possa ter
    erros = policy.test(senha)

    # Verifica se a senha contém erros
    if erros:
        # levanta uma exceção caso a senha tenha erros
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                'mensagem': 'Senha inválida',
                'requisitos': [
                    'mínimo de 8 caracteres',
                    '1 letra maiúscula',
                    '1 número',
                    '1 caractere especial',
                ],
            },
        )


def gerar_token(
    id_usuario: int,
    duracao_do_token: timedelta = timedelta(minutes=TEMPO_EXPIRACAO_TOKEN),
) -> str:
    # Pega a data atual e calcula a duração do token
    # de acordo com o tempo de expiração passado
    tempo_expiracao = datetime.now(timezone.utc) + duracao_do_token

    # Cria o dicionário com as informações que o token vai ter
    dict_info = {'sub': str(id_usuario), 'exp': tempo_expiracao}

    # Codifica o token
    token = jwt.encode(dict_info, CHAVE_SECRETA, ALGORITMO)

    return token
