from fastapi import APIRouter, HTTPException,Form,Depends
from src.db import db
from src.models.models import FeedbackModel,FeedbackMode2
from bson import ObjectId
from typing import Optional
from datetime import datetime
from src.core.security import require_profesor,require_todos
router = APIRouter()

@router.get("/", response_model=list[FeedbackMode2])
async def get_feedback(user: dict = Depends(require_todos)):
    feedbacks = await db.feedback.find().to_list(100)
    for f in feedbacks:
        f["_id"] = str(f["_id"])
    return feedbacks

@router.get("/{feedback_id}", response_model=FeedbackModel)
async def get_feedback_by_id(feedback_id: str,user: dict = Depends(require_todos)):
    f = await db.feedback.find_one({"_id": ObjectId(feedback_id)})
    if not f:
        raise HTTPException(status_code=404, detail="Retroalimentación no encontrada")
    f["_id"] = str(f["_id"])
    return f

@router.post("/")
async def create_feedback(
    tarea_id: str =Form("",description="id de la tarea"),
    submission_id: str = Form("", description="id de la entrga"),
    comentario: Optional[str] = Form("", description=""),
    calificacion: Optional[float] = Form(0, description=""),
    user: dict = Depends(require_profesor)
):
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
    try:
        envio = await db.tasks.find_one({"entregas": submission_id})
    except:
        raise HTTPException(
            status_code=401,
            detail=f"La entrega no existe"
        )
    if not envio:
        raise HTTPException(
            status_code=401,
            detail=f"La entraga no existe"
        )
    profesor_id = user["username"] 
    feedback_dict = {
        "tarea_id": tarea_id,
        "submission_id": submission_id,
        "profesor_id": profesor_id,
        "comentario": comentario,
        "calificacion": calificacion,
        "fecha": datetime.utcnow()       
    }

    result = await db.feedback.insert_one(feedback_dict)
    feedback_dict["_id"] = str(result.inserted_id)
    feedback_id = str(result.inserted_id)
    update_result = await db.submissions.update_one(
        {"_id": ObjectId(submission_id)},
        {"$set": {"retroalimentacion_id": feedback_id}}
    )
    return feedback_dict

@router.put("/{feedback_id}")
async def update_feedback(
    feedback_id: str,
    submission_id: str = Form(..., description=""),
    
    comentario: Optional[str] = Form(None, description=""),
    calificacion: Optional[float] = Form(None, description=""),
    user: dict = Depends(require_profesor)
):
    try:
        tarea = await db.feedback.find_one({"_id": ObjectId(feedback_id)})
    except:
        raise HTTPException(
            status_code=401,
            detail=f"La retroalimentacion no existe"
        )
    if not tarea:
        raise HTTPException(
            status_code=401,
            detail=f"La retroalimentacion no existe"
        )
    try:
        envio = await db.tasks.find_one({"entregas": submission_id})
    except:
        raise HTTPException(
            status_code=401,
            detail=f"La entrega no existe"
        )
    if not envio:
        raise HTTPException(
            status_code=401,
            detail=f"La entraga no existe"
        )
    profesor_id = user["username"] 
    feedback_dict = {
        "submission_id": submission_id,
        "profesor_acualizo": profesor_id,
        "comentario": comentario,
        "calificacion": calificacion,
        "fecha": datetime.utcnow()    
    }

    result = await db.feedback.update_one(
        {"_id": ObjectId(feedback_id)},
        {"$set": feedback_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Retroalimentación no encontrada")

    return {"message": "Retroalimentación actualizada correctamente"}


@router.delete("/{feedback_id}")
async def delete_feedback(feedback_id: str,user: dict = Depends(require_profesor)):
    result = await db.feedback.delete_one({"_id": ObjectId(feedback_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Retroalimentación no encontrada")
    return {"message": "Retroalimentación eliminada correctamente"}


