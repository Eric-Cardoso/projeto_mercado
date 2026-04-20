from pydantic import BaseModel
from typing import Optional

class AdicionarProduto(BaseModel):
    
    nome: str
    quantidade: int
    categoria: str
    preco_unitario: float

class ProdutoPublico(BaseModel):
    
    id: int
    id_usuario: int
    nome: str
    quantidade: int
    categoria: str
    preco_unitario: float