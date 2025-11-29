from fastapi import APIRouter, HTTPException, Form
from src.db import db
from src.models.models import TeamModel,TeamMode2
from bson import ObjectId
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=list[TeamMode2])
async def get_teams():
    teams = await db.teams.find().to_list(100)
    for team in teams:
        team["_id"] = str(team["_id"])
    return teams

@router.get("/{team_id}", response_model=TeamModel)
async def get_team(team_id: str):
    team = await db.teams.find_one({"_id": ObjectId(team_id)})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    team["_id"] = str(team["_id"])
    return team

@router.post("/",response_model=list[TeamModel])
async def create_team(
    nombre: str = Form("", description="nombre del equipo"),
    curso_id: str = Form("", description="id del curso"),
    integrantes: List[str] = Form(...,description="email de los integrantes"),   
    proyecto: str = Form("", description="nombre del proyecto")
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
    
    miembros_id = []
    for email in integrantes:
        email_list = [e.strip() for e in email.split(",") if e.strip()]

    duplicados = [email for email in email_list if email_list.count(email) > 1]
    if duplicados:
        raise HTTPException(
            status_code=400,
            detail=f"integrantes repetidos: {', '.join(set(duplicados))}"
        )

    for email in email_list:
        miembro = await db.users.find_one({"email": email, "rol": "estudiante"})
        if not miembro:
            raise HTTPException(
                status_code=404,
                detail=f"El integrante con email {email} no existe"
            )
        miembros_id.append("email: "+str(email)+", nombre: "+str(miembro["nombre"])+", id: "+str(miembro["_id"]))

    miembro_total=len(miembros_id)

    team_dict = {
        "nombre": nombre,
        "curso_id": curso_id,
        "integrantes": miembros_id,
        "integrantes totales": miembro_total,
        "proyecto": proyecto,
        "fecha_creacion": datetime.utcnow() 
    }

    result = await db.teams.insert_one(team_dict)
    team_dict["_id"] = str(result.inserted_id)
    task_id = str(result.inserted_id)

    update_result = await db.courses.update_one(
        {"_id": ObjectId(curso_id)},
        {"$push": {"equipos": task_id}}
    )
    return team_dict

@router.put("/{team_id}")
async def update_team(
    team_id: str,
    nombre: str = Form("", description="nombre del equipo"),
    curso_id: str = Form("", description="id del curso"),
    integrantes: List[str] = Form("", description="email de los integrantes"),
    proyecto: str = Form("", description="nombre del proyecto")
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
            detail=f"El curso no existe {curso_id}"
        )
    
    miembros_id = []
    for email in integrantes:
        email_list = [e.strip() for e in email.split(",") if e.strip()]

    duplicados = [email for email in email_list if email_list.count(email) > 1]
    if duplicados:
        raise HTTPException(
            status_code=400,
            detail=f"integrantes repetidos: {', '.join(set(duplicados))}"
        )

    for email in email_list:
        miembro = await db.users.find_one({"email": email, "rol": "estudiante"})
        if not miembro:
            raise HTTPException(
                status_code=404,
                detail=f"El integrante con email {email} no existe"
            )
        miembros_id.append("email: "+str(email)+", nombre: "+str(miembro["nombre"])+", id: "+str(miembro["_id"]))

    miembro_total=len(miembros_id)
    team_dict = {
        "nombre": nombre,
        "curso_id": curso_id,
        "integrantes": miembros_id,
        "integrantes totales": miembro_total,
        "proyecto": proyecto,
        "fecha_actualizacion": datetime.utcnow()

    }
    
    result = await db.teams.update_one(
        {"_id": ObjectId(team_id)},
        {"$set": team_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    return {"message": "Equipo actualizado correctamente"}

@router.delete("/{team_id}")
async def delete_team(team_id: str):
    result = await db.teams.delete_one({"_id": ObjectId(team_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"message": "Equipo eliminado correctamente"}
