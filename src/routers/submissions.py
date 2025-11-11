from fastapi import APIRouter, HTTPException
from src.db import db
from src.models.models import SubmissionModel
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=list[SubmissionModel])
async def get_submissions():
    submissions = await db.submissions.find().to_list(100)
    for s in submissions:
        s["_id"] = str(s["_id"])
    return submissions

@router.get("/{submission_id}", response_model=SubmissionModel)
async def get_submission(submission_id: str):
    s = await db.submissions.find_one({"_id": ObjectId(submission_id)})
    if not s:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    s["_id"] = str(s["_id"])
    return s

@router.post("/", response_model=SubmissionModel)
async def create_submission(submission: SubmissionModel):
    submission_dict = submission.model_dump(by_alias=True, exclude=["id"])
    result = await db.submissions.insert_one(submission_dict)
    submission_dict["_id"] = str(result.inserted_id)
    return submission_dict

@router.put("/{submission_id}")
async def update_submission(submission_id: str, submission: SubmissionModel):
    submission_dict = submission.model_dump(by_alias=True, exclude=["id"])
    result = await db.submissions.update_one({"_id": ObjectId(submission_id)}, {"$set": submission_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return {"message": "Entrega actualizada correctamente"}

@router.delete("/{submission_id}")
async def delete_submission(submission_id: str):
    result = await db.submissions.delete_one({"_id": ObjectId(submission_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return {"message": "Entrega eliminada correctamente"}
