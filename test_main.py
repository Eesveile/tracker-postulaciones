import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base
import main

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[main.get_db] = override_get_db


@pytest.fixture(autouse=True)
def preparar_base_de_datos():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_registro_usuario():
    respuesta = client.post("/usuarios", json={
        "email": "test@ejemplo.com",
        "password": "clave123",
        "nombre": "Test"
    })
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["email"] == "test@ejemplo.com"
    assert "password" not in datos


def test_no_permite_email_duplicado():
    client.post("/usuarios", json={
        "email": "test@ejemplo.com",
        "password": "clave123",
        "nombre": "Test"
    })
    respuesta = client.post("/usuarios", json={
        "email": "test@ejemplo.com",
        "password": "otraclave",
        "nombre": "Test2"
    })
    assert respuesta.status_code == 400


def test_login_correcto():
    client.post("/usuarios", json={
        "email": "test@ejemplo.com",
        "password": "clave123",
        "nombre": "Test"
    })
    respuesta = client.post("/login", data={
        "username": "test@ejemplo.com",
        "password": "clave123"
    })
    assert respuesta.status_code == 200
    assert "access_token" in respuesta.json()


def test_login_password_incorrecta():
    client.post("/usuarios", json={
        "email": "test@ejemplo.com",
        "password": "clave123",
        "nombre": "Test"
    })
    respuesta = client.post("/login", data={
        "username": "test@ejemplo.com",
        "password": "claveincorrecta"
    })
    assert respuesta.status_code == 401


def test_no_puede_crear_postulacion_sin_token():
    respuesta = client.post("/postulaciones", json={
        "empresa": "Falabella",
        "cargo": "Practicante",
        "fecha_postulacion": "2026-07-23"
    })
    assert respuesta.status_code == 401


def test_crear_y_listar_postulacion_con_token():
    client.post("/usuarios", json={
        "email": "test@ejemplo.com",
        "password": "clave123",
        "nombre": "Test"
    })
    login = client.post("/login", data={
        "username": "test@ejemplo.com",
        "password": "clave123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    respuesta_crear = client.post("/postulaciones", json={
        "empresa": "Falabella",
        "cargo": "Practicante",
        "fecha_postulacion": "2026-07-23"
    }, headers=headers)
    assert respuesta_crear.status_code == 200

    respuesta_listar = client.get("/postulaciones", headers=headers)
    assert respuesta_listar.status_code == 200
    assert len(respuesta_listar.json()) == 1