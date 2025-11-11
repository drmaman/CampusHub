from fastapi import APIRouter, HTTPException
from src.db import db
from src.models.models import TeamModel
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=list[TeamModel])
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

@router.post("/", response_model=TeamModel)
async def create_team(team: TeamModel):
    team_dict = team.model_dump(by_alias=True, exclude=["id"])
    result = await db.teams.insert_one(team_dict)
    team_dict["_id"] = str(result.inserted_id)
    return team_dict

@router.put("/{team_id}")
async def update_team(team_id: str, team: TeamModel):
    team_dict = team.model_dump(by_alias=True, exclude=["id"])
    result = await db.teams.update_one({"_id": ObjectId(team_id)}, {"$set": team_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"message": "Equipo actualizado correctamente"}

@router.delete("/{team_id}")
async def delete_team(team_id: str):
    result = await db.teams.delete_one({"_id": ObjectId(team_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"message": "Equipo eliminado correctamente"}
