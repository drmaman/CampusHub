from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from src.db import db

scheduler = AsyncIOScheduler()

async def check_task_deadlines():
    now = datetime.utcnow()

    # Buscar tareas activas cuya fecha ya pasó
    tareas = await db.tasks.find({
        "estado": "activa",
        "fecha_limite": {"$lte": now}
    }).to_list(None)

    for t in tareas:
        await db.tasks.update_one(
            {"_id": t["_id"]},
            {"$set": {
                "estado": "vencida",
                "fecha_actualizacion": datetime.utcnow()
            }}
        )

        print(f"Tarea {t['_id']} marcada como vencida")

def start_scheduler():
    scheduler.add_job(check_task_deadlines, "interval", minutes=2)  
    scheduler.start()
