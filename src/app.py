from fastapi import FastAPI

from routers.admin_rotas import admin_rota
from routers.auth_rotas import auth_rota
from routers.carrinhos_rotas import carrinho_rota
from routers.produtos_rotas import produtos_rota
from routers.usuarios_rotas import usuarios_rota

# Configurar o app
app = FastAPI(
    title='projeto-mercado',
    description="""
api rest para gerenciamento de produtos de mercado, 
desenvolvida com fastapi e sqlite, com autenticação jwt, hash de senhas
e validação de força de senha com password_strength, 
além de paginação e controle de acesso por usuário.""",
    version='0.1.0',
)

# incluir as rotas no app
app.include_router(auth_rota)
app.include_router(produtos_rota)
app.include_router(usuarios_rota)
app.include_router(admin_rota)
app.include_router(carrinho_rota)


@app.get('/')
def home():
    return {'status': 'ok'}
