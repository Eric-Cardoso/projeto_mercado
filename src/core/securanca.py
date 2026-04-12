from core.configuracoes import SECRET_KEY
from passlib.context import CryptContext
from password_strength import PasswordPolicy
from fastapi import HTTPException, status 

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def validar_senha(senha: str) -> None:
    # Configura os requisitos para a senha ser válida
    policy = PasswordPolicy.from_names(
        length=8,  
        uppercase=1, 
        numbers=1, 
        special=1  
)
    # Coleta os erros que a senha possa ter
    erros = policy.test(senha)

    # Verifica se a senha contém erros
    if erros:
        # levanta uma exceção caso a senha tenha erros
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail={'mensagem': 'Senha inválida',
                    'requisitos' : [
                'mínimo de 8 caracteres',
                '1 letra maiúscula',
                '1 número',
                '1 caractere especial'
                ]
            }
        )

    return 
