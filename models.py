from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import ForeignKey

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    nombre = Column(String)

class Postulacion(Base):
    __tablename__ = "postulaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    empresa = Column(String)
    cargo = Column(String)
    estado = Column(String, default="postulado")
    fecha_postulacion = Column(String)
    link_oferta = Column(String, nullable=True)
    notas = Column(String, nullable=True)