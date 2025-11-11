from fastapi import Depends, HTTPException, status
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
async def get_current_user(token: str = Depends(auth_scheme)):
    try:
        # Decodificar el JWT
        payload = jwt.decode(token.credentials, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o incompleto",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Validar expiración del token
        #exp = payload.get("exp")
        #if exp and datetime.utcnow().timestamp() > exp:
        #    raise HTTPException(
        #        status_code=status.HTTP_401_UNAUTHORIZED,
        #        detail="El token ha expirado",
        #        headers={"WWW-Authenticate": "Bearer"},
        #    )

        return {"username": username, "role": role}

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

# Dependencia para verificar si el usuario es estudiante
async def require_estudiante(user: dict = Depends(get_current_user)):
    if user["role"] != "estudiante":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los estudiantes pueden acceder a este recurso"
        )
    return user
