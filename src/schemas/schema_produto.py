from typing import Optional

from pydantic import BaseModel


class AdicionarProduto(BaseModel):
    nome: str
    quantidade: int
    categoria: str
    preco_unitario: float


class ProdutoPublico(BaseModel):
    id: int
    id_carrinho: int
    nome: str
    quantidade: int
    categoria: str
    preco_unitario: float
    desconto: float


class ListarProdutos(BaseModel):
    produtos: list[ProdutoPublico]


class AtualizarProdutoParcial(BaseModel):
    nome: Optional[str] = None
    quantidade: Optional[int] = None
    categoria: Optional[str] = None
    preco_unitario: Optional[float] = None
