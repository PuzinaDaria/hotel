from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from database import engine
import models
from routers import admin, room, reservation, clients, additional_services
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel API", description="API для управления отелем")

templates = Jinja2Templates(directory="templates")

@app.get("/style.css")
async def serve_css():
    css_path = os.path.join(os.path.dirname(__file__), "templates", "style.css")
    return FileResponse(css_path, media_type="text/css")

app.include_router(admin.router)
app.include_router(room.router)
app.include_router(reservation.router)
app.include_router(clients.router)
app.include_router(additional_services.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/allReservations.html", response_class=HTMLResponse)
async def all_reservations(request: Request):
    return templates.TemplateResponse("allReservations.html", {"request": request})

@app.get("/createReservations.html", response_class=HTMLResponse)
async def create_reservations(request: Request):
    return templates.TemplateResponse("createReservations.html", {"request": request})

@app.get("/room.html", response_class=HTMLResponse)
async def room_page(request: Request):
    return templates.TemplateResponse("room.html", {"request": request})

@app.get("/additionalServices.html", response_class=HTMLResponse)
async def additional_services_page(request: Request):
    return templates.TemplateResponse("additionalServices.html", {"request": request})