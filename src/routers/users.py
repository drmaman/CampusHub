from src.models.models import UserModel, UserMode2
from fastapi import APIRouter, HTTPException, Form, Depends
from src.db import db
from bson import ObjectId
from typing import Literal
from datetime import datetime
from src.core.security import require_admin
router = APIRouter()

# Listar todos los usuarios
@router.get("/", response_model=list[UserMode2])
async def get_users():
    users = await db.users.find().to_list(100)
    for user in users:
        user["_id"] = str(user["_id"])
    return users

# Obtener usuario por ID
@router.get("/{user_id}", response_model=UserModel)
async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user["_id"] = str(user["_id"])
    return user


# Crear usuario desde FORM
@router.post("/")
async def create_user(
    nombre: str = Form(""),
    email: str = Form(""),
    password: str = Form(""),
    rol: Literal["estudiante","profesor","Administrador"] = Form(...),
    user: dict = Depends(require_admin)
):
    # Validar email único
    existing = await db["users"].find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    new_user = {
        "nombre": nombre,
        "email": email,
        "password": password,       
        "rol": rol,
        "creado_en": datetime.utcnow()   
    }

    result = await db["users"].insert_one(new_user)

    return {
        "message": "Usuario creado exitosamente",
        "id": str(result.inserted_id),
        "creado_en": new_user["creado_en"]  
    }
# Actualizar un usuario
@router.put("/{user_id}")
async def update_user(
    user_id: str,
    nombre: str = Form(""),
    email: str = Form(""),
    password: str = Form(""),
    rol: Literal["profesor", "estudiante","Administrador"] = Form(...),
    user: dict = Depends(require_admin)
):
    # Valores obligatorios–desde formulario
    user_dict = {
        "nombre": nombre,
        "email": email,
        "rol": rol,
        "actualizado_en": datetime.utcnow()   
    }

    # Solo guardar password si se envió (para no sobreescribir con None)
    if password is not None:
        user_dict["password"] = password

    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "message": "Usuario actualizado correctamente",
        "id": user_id,
        "actualizado_en": user_dict["actualizado_en"]
    }

# Eliminar un usuario
@router.delete("/{user_id}")
async def delete_user(user_id: str, user: dict = Depends(require_admin)):
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}

