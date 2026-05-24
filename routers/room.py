from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from typing import List

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", response_model=List[schemas.RoomResponse])
def get_all_rooms(db: Session = Depends(get_db)):
    rooms = db.query(models.Room).all()
    return rooms

@router.post("/", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    existing_room = db.query(models.Room).filter(
        models.Room.n_count == room.n_count
    ).first()
    
    if existing_room:
        raise HTTPException(status_code=400, detail=f"Комната '{room.n_count}' уже существует")
    
    new_room = models.Room(
        n_count=room.n_count,
        n_type=room.n_type,
        n_cost=room.n_cost,
        n_st=room.n_st
    )
    
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    
    return new_room

@router.get("/{n_id}", response_model=schemas.RoomResponse)
def get_room_by_id(n_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.n_id == n_id).first()
    
    if room is None:
        raise HTTPException(status_code=404, detail=f"Комната с id {n_id} не найдена")
    
    return room

@router.patch("/{n_id}", response_model=schemas.RoomResponse)
def update_room(n_id: int, room_update: schemas.RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.n_id == n_id).first()
    
    if room is None:
        raise HTTPException(status_code=404, detail=f"Комната с id {n_id} не найдена")
    
    update_data = room_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(room, field, value)
    
    db.commit()
    db.refresh(room)
    
    return room

@router.delete("/{n_id}")
def delete_room(n_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.n_id == n_id).first()
    
    if room is None:
        raise HTTPException(status_code=404, detail=f"Комната с id {n_id} не найдена")
    
    db.delete(room)
    db.commit()
    
    return {"message": f"Комната {room.n_count} успешно удалена"}