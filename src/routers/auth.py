from fastapi import APIRouter, HTTPException, Request
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os
from src.db import db
from src.models.models import LoginRequest, LoginResponse  # 👈 importar modelos

router = APIRouter()

# Configuración JWT
SECRET = os.getenv("JWT_SECRET", "supersecreto")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = 2

# Cifrado de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


@router.post("/", response_model=LoginResponse)
async def login(credentials: LoginRequest, request: Request):
    """
    Inicia sesión con email y contraseña.
    Retorna token JWT + nombre + rol + id del usuario.
    """
    # Buscar usuario
    user = await db.users.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Validar contraseña (puedes cambiar a verify_password si usas hash)
    if credentials.password != user["password"]:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Crear el token
    token_data = {"sub": str(user["_id"]), "role": user["rol"], "email": user["email"]}
    token = create_access_token(token_data)

    # Respuesta del modelo
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        nombre=user["nombre"],
        rol=user["rol"],
        _id=str(user["_id"])
    )
