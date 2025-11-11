from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# ------------------------------
# MODELOS DE AUTENTICACIÓN
# ------------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nombre: str
    rol: str
    _id: str

# =======================
# Usuario
# =======================
class UserModel(BaseModel):
    nombre: str
    email: EmailStr
    password: Optional[str] = None
    rol: str = Field(..., description="profesor o estudiante")
    

    class Config:
        orm_mode = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nombre": "nombre apellido",
                "email": "nombre@campushub.com",
                "password": "1234",
                "rol": "profesor"
            }
        }

# =======================
# Curso
# =======================
class CourseModel(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    profesor_id: str
    estudiantes: Optional[List[str]] = []
    equipos: Optional[List[str]] = []
    tareas: Optional[List[str]] = []

    class Config:
        orm_mode = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nombre": "Introducción a la IA",
                "descripcion": "Curso sobre fundamentos de IA y redes neuronales",
                "profesor_id": "671ea2f912b9df0f91f1a333",
                "estudiantes": [],
                "equipos": [],
                "tareas": []
            }
        }

# =======================
# Equipo de proyecto
# =======================
class TeamModel(BaseModel):
    nombre: str
    curso_id: str
    miembros: List[str]
    proyecto: Optional[str] = None

    class Config:
        orm_mode = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nombre": "Equipo Innovadores",
                "curso_id": "671ea2f912b9df0f91f1a333",
                "miembros": ["671ea2f912b9df0f91f1a331", "671ea2f912b9df0f91f1a332"],
                "proyecto": "Reconocimiento de dígitos con CNN"
            }
        }

# =======================
# Entrega / Tarea
# =======================
class SubmissionModel(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    curso_id: str
    autor_id: str
    fecha_entrega: datetime = Field(default_factory=datetime.utcnow)
    archivo_url: Optional[str] = None
    estado: str = "enviado"
    retroalimentacion_id: Optional[str] = None

    class Config:
        orm_mode = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "titulo": "Entrega 1 - Clasificador MNIST",
                "descripcion": "Primera entrega del proyecto CNN",
                "curso_id": "671ea2f912b9df0f91f1a333",
                "autor_id": "671ea2f912b9df0f91f1a331",
                "archivo_url": "https://drive.google.com/entrega1",
                "estado": "enviado"
            }
        }

# =======================
# Retroalimentación
# =======================
class FeedbackModel(BaseModel):
    submission_id: str
    profesor_id: str
    comentario: Optional[str] = None
    calificacion: Optional[float] = None
    fecha: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "submission_id": "671ea2f912b9df0f91f1a334",
                "profesor_id": "671ea2f912b9df0f91f1a335",
                "comentario": "Buen trabajo, aunque podrías mejorar la documentación.",
                "calificacion": 9.2
            }
        }
