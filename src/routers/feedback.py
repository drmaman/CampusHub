from fastapi import APIRouter, HTTPException
from src.db import db
from src.models.models import FeedbackModel
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=list[FeedbackModel])
async def get_feedback():
    feedbacks = await db.feedback.find().to_list(100)
    for f in feedbacks:
        f["_id"] = str(f["_id"])
    return feedbacks

@router.get("/{feedback_id}", response_model=FeedbackModel)
async def get_feedback_by_id(feedback_id: str):
    f = await db.feedback.find_one({"_id": ObjectId(feedback_id)})
    if not f:
        raise HTTPException(status_code=404, detail="Retroalimentación no encontrada")
    f["_id"] = str(f["_id"])
    return f

@router.post("/", response_model=FeedbackModel)
async def create_feedback(feedback: FeedbackModel):
    feedback_dict = feedback.model_dump(by_alias=True, exclude=["id"])
    result = await db.feedback.insert_one(feedback_dict)
    feedback_dict["_id"] = str(result.inserted_id)
    return feedback_dict

@router.put("/{feedback_id}")
async def update_feedback(feedback_id: str, feedback: FeedbackModel):
    feedback_dict = feedback.model_dump(by_alias=True, exclude=["id"])
    result = await db.feedback.update_one({"_id": ObjectId(feedback_id)}, {"$set": feedback_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Retroalimentación no encontrada")
    return {"message": "Retroalimentación actualizada correctamente"}

@router.delete("/{feedback_id}")
async def delete_feedback(feedback_id: str):
    result = await db.feedback.delete_one({"_id": ObjectId(feedback_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Retroalimentación no encontrada")
    return {"message": "Retroalimentación eliminada correctamente"}
