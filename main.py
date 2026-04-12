from fastapi import FastAPI
from database import engine
import models
from routers import admin
from routers import room
from routers import reservation


app = FastAPI(title="Hotel API", description="API для управления отелем")

app.include_router(admin.router)

app.include_router(room.router)

app.include_router(reservation.router)