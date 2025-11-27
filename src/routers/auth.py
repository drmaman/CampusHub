from fastapi import APIRouter, HTTPException, Request, Form,Response
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os
from src.db import db
from src.models.models import LoginResponse

router = APIRouter()

SECRET = os.getenv("JWT_SECRET", "supersecreto")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = 2

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


@router.post("/", response_model=LoginResponse)
async def login(
    response: Response,
    email: str = Form(""),
    password: str = Form("")
):
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if password != user["password"]:  # usa verify_password si ocupas hash
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token_data = {"sub": str(user["_id"]), "role": user["rol"], "email": user["email"]}
    token = create_access_token(token_data)

    # ✅ Guardar token en cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,      # pon True si usas HTTPS
        samesite="lax",
        max_age=7200
    )

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        nombre=user["nombre"],
        rol=user["rol"],
        id=str(user["_id"])
    )
@router.post("/logout")
async def logout(response: Response):
    # ✅ borrar cookie del token
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,   # pon True si usas HTTPS
        samesite="lax"
    )

    return {"message": "Logout exitoso"}
