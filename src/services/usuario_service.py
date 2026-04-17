from schemas.schema_usuario import CriarUsuario
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from models import Usuario
from core.seguranca import bcrypt_context, validar_senha
from repos import repo_usuario
from schemas.schema_usuario import AtualizarUsuario

def criar_usuario(
        usuario: CriarUsuario, sessao: Session
) -> Usuario:
    
    # Verifica se ja existe um usuário com o mesmo email no banco
    db_usuario = sessao.scalar(
        select(Usuario).where(Usuario.email == usuario.email)
)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail='Já existe um usuário com este email.'
)
    # Pega os dados do usuário
    dados = usuario.model_dump()

    # Valida a senha
    validar_senha(senha=dados['senha'])

    # Criptografa a senha
    dados['senha'] = bcrypt_context.hash(dados['senha'])

    # Pega o usuário
    db_usuario = Usuario(**dados)

    # Adiciona o usuário ao banco e salva
    repo_usuario.criar(usuario=db_usuario, sessao=sessao)

    return db_usuario

def obter_usuario(usuario: Usuario, sessao: Session) -> Usuario:
    # Tenta pegar o usuário de acordo com o id
    db_usuario = sessao.scalar(select(Usuario).where(Usuario.id == usuario.id))

    # Verifica se o usuário existe
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Credencias inválidas'
)
    
    return db_usuario

def atualizar_dados(
        dados: AtualizarUsuario, 
        usuario: Usuario,
        sessao: Session
) -> Usuario:
    
    # Pega os dados em forma de dicionário
    dict_dados = dados.model_dump()
    
    # Verifica se os dados estão vazios
    if not dict_dados:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credencial inválido'
)
    # Atualiza os dados
    for campo, valor in dict_dados.items():
        setattr(usuario, campo, valor)
    
    # Atualiza os dados e salva
    repo_usuario.atualizar(usuario=usuario, sessao=sessao)
    
    return usuario

def deletar_usuario(usuario: Usuario, sessao: Session) -> Response:
    
    # Deleta o usuário do banco e salva
    repo_usuario.deletar(usuario=usuario, sessao=sessao)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
