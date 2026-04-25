from pydantic import BaseModel
from typing import Optional

class CarrinhoPublico(BaseModel):

    id: int
    id_usuario: int
    status: str
    desconto_total: float
    preco_total: float
    quantidade_produtos: int