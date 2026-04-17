from pydantic import BaseModel
from typing import Optional
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