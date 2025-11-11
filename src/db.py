# src/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Obtener valores del entorno
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

if not MONGO_URL or not MONGO_DB:
    raise ValueError(" No se encontraron las variables MONGO_URL o MONGO_DB en el .env")

# Conexión a MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]

print(f" Conectado a la base de datos: {MONGO_DB}")
