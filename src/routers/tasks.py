from fastapi import APIRouter, HTTPException, Form, Depends
from src.db import db
from bson import ObjectId
from datetime import datetime
from typing import Optional, List
from src.models.models import TaskModel, TaskMode2
from src.core.security import require_profesor,require_todos

router = APIRouter()

# Obtener todas las tareas
@router.get("/", response_model=list[TaskMode2])
async def get_tasks(user: dict = Depends(require_todos)):
    tasks = await db.tasks.find().to_list(100)
    for t in tasks:
        t["_id"] = str(t["_id"])
    return tasks

# Obtener una tarea específica por ID
@router.get("/{task_id}", response_model=TaskModel)
async def get_task(task_id: str,user: dict = Depends(require_todos)):
    t = await db.tasks.find_one({"_id": ObjectId(task_id)})
    if not t:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    t["_id"] = str(t["_id"])
    return t

# Crear una nueva tarea
@router.post("/")
async def create_task(
    titulo: str = Form("", description="Título de la tarea"),
    descripcion: Optional[str] = Form("", description="Descripción de la tarea"),
    curso_id: str = Form("", description="ID del curso al que pertenece"),
    fecha_limite: Optional[datetime] = Form(..., description="Fecha límite (YYYY-MM-DD)"),
    entregas: Optional[List[str]] = Form([]),
    user: dict = Depends(require_profesor)
):
    try:
        curso = await db.courses.find_one({"_id": ObjectId(curso_id)})
    except:
        raise HTTPException(
            status_code=401,
            detail=f"El curso no existe"
        )
    if not curso:
        raise HTTPException(
            status_code=401,
            detail=f"El curso no existe"
        )
    estado="activa"
    task_dict = {
        "titulo": titulo,
        "descripcion": descripcion,
        "curso_id": curso_id,
        "fecha_limite": fecha_limite,
        "estado": estado,
        "entregas":entregas,
        "fecha_creacion": datetime.utcnow()
    }

    result = await db.tasks.insert_one(task_dict)
    task_dict["_id"] = str(result.inserted_id)
    task_id = str(result.inserted_id)
    update_result = await db.courses.update_one(
        {"_id": ObjectId(curso_id)},
        {"$push": {"tareas": task_id}}
    )
    return task_dict

# Actualizar una tarea existente
@router.put("/{task_id}")
async def update_task(
    task_id: str,
    titulo: str = Form("", description="Título de la tarea"),
    descripcion: Optional[str] = Form("", description="Descripción de la tarea"),
    curso_id: str = Form("", description="ID del curso al que pertenece"),
    fecha_limite: Optional[str] = Form("", description="Fecha límite (YYYY-MM-DD)"),
    entregas: Optional[List[str]] = Form([]),
    user: dict = Depends(require_profesor)

):
    try:
        curso = await db.courses.find_one({"_id": ObjectId(curso_id)})
    except:
        raise HTTPException(
            status_code=401,
            detail=f"El curso no existe"
        )
    if not curso:
        raise HTTPException(
            status_code=401,
            detail=f"El curso no existe"
        )
    estado="activa"
    task_dict = {
        "titulo": titulo,
        "descripcion": descripcion,
        "curso_id": curso_id,
        "fecha_limite": fecha_limite,
        "estado": estado,
        "entregas":entregas,
        "fecha_actualizacion": datetime.utcnow()
    }

    result = await db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    return {"message": "Tarea actualizada correctamente"}

# Eliminar tarea
@router.delete("/{task_id}")
async def delete_task(task_id: str, user: dict = Depends(require_profesor)):
    result = await db.tasks.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada correctamente"}

