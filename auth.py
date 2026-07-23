from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "cambia-esto-por-algo-secreto-y-largo-despues"
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60

def crear_token(datos: dict):
    datos_a_codificar = datos.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=EXPIRACION_MINUTOS)
    datos_a_codificar.update({"exp": expiracion})
    token = jwt.encode(datos_a_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token