from fastapi import APIRouter, HTTPException, Depends
from src.db import db
from src.models.models import CourseModel
from bson import ObjectId
from src.core.security import require_profesor, get_current_user  # 👈 importar seguridad

router = APIRouter()

# ✅ Todos pueden ver los cursos
@router.get("/", response_model=list[CourseModel])
async def get_courses():
    courses = await db.courses.find().to_list(100)
    for course in courses:
        course["_id"] = str(course["_id"])
    return courses

# ✅ Todos pueden ver un curso específico
@router.get("/{course_id}", response_model=CourseModel)
async def get_course(course_id: str):
    course = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    course["_id"] = str(course["_id"])
    return course

# ✅ Solo profesores pueden crear cursos
@router.post("/", response_model=CourseModel)
async def create_course(course: CourseModel, user: dict = Depends(require_profesor)):
    course_dict = course.model_dump(by_alias=True, exclude=["id"])
    result = await db.courses.insert_one(course_dict)
    course_dict["_id"] = str(result.inserted_id)
    return course_dict

# ✅ Solo profesores pueden actualizar cursos
@router.put("/{course_id}")
async def update_course(course_id: str, course: CourseModel, user: dict = Depends(require_profesor)):
    course_dict = course.model_dump(by_alias=True, exclude=["id"])
    result = await db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": course_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"message": "Curso actualizado correctamente"}

# ✅ Solo profesores pueden eliminar cursos
@router.delete("/{course_id}")
async def delete_course(course_id: str, user: dict = Depends(require_profesor)):
    result = await db.courses.delete_one({"_id": ObjectId(course_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"message": "Curso eliminado correctamente"}
