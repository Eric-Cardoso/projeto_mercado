from pydantic import BaseModel
from schemas.schema_produto import ProdutoPublico

class CarrinhoPublico(BaseModel):

    id: int
    id_usuario: int
    status: str
    desconto_total: float
    preco_total: float
    quantidade_produtos: int

class ListarCarrinho(BaseModel):
    carrinho: CarrinhoPublico
    produtos: list[ProdutoPublico]