from fastapi import FastAPI
from src.routers import users, courses, teams, submissions, feedback,auth

app = FastAPI(
    title="CampusHub API",
    version="1.3",
    description="Plataforma académica con MongoDB"
)

# Registrar los routers
app.include_router(auth.router, prefix="/v1/login", tags=["login"])
app.include_router(users.router, prefix="/v1/users", tags=["Usuarios"])
app.include_router(courses.router, prefix="/v1/courses", tags=["Cursos"])
app.include_router(teams.router, prefix="/v1/teams", tags=["Equipos"])
app.include_router(submissions.router, prefix="/v1/submissions", tags=["Entregas"])
app.include_router(feedback.router, prefix="/v1/feedback", tags=["Retroalimentaciones"])

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a CampusHub API 🚀"}