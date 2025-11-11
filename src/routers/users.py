from fastapi import APIRouter, HTTPException
from src.db import db
from src.models.models import UserModel
from bson import ObjectId

router = APIRouter()

# Listar todos los usuarios
@router.get("/", response_model=list[UserModel])
async def get_users():
    users = await db.users.find().to_list(100)
    for user in users:
        user["_id"] = str(user["_id"])
    return users

# Obtener un usuario por ID
@router.get("/{user_id}", response_model=UserModel)
async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user["_id"] = str(user["_id"])
    return user

# Crear un usuario
@router.post("/")
async def create_user(user: UserModel):
    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    new_user = user.dict()
    await db["users"].insert_one(new_user)
    return {"message": "Usuario creado exitosamente", "id": str(new_user["_id"]) if "_id" in new_user else None}
# Actualizar un usuario
@router.put("/{user_id}")
async def update_user(user_id: str, user: UserModel):
    user_dict = user.model_dump(by_alias=True, exclude=["id"])
    result = await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario actualizado correctamente"}

# Eliminar un usuario
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}
