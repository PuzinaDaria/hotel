from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from typing import List
from datetime import date

router = APIRouter(prefix="/reservation", tags=["Reservations"])

# Получение списка всех бронирований
@router.get("/", response_model=List[schemas.ReservationResponse])
def get_all_reservations(db: Session = Depends(get_db)):
    reservations = db.query(models.Reservation).all()
    return reservations

# Создание нового бронирования
@router.post("/", response_model=schemas.ReservationResponse)
def create_reservation(
    reservation: schemas.ReservationCreate, 
    db: Session = Depends(get_db)
):
    # Проверка администратора
    admin = db.query(models.Admin).filter(models.Admin.a_id == reservation.a_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail=f"Администратор с id {reservation.a_id} не найден")
    
    # Проверка комнаты
    room = db.query(models.Room).filter(models.Room.n_id == reservation.n_id).first()
    if not room:
        raise HTTPException(status_code=404, detail=f"Комната с id {reservation.n_id} не найдена")
    
    # Проверка даты
    if reservation.r_datearrival >= reservation.r_datedeparture:
        raise HTTPException(status_code=400, detail="Дата заезда должна быть раньше даты выезда")
    
    new_reservation = models.Reservation(
        a_id=reservation.a_id,
        c_id=reservation.c_id,
        n_id=reservation.n_id,
        as_id=reservation.as_id,
        r_datearrival=reservation.r_datearrival,
        r_datedeparture=reservation.r_datedeparture,
        r_st=reservation.r_st
    )
    
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    
    return new_reservation

# Получение информации о бронировании по ID
@router.get("/{r_id}", response_model=schemas.ReservationResponse)
def get_reservation_by_id(r_id: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.r_id == r_id).first()
    
    if reservation is None:
        raise HTTPException(status_code=404, detail=f"Бронирование с id {r_id} не найдено")
    
    return reservation# Изменение бронирования
@router.patch("/{r_id}", response_model=schemas.ReservationResponse)
def update_reservation(
    r_id: int, 
    reservation_update: schemas.ReservationUpdate, 
    db: Session = Depends(get_db)
):
    reservation = db.query(models.Reservation).filter(models.Reservation.r_id == r_id).first()
    
    if reservation is None:
        raise HTTPException(status_code=404, detail=f"Бронирование с id {r_id} не найдено")
    
    update_data = reservation_update.model_dump(exclude_unset=True)
    
    # Если обновляются даты 
    if 'r_datearrival' in update_data and 'r_datedeparture' in update_data:
        if update_data['r_datearrival'] >= update_data['r_datedeparture']:
            raise HTTPException(status_code=400, detail="Дата заезда должна быть раньше даты выезда")
    elif 'r_datearrival' in update_data:
        new_arrival = update_data['r_datearrival']
        departure = reservation.r_datedeparture
        if new_arrival >= departure:
            raise HTTPException(status_code=400, detail="Дата заезда должна быть раньше даты выезда")
    elif 'r_datedeparture' in update_data:
        arrival = reservation.r_datearrival
        new_departure = update_data['r_datedeparture']
        if arrival >= new_departure:
            raise HTTPException(status_code=400, detail="Дата заезда должна быть раньше даты выезда")
    
    # Если обновляется a_id
    if 'a_id' in update_data:
        admin = db.query(models.Admin).filter(models.Admin.a_id == update_data['a_id']).first()
        if not admin:
            raise HTTPException(status_code=404, detail=f"Администратор с id {update_data['a_id']} не найден")
    
    # Если обновляется n_id
    if 'n_id' in update_data:
        room = db.query(models.Room).filter(models.Room.n_id == update_data['n_id']).first()
        if not room:
            raise HTTPException(status_code=404, detail=f"Комната с id {update_data['n_id']} не найдена")
        
    for field, value in update_data.items():
        setattr(reservation, field, value)
    
    db.commit()
    db.refresh(reservation)
    
    return reservation

#Отмена бронирования (удаление)
@router.delete("/{r_id}")
def delete_reservation(r_id: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.r_id == r_id).first()
    
    if reservation is None:
        raise HTTPException(status_code=404, detail=f"Бронирование с id {r_id} не найдено")
    
    db.delete(reservation)
    db.commit()
    
    return {"message": f"Бронирование {r_id} успешно отменено"}