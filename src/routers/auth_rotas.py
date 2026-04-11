from fastapi import APIRouter

# Configurar a rota de autenticação
auth_rota = APIRouter(prefix='/auth', tags=['auth'])

@auth_rota.get('/')
def auth_principal():
    return {'status': '200, tudo certo com as rotas'}