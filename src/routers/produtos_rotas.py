from fastapi import APIRouter

# Configurar a rota de produtos
produtos_rota = APIRouter(prefix='/produtos', tags=['produtos'])

@produtos_rota.get('/')
def produtos_principal():
    return {'status': 'produtos ok'}