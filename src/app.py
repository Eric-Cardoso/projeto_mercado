from fastapi import FastAPI
from routers.auth_rotas import auth_rota
from routers.produtos_rotas import produtos_rota
from routers.usuarios_rotas import usuarios_rota
from routers.admin_rotas import admin_rota
from routers.carrinhos_rotas import carrinho_rota

# Configurar o app
app = FastAPI(
    title='projeto-mercado', 
    description='''
API REST de mercado para gerenciamento de produtos, 
construída com FastAPI, SQLite e Redis, implementando cache, filtros, 
paginação e otimização de desempenho.''',
    version='0.1.0'
)

# incluir as rotas no app
app.include_router(auth_rota)
app.include_router(produtos_rota)
app.include_router(usuarios_rota)
app.include_router(admin_rota)
app.include_router(carrinho_rota)

@app.get('/')
def home():
    return {'status': '200'}
