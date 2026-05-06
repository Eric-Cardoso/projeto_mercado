from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CriarUsuario(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=3)
    email: EmailStr
    senha: str


class UsuarioPublico(BaseModel):
    id: int
    nome: Optional[str] = None
    email: str
    senha: str


class AtualizarUsuario(BaseModel):
    nome: str = Field(..., min_length=3)
