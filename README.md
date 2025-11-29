#  CampusHub — Plataforma Académica con MongoDB

### Proyecto Final — Curso de Bases de Datos NoSQL (MongoDB)

Una plataforma académica desarrollada con FastAPI y MongoDB para la gestión de cursos, tareas, entregas y retroalimentación entre estudiantes y profesores.

## Características
Autenticación JWT con roles (estudiante, profesor, administrador)

Gestión de usuarios con diferentes niveles de acceso

Cursos creados por profesores con límite de estudiantes

Tareas con fechas límite y estados automáticos

Entregas de estudiantes con archivos adjuntos

Equipos de trabajo para proyectos colaborativos

Sistema de retroalimentación y calificaciones

Programación automática para tareas vencidas

## Tecnologías
Backend: FastAPI

Base de datos: MongoDB Atlas

Autenticación: JWT (JSON Web Tokens)

Programación: APScheduler

Hashing: Passlib (bcrypt)

Validación: Pydantic

## Estructura del Proyecto

src/
├── main.py                 # Aplicación principal FastAPI
├── db.py                  # Conexión a MongoDB
├── core/
│   ├── security.py        # Autenticación y autorización
│   └── scheduler.py       # Tareas programadas
├── models/
│   └── models.py          # Modelos Pydantic
└── routers/
    ├── auth.py            # Autenticación (login/logout)
    ├── users.py           # Gestión de usuarios
    ├── courses.py         # Gestión de cursos
    ├── tasks.py           # Gestión de tareas
    ├── submissions.py     # Gestión de entregas
    ├── feedback.py        # Sistema de retroalimentación
    └── teams.py           # Gestión de equipos
### Roles y Permisos
## Profesor
Crear, editar y eliminar cursos

Crear y gestionar tareas

Proporcionar retroalimentación


## Estudiante

Inscribirse en cursos

Unirse a equipos

Realizar entregas de tareas


## Administrador
Gestionar todos los usuarios

### Endpoints Principales

## Autenticación
POST /v1/login/ - Iniciar sesión

POST /v1/login/logout - Cerrar sesión

## Usuarios
GET /v1/users/ - Listar usuarios 

POST /v1/users/ - Crear usuario (admin)

PUT /v1/users/{user_id} - Actualizar usuario (admin)

DELETE /v1/users/{user_id} - Eliminar usuario (admin)

## Cursos
GET /v1/courses/ - Listar cursos 

GET /v1/courses/{course_id} - Obtener curso específico

POST /v1/courses/ - Crear curso (profesor)

PUT /v1/courses/{course_id} - Actualizar curso (profesor)

DELETE /v1/courses/{course_id} - Eliminar curso (profesor)

## Tareas
GET /v1/tasks/ - Listar tareas

GET /v1/tasks/{task_id} - Obtener tarea específica

POST /v1/tasks/ - Crear tarea (profesor)

PUT /v1/tasks/{task_id} - Actualizar tarea (profesor)

DELETE /v1/tasks/{task_id} - Eliminar tarea (profesor)

## Entregas
GET /v1/submissions/ - Listar entregas

GET /v1/submissions/{submission_id} - Obtener entrega específica

POST /v1/submissions/ - Crear entrega (estudiante)

PUT /v1/submissions/{submission_id} - Actualizar entrega (estudiante)

DELETE /v1/submissions/{submission_id} - Eliminar entrega (estudiante)

## Configuración
Variables de Entorno
Crea un archivo .env en la raíz del proyecto:

## .env
MONGO_URI="mongodb+srv://<USER>:<PASSWORD>@<CLUSTER>.mongodb.net"
MONGO_DB_NAME="campushub"

JWT_SECRET="supersecreto"
JWT_ALGORITHM="HS256"

## Instalación
Clona el repositorio:
git clone https://github.com/<tu_usuario>/CampusHub.git
cd CampusHub
## Instala las dependencias:

## bash

pip install -r requirements.txt

Configura las variables de entorno en el archivo .env

## Ejecuta la aplicación:

## bash

uvicorn src.main:app --reload

El servidor se levantará en:
>  http://127.0.0.1:8000

La documentación interactiva (Swagger):
>  http://127.0.0.1:8000/docs

## Dependencias Principales
txt
fastapi
uvicorn
motor
pymongo
python-dotenv
python-jose[cryptography]
passlib[bcrypt]
apscheduler
pydantic


##  Equipo de desarrollo

| Nombre | Rol | Tareas |
|--------|------|--------|
| Alejandro Adame | Backend & MongoDB | Modelado, CRUD, Atlas |
| DIEGO JULIAN | Plan de índices & Índices creados | reporte de explain(), Benchmark de índices y Manual técnico |

---

## Características Automáticas
Verificación de tareas vencidas: Cada 2 minutos, el sistema actualiza automáticamente el estado de las tareas cuya fecha límite ha pasado.

Tokens JWT: Expiran después de 2 horas con renovación automática al login.

## Modelos de Datos
Los modelos principales incluyen:

User: Información de usuarios con roles

Course: Cursos con estudiantes y tareas

Task: Tareas con fechas límite

Submission: Entregas de estudiantes

Feedback: Retroalimentación de profesores

Team: Equipos de trabajo colaborativo