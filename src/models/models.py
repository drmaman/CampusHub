from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nombre: str
    rol: str
    id: str = Field(..., alias="_id")   

    class Config:
        populate_by_name = True



# Usuario

class UserModel(BaseModel):
    nombre: str
    email: EmailStr
    password: Optional[str] = None
    rol: str = Field(..., description="profesor o estudiante")
    

  
class UserMode2(BaseModel):
    nombre: str
    email: EmailStr
    rol: str = Field(..., description="profesor o estudiante")

# Curso

class CourseModel(BaseModel):
    nombre: str = " "
    descripcion: Optional[str] = None
    profesor_id: str
    profesor_email:str
    profesor_nombre:str
    estudiantes: Optional[List[str]] = []
    equipos: Optional[List[str]] = []
    tareas: Optional[List[str]] = []
    max_estudiantes: int = 30         
    total_estudiantes: int = 0        
    fecha_creacion: Optional[datetime] = None

class CourseMode2(BaseModel):
    id: str = Field(..., alias="_id")
    nombre: str 
    descripcion: Optional[str] = None
    profesor_id: str
    profesor_email:str
    profesor_nombre:str
    estudiantes: Optional[List[str]] = []
    equipos: Optional[List[str]] = []
    tareas: Optional[List[str]] = []
    max_estudiantes: int = 30         
    total_estudiantes: int = 0        
    fecha_creacion: Optional[datetime] = None
# =======================
# Equipo de proyecto
# =======================
class TeamModel(BaseModel):
    nombre: str
    curso_id: str
    miembros: List[str]
    miembros_total: int = 0
    proyecto: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    

 
class TeamMode2(BaseModel):
    id: str = Field(..., alias="_id")
    nombre: str
    curso_id: str
    miembros: List[str]
    miembros_total: int = 0
    proyecto: Optional[str] = None

# Entrega / Tarea

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
class SubmissionMode2(BaseModel):
    id: str = Field(..., alias="_id")
    titulo: str
    descripcion: Optional[str] = None
    curso_id: str
    estudiante: str
    fecha_entrega: datetime = Field(default_factory=datetime.utcnow)
    archivo_url: Optional[str] = None
    estado: str = "enviado"
    retroalimentacion_id: Optional[str] = None

#tareas
class TaskModel(BaseModel):

    titulo: str
    descripcion: Optional[str]
    curso_id: str
    fecha_limite: Optional[datetime]
    estado: str
    fecha_creacion: datetime
    entrega_id: Optional[str] = None

class TaskMode2(BaseModel):
    id: str = Field(..., alias="_id")
    titulo: str
    curso_id: str
    fecha_limite: Optional[datetime]
    estado: str
    fecha_creacion: datetime
    entrega_id: Optional[str] = None
# Retroalimentación

class FeedbackModel(BaseModel):
    submission_id: str
    profesor_id: str
    comentario: Optional[str] = None
    calificacion: Optional[float] = None
    fecha: datetime = Field(default_factory=datetime.utcnow)

   
class FeedbackMode2(BaseModel):
    id: str = Field(..., alias="_id")
    submission_id: str
    profesor_id: str
    comentario: Optional[str] = None
    calificacion: Optional[float] = None
    fecha: datetime = Field(default_factory=datetime.utcnow)