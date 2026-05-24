from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/rooms", tags=["Rooms"])


# ➕ создать комнату
@router.post("/", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = models.Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


# 📋 все комнаты
@router.get("/", response_model=list[schemas.RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()


# 🔍 по ID
@router.get("/{n_id}", response_model=schemas.RoomResponse)
def get_room(n_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.n_id == n_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    return room


# ✏️ обновление
@router.patch("/{n_id}", response_model=schemas.RoomResponse)
def update_room(n_id: int, data: schemas.RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.n_id == n_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(room, key, value)

    db.commit()
    db.refresh(room)
    return room


# ❌ удалить
@router.delete("/{n_id}")
def delete_room(n_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.n_id == n_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    db.delete(room)
    db.commit()
    return {"message": "Комната удалена"}