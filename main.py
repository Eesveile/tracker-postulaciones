from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from auth import crear_token
from auth import crear_token, obtener_usuario_actual
from fastapi.security import OAuth2PasswordRequestForm
from database import engine, Base, SessionLocal
from sqlalchemy import func
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def leer_raiz():
    return {"mensaje": "hola"}

@app.post("/usuarios", response_model=schemas.UsuarioRespuesta)
def crear_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Ese email ya está registrado")

    password_hasheada = pwd_context.hash(usuario.password)

    nuevo_usuario = models.Usuario(
        email=usuario.email,
        password_hash=password_hasheada,
        nombre=usuario.nombre
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario
@app.get("/usuarios", response_model=list[schemas.UsuarioRespuesta])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()

    if not usuario or not pwd_context.verify(form_data.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    token = crear_token({"sub": usuario.email})

    return {"access_token": token, "token_type": "bearer"}

@app.post("/postulaciones", response_model=schemas.PostulacionRespuesta)
def crear_postulacion(
    postulacion: schemas.PostulacionCrear,
    db: Session = Depends(get_db),
    email_actual: str = Depends(obtener_usuario_actual)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email_actual).first()

    nueva_postulacion = models.Postulacion(
        **postulacion.dict(),
        usuario_id=usuario.id
    )
    db.add(nueva_postulacion)
    db.commit()
    db.refresh(nueva_postulacion)

    return nueva_postulacion


@app.get("/postulaciones", response_model=list[schemas.PostulacionRespuesta])
def listar_postulaciones(
    estado: str | None = None,
    db: Session = Depends(get_db),
    email_actual: str = Depends(obtener_usuario_actual)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email_actual).first()

    query = db.query(models.Postulacion).filter(models.Postulacion.usuario_id == usuario.id)

    if estado:
        query = query.filter(models.Postulacion.estado == estado)

    return query.all()

@app.get("/postulaciones/{postulacion_id}", response_model=schemas.PostulacionRespuesta)
def ver_postulacion(
    postulacion_id: int,
    db: Session = Depends(get_db),
    email_actual: str = Depends(obtener_usuario_actual)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email_actual).first()

    postulacion = db.query(models.Postulacion).filter(
        models.Postulacion.id == postulacion_id,
        models.Postulacion.usuario_id == usuario.id
    ).first()

    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")

    return postulacion


@app.put("/postulaciones/{postulacion_id}", response_model=schemas.PostulacionRespuesta)
def actualizar_postulacion(
    postulacion_id: int,
    cambios: schemas.PostulacionActualizar,
    db: Session = Depends(get_db),
    email_actual: str = Depends(obtener_usuario_actual)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email_actual).first()

    postulacion = db.query(models.Postulacion).filter(
        models.Postulacion.id == postulacion_id,
        models.Postulacion.usuario_id == usuario.id
    ).first()

    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")

    for campo, valor in cambios.dict(exclude_unset=True).items():
        setattr(postulacion, campo, valor)

    db.commit()
    db.refresh(postulacion)

    return postulacion


@app.delete("/postulaciones/{postulacion_id}")
def eliminar_postulacion(
    postulacion_id: int,
    db: Session = Depends(get_db),
    email_actual: str = Depends(obtener_usuario_actual)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email_actual).first()

    postulacion = db.query(models.Postulacion).filter(
        models.Postulacion.id == postulacion_id,
        models.Postulacion.usuario_id == usuario.id
    ).first()

    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")

    db.delete(postulacion)
    db.commit()

    return {"mensaje": "Postulación eliminada"}

@app.get("/postulaciones/stats/resumen")
def estadisticas_postulaciones(
    db: Session = Depends(get_db),
    email_actual: str = Depends(obtener_usuario_actual)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email_actual).first()

    resultados = (
        db.query(models.Postulacion.estado, func.count(models.Postulacion.id))
        .filter(models.Postulacion.usuario_id == usuario.id)
        .group_by(models.Postulacion.estado)
        .all()
    )

    return {estado: cantidad for estado, cantidad in resultados}