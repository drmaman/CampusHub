
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# Leer variables del .env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = "CampusHub"

# Cliente MongoDB
client = AsyncIOMotorClient(MONGO_URI)

# Base de datos
db = client[MONGO_DB_NAME]
