from pydantic import BaseModel, EmailStr

class LoginUsuario(BaseModel):
    email: EmailStr
    senha: str

class TokenPublico(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenForm(BaseModel):
    access_token: str
    token_type: str

class TokenRefresh(BaseModel):
    access_token: str
    token_type: str