from fastapi import FastAPI

app = FastAPI(
    title='projeto-mercado', 
    description='''
API REST de mercado para gerenciamento de produtos, 
construída com FastAPI, SQLite e Redis, implementando cache, filtros, 
paginação e otimização de desempenho.''',
    version='0.1.0'
)

@app.get('/')
def home():
    return {'status': '200'}
