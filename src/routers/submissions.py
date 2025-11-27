from fastapi import APIRouter, HTTPException, Form,Depends
from src.db import db
from src.models.models import SubmissionModel,SubmissionMode2
from bson import ObjectId
from datetime import datetime
from typing import Optional
from src.core.security import require_estudiante

router = APIRouter()

@router.get("/", response_model=list[SubmissionMode2])
async def get_submissions():
    submissions = await db.submissions.find().to_list(100)
    for s in submissions:
        s["_id"] = str(s["_id"])
    return submissions

@router.get("/{submission_id}")
async def get_submission(submission_id: str):
    s = await db.submissions.find_one({"_id": ObjectId(submission_id)})
    if not s:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    s["_id"] = str(s["_id"])
    return s

@router.post("/")
async def create_submission(
    titulo: str = Form("", description=""),
    descripcion: Optional[str] = Form("", description=""),
    curso_id: str = Form("", description="id de la tarea"),
    tarea_id: str = Form("", description=""),
    archivo_url: Optional[str] = Form("", description=""),
    retroalimentacion_id: Optional[str] = Form("", description=""),
    user: dict = Depends(require_estudiante)
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
    
    
    try:
        tarea = await db.courses.find_one({"tareas": tarea_id})
    except:
        raise HTTPException(
            status_code=401,
            detail=f"La tarea no existe"
        )
    if not tarea:
        raise HTTPException(
            status_code=401,
            detail=f"La tarea no existe"
        )
    autor_id = user["username"]  
    autor_email = user["email"]
    autor = await db.users.find_one({"_id": ObjectId(autor_id)})
    autor_nombre = autor["nombre"]
    autor_in="email: "+autor_email+", nombre: "+autor_nombre+", id: "+autor_id
    estado="enviado"
    retroalimentacion_id = retroalimentacion_id.strip()
    if retroalimentacion_id == "":
        retroalimentacion_id = None
    submission_dict = {
        "titulo": titulo,
        "descripcion": descripcion,
        "curso_id": curso_id,
        "tarea_id": tarea_id,
        "estudiante": autor_in,
        "archivo_url": archivo_url,
        "estado": estado,
        "retroalimentacion_id": retroalimentacion_id,
        "fecha_entrega": datetime.utcnow()                    
    }

    result = await db.submissions.insert_one(submission_dict)
    submission_dict["_id"] = str(result.inserted_id)
    entrega_id = str(result.inserted_id)
    update_result = await db.tasks.update_one(
        {"_id": ObjectId(tarea_id)},
        {"$push": {"entregas": entrega_id}}
    )
    return submission_dict


@router.put("/{submission_id}")
async def update_submission(
    submission_id: str,
    titulo: str = Form("", description=""),
    descripcion: Optional[str] = Form("", description=""),
    curso_id: str = Form("", description="id de la tarea"),
    tarea_id: str = Form("", description="id de la tarea"),
    archivo_url: Optional[str] = Form("", description=""),
    retroalimentacion_id: Optional[str] = Form("", description=""),
    user: dict = Depends(require_estudiante)
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
    try:
        tarea = await db.courses.find_one({"tareas": tarea_id})
    except:
        raise HTTPException(
            status_code=401,
            detail=f"La tarea no existe"
        )
    if not tarea:
        raise HTTPException(
            status_code=401,
            detail=f"La tarea no existe"
        )
    estado="enviado"
    submission_dict = {
        "titulo": titulo,
        "descripcion": descripcion,
        "curso_id": curso_id,
        "tarea_id": tarea_id,
        "archivo_url": archivo_url,
        "estado": estado,
        "retroalimentacion_id": retroalimentacion_id,
        "fecha_actualizacion": datetime.utcnow()     # actualizamos fecha
    }

    result = await db.submissions.update_one(
        {"_id": ObjectId(submission_id)},
        {"$set": submission_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")

    return {"message": "Entrega actualizada correctamente"}


@router.delete("/{submission_id}")
async def delete_submission(submission_id: str,user: dict = Depends(require_estudiante)):
    result = await db.submissions.delete_one({"_id": ObjectId(submission_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return {"message": "Entrega eliminada correctamente"}
