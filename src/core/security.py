from fastapi import Depends, HTTPException, status,Request
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from datetime import datetime
import os

# Configuración del token
SECRET = os.getenv("JWT_SECRET", "supersecreto")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Middleware de autenticación HTTP Bearer
auth_scheme = HTTPBearer()

# Dependencia para obtener el usuario actual
async def get_current_user(request: Request):
    token = None

    # ✅ Primero intenta leer cookie
    if "access_token" in request.cookies:
        token = request.cookies.get("access_token")
    else:
        # ✅ Fallback: header Authorization
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return {
            "username": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role")
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o no autorizado",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependencia para verificar si el usuario es profesor
async def require_profesor(user: dict = Depends(get_current_user)):
    if user["role"] != "profesor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los profesores pueden acceder a este recurso"
        )
    return user
async def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "Administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden acceder a este recurso"
        )
    return user

# Dependencia para verificar si el usuario es estudiante
async def require_estudiante(user: dict = Depends(get_current_user)):
    if user["role"] != "estudiante":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los estudiantes pueden acceder a este recurso"
        )
    return user
