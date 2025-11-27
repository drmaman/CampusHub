from fastapi import APIRouter, HTTPException, Depends, Form
from src.db import db
from src.models.models import CourseModel, CourseMode2
from bson import ObjectId
from src.core.security import require_profesor, require_admin
from typing import Optional, List
from datetime import datetime
router = APIRouter()

# Todos pueden ver los cursos
@router.get("/", response_model=list[CourseMode2])
async def get_courses():
    courses = await db.courses.find().to_list(100)
    for course in courses:
        course["_id"] = str(course["_id"])
    return courses

#  Todos pueden ver un curso específico
@router.get("/{course_id}", response_model=CourseModel)
async def get_course(course_id: str):
    course = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    course["_id"] = str(course["_id"])
    return course

#  Solo profesores pueden crear cursos
@router.post("/", response_model=CourseModel)
async def create_course(
    nombre: str = Form("",description="nombre del curso"),
    descripcion: Optional[str] = Form(""),
    max_estudiantes: int = Form(1),
    estudiantes: Optional[List[str]] = Form(default=[]),
    equipos: Optional[List[str]] = Form([]),
    tareas: Optional[List[str]] = Form([]),
    user: dict = Depends(require_profesor)
):
    profesor_id = user["username"]  
    profesor_email = user["email"]
    profesor = await db.users.find_one({"_id": ObjectId(profesor_id)})
    profesor_nombre = profesor["nombre"]

    
    
    estudiantes_id = []
    for email in estudiantes:
        email_list = [e.strip() for e in email.split(",") if e.strip()]

    duplicados = [email for email in email_list if email_list.count(email) > 1]
    if duplicados:
        raise HTTPException(
            status_code=400,
            detail=f"Estudiantes repetidos: {', '.join(set(duplicados))}"
        )

    for email in email_list:
        estudiante = await db.users.find_one({"email": email, "rol": "estudiante"})
        if not estudiante:
            raise HTTPException(
                status_code=404,
                detail=f"El estudiante con email {email} no existe"
            )
        estudiantes_id.append("mail: "+str(email)+", nombre: "+str(estudiante["nombre"])+", id: "+str(estudiante["_id"]))
         
    total_estudiantes = len(estudiantes_id)
    
    if total_estudiantes>max_estudiantes:
        raise HTTPException(
            status_code=400,
            detail=f"los estudiantes exeden la cantidad maxima"
        )

    course_dict = {
        "nombre": nombre,
        "descripcion": descripcion,
        "profesor_id": profesor_id,
        "profesor_nombre": profesor_nombre,
        "profesor_email": profesor_email,
        "estudiantes": estudiantes_id,
        "equipos": equipos,
        "tareas": tareas,
        "max_estudiantes": max_estudiantes,
        "total_estudiantes": total_estudiantes,
        "fecha_creacion": datetime.utcnow(),
    }

    result = await db.courses.insert_one(course_dict)
    course_dict["_id"] = str(result.inserted_id)
    return course_dict

#  Solo profesores pueden actualizar cursos
@router.put("/{course_id}")
async def update_course(
    course_id: str,
    nombre: str = Form(""),
    descripcion: Optional[str] = Form(""),
    max_estudiantes: int = Form(1),
    estudiantes: Optional[List[str]] = Form([]),
    equipos: Optional[List[str]] = Form([]),
    tareas: Optional[List[str]] = Form([]),
    user: dict = Depends(require_profesor)
):
    profesor_id = user["username"]
    profesor_email = user["email"]
    profesor = await db.users.find_one({"_id": ObjectId(profesor_id)})
    profesor_nombre = profesor["nombre"]
    
    
    estudiantes_id = []
    for email in estudiantes:
        email_list = [e.strip() for e in email.split(",") if e.strip()]

    duplicados = [email for email in email_list if email_list.count(email) > 1]
    if duplicados:
        raise HTTPException(
            status_code=400,
            detail=f"Estudiantes repetidos: {', '.join(set(duplicados))}"
        )

    for email in email_list:
        estudiante = await db.users.find_one({"email": email, "rol": "estudiante"})
        if not estudiante:
            raise HTTPException(
                status_code=404,
                detail=f"El estudiante con email {email} no existe"
            )
        estudiantes_id.append("mail: "+str(email)+", nombre: "+str(estudiante["nombre"])+", id: "+str(estudiante["_id"]))

    total_estudiantes = len(estudiantes_id)
    
    if total_estudiantes>max_estudiantes:
        raise HTTPException(
            status_code=400,
            detail=f"los estudiantes exeden la cantidad maxima"
        )
    
    course_dict = {
        "nombre": nombre,
        "descripcion": descripcion,
        "profesor_id": profesor_id,
        "profesor_nombre": profesor_nombre,
        "profesor_email": profesor_email,
        "max_estudiantes": max_estudiantes,
        "estudiantes": estudiantes,
        "equipos": equipos,
        "tareas": tareas,
        "total_estudiantes": total_estudiantes,
        "fecha_actualizacion": datetime.utcnow()
    }

    result = await db.courses.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": course_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    return {"message": "Curso actualizado correctamente"}

#  Solo profesores pueden eliminar cursos
@router.delete("/{course_id}")
async def delete_course(course_id: str, user: dict = Depends(require_profesor)):
    result = await db.courses.delete_one({"_id": ObjectId(course_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"message": "Curso eliminado correctamente"}
