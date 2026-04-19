from fastapi import FastAPI
from database import engine
import models
from routers import admin
from routers import room
from routers import reservation
from routers import clients
from routers import additional_services


app = FastAPI(title="Hotel API", description="API для управления отелем")

app.include_router(admin.router)

app.include_router(room.router)

app.include_router(reservation.router)

app.include_router(clients.router)

app.include_router(additional_services.router)