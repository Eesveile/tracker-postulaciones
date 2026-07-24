# Tracker de Postulaciones

API REST para gestionar postulaciones a prácticas profesionales y trabajos, construida como proyecto de preparación para práctica profesional.

## Funcionalidades

- Registro y login de usuarios con autenticación JWT
- Contraseñas encriptadas con bcrypt
- CRUD completo de postulaciones (crear, listar, ver detalle, actualizar, eliminar)
- Filtro de postulaciones por estado
- Endpoint de estadísticas (conteo de postulaciones por estado)
- Cada usuario solo puede ver y modificar sus propias postulaciones

## Stack tecnológico

- Python 3.13
- FastAPI
- SQLAlchemy + SQLite
- Pydantic (validación de datos)
- JWT (python-jose) para autenticación
- Passlib + bcrypt para encriptar contraseñas

## Cómo correr el proyecto localmente

```bash
# Clonar el repositorio
git clone https://github.com/Eesveile/tracker-postulaciones.git
cd tracker-postulaciones

# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install fastapi uvicorn sqlalchemy "passlib[bcrypt]" "python-jose[cryptography]" python-multipart

# Correr el servidor
uvicorn main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`, con documentación interactiva en `http://127.0.0.1:8000/docs`.

## Endpoints principales

| Método | Ruta | Descripción | Requiere auth |
|--------|------|-------------|----------------|
| POST | /usuarios | Registrar usuario | No |
| POST | /login | Iniciar sesión | No |
| GET | /postulaciones | Listar postulaciones (filtro opcional por estado) | Sí |
| POST | /postulaciones | Crear postulación | Sí |
| GET | /postulaciones/{id} | Ver detalle | Sí |
| PUT | /postulaciones/{id} | Actualizar | Sí |
| DELETE | /postulaciones/{id} | Eliminar | Sí |
| GET | /postulaciones/stats/resumen | Estadísticas por estado | Sí |