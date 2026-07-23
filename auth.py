from datetime import datetime, timedelta
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

SECRET_KEY = "cambia-esto-por-algo-secreto-y-largo-despues"
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60

def crear_token(datos: dict):
    datos_a_codificar = datos.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=EXPIRACION_MINUTOS)
    datos_a_codificar.update({"exp": expiracion})
    token = jwt.encode(datos_a_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la credencial",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credenciales_invalidas
        return email
    except JWTError:
        raise credenciales_invalidas