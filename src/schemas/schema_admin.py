from typing import Optional

from pydantic import BaseModel

from schemas.schema_usuario import UsuarioPublico


class UsuariosPublicos(BaseModel):
    usuarios: list[UsuarioPublico]


class AtualizarUsuario(BaseModel):
    ativo: Optional[bool] = True
    admin: Optional[bool] = False


class UsuarioPublico(BaseModel):
    id: int
    nome: Optional[str] = None
    email: str
    senha: str
    ativo: bool
    admin: bool


class AtualizarProduto(BaseModel):
    categoria: Optional[str] = None
    preco_unitario: Optional[float] = None
    desconto: Optional[float] = None
