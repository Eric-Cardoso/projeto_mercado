from pydantic import BaseModel
from schemas.schema_usuario import UsuarioPublico

class UsuariosPublicos(BaseModel):
    usuarios: list[UsuarioPublico]