from pydantic import BaseModel

class UsuarioCrear(BaseModel):
    email: str
    password: str
    nombre: str

class UsuarioRespuesta(BaseModel):
    id: int
    email: str
    nombre: str

    class Config:
        from_attributes = True