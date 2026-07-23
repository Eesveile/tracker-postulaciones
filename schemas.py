from pydantic import BaseModel
from typing import Optional

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

class UsuarioLogin(BaseModel):
    email: str
    password: str

class PostulacionCrear(BaseModel):
    empresa: str
    cargo: str
    estado: str = "postulado"
    fecha_postulacion: str
    link_oferta: Optional[str] = None
    notas: Optional[str] = None

class PostulacionRespuesta(BaseModel):
    id: int
    usuario_id: int
    empresa: str
    cargo: str
    estado: str
    fecha_postulacion: str
    link_oferta: Optional[str]
    notas: Optional[str]

    class Config:
        from_attributes = True

class PostulacionActualizar(BaseModel):
    empresa: Optional[str] = None
    cargo: Optional[str] = None
    estado: Optional[str] = None
    fecha_postulacion: Optional[str] = None
    link_oferta: Optional[str] = None
    notas: Optional[str] = None