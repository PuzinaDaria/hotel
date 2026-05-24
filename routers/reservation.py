from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, join
from database import get_db
import models
import schemas
from typing import List
from datetime import date
import logging

router = APIRouter(prefix="/reservation", tags=["Reservations"])

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/")
def get_all_reservations(db: Session = Depends(get_db)):
    try:
        reservations = db.query(models.Reservation).all()
        
        result_list = []
        for r in reservations:
            client = db.query(models.Client).filter(models.Client.c_id == r.c_id).first()
            room = db.query(models.Room).filter(models.Room.n_id == r.n_id).first()
            admin = db.query(models.Admin).filter(models.Admin.a_id == r.a_id).first()
            services = [s.as_name for s in r.services]
            
            result_list.append({
                "r_id": r.r_id,
                "guest": f"{client.c_name} {client.c_lastname}" if client else "Неизвестно",
                "phone": client.c_tel if client else "Неизвестно",
                "room_number": room.n_count if room else "Неизвестно",
                "room_type": room.n_type if room else "Неизвестно",
                "services": services,
                "admin": f"{admin.a_name} {admin.a_lastname}" if admin else "Неизвестно",
                "check_in": r.r_datearrival.strftime("%Y-%m-%d") if r.r_datearrival else "",
                "check_out": r.r_datedeparture.strftime("%Y-%m-%d") if r.r_datedeparture else "",
                "status": r.r_st
            })
        
        return result_list
    except Exception as e:
        logger.error(f"Ошибка при получении бронирований: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")

@router.post("/")
def create_reservation(request_data: dict, db: Session = Depends(get_db)):
    try:
        admin_id = request_data.get('a_id')
        room_id = request_data.get('n_id')
        service_ids = request_data.get('service_ids', [])  
        check_in = request_data.get('r_datearrival')
        check_out = request_data.get('r_datedeparture')
        status = request_data.get('r_st', 'активно')

        client_name = request_data.get('c_name')
        client_lastname = request_data.get('c_lastname')
        client_phone = request_data.get('c_tel')
        
        if not all([admin_id, room_id, check_in, check_out, client_name, client_lastname, client_phone]):
            raise HTTPException(status_code=400, detail="Заполните все обязательные поля")
 
        admin = db.query(models.Admin).filter(models.Admin.a_id == admin_id).first()
        if not admin:
            raise HTTPException(status_code=404, detail=f"Администратор с id {admin_id} не найден")
        
        room = db.query(models.Room).filter(models.Room.n_id == room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail=f"Комната с id {room_id} не найдена")

        if check_in >= check_out:
            raise HTTPException(status_code=400, detail="Дата заезда должна быть раньше даты выезда")
        
        services = []
        if service_ids:
            for service_id in service_ids:
                service = db.query(models.AdditionalService).filter(models.AdditionalService.as_id == service_id).first()
                if not service:
                    raise HTTPException(status_code=404, detail=f"Услуга с id {service_id} не найдена")
                services.append(service)

        new_client = models.Client(
            c_name=client_name,
            c_lastname=client_lastname,
            c_tel=client_phone
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)

        new_reservation = models.Reservation(
            a_id=admin_id,
            c_id=new_client.c_id,
            n_id=room_id,
            r_datearrival=check_in,
            r_datedeparture=check_out,
            r_st=status
        )

        new_reservation.services = services
        
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
        
        return {
            "success": True,
            "message": "Бронирование успешно создано",
            "reservation_id": new_reservation.r_id,
            "client_id": new_client.c_id,
            "services_count": len(services)
        }
    except Exception as e:
        logger.error(f"Ошибка при создании бронирования: {str(e)}", exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")

@router.get("/{r_id}")
def get_reservation_by_id(r_id: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.r_id == r_id).first()
    
    if reservation is None:
        raise HTTPException(status_code=404, detail=f"Бронирование с id {r_id} не найдено")
    
    client = db.query(models.Client).filter(models.Client.c_id == reservation.c_id).first()
    room = db.query(models.Room).filter(models.Room.n_id == reservation.n_id).first()
    admin = db.query(models.Admin).filter(models.Admin.a_id == reservation.a_id).first()
    services = [{"id": s.as_id, "name": s.as_name, "cost": s.as_cost} for s in reservation.services]
    
    return {
        "r_id": reservation.r_id,
        "c_id": reservation.c_id,
        "guest_name": client.c_name if client else "",
        "guest_lastname": client.c_lastname if client else "",
        "phone": client.c_tel if client else "",
        "room_number": room.n_count if room else 0,
        "room_type": room.n_type if room else "",
        "services": services,
        "admin_name": admin.a_name if admin else "",
        "admin_lastname": admin.a_lastname if admin else "",
        "check_in": reservation.r_datearrival.strftime("%Y-%m-%d") if reservation.r_datearrival else "",
        "check_out": reservation.r_datedeparture.strftime("%Y-%m-%d") if reservation.r_datedeparture else "",
        "status": reservation.r_st
    }

@router.put("/{r_id}")
def update_reservation_full(r_id: int, request_data: dict, db: Session = Depends(get_db)):
    try:
        reservation = db.query(models.Reservation).filter(models.Reservation.r_id == r_id).first()
        if reservation is None:
            raise HTTPException(status_code=404, detail=f"Бронирование с id {r_id} не найдено")

        client = db.query(models.Client).filter(models.Client.c_id == reservation.c_id).first()
        if client is None:
            raise HTTPException(status_code=404, detail=f"Клиент с id {reservation.c_id} не найден")
        
        if 'c_name' in request_data:
            client.c_name = request_data['c_name']
        if 'c_lastname' in request_data:
            client.c_lastname = request_data['c_lastname']
        if 'c_tel' in request_data:
            client.c_tel = request_data['c_tel']

        if 'a_id' in request_data:
            admin = db.query(models.Admin).filter(models.Admin.a_id == request_data['a_id']).first()
            if not admin:
                raise HTTPException(status_code=404, detail=f"Администратор с id {request_data['a_id']} не найден")
            reservation.a_id = request_data['a_id']
        
        if 'n_id' in request_data:
            room = db.query(models.Room).filter(models.Room.n_id == request_data['n_id']).first()
            if not room:
                raise HTTPException(status_code=404, detail=f"Комната с id {request_data['n_id']} не найдена")
            reservation.n_id = request_data['n_id']
        
        if 'r_datearrival' in request_data:
            reservation.r_datearrival = request_data['r_datearrival']
        
        if 'r_datedeparture' in request_data:
            reservation.r_datedeparture = request_data['r_datedeparture']
        
        if 'r_st' in request_data:
            reservation.r_st = request_data['r_st']

        if 'service_ids' in request_data:
            service_ids = request_data['service_ids']
            services = []
            for service_id in service_ids:
                service = db.query(models.AdditionalService).filter(models.AdditionalService.as_id == service_id).first()
                if not service:
                    raise HTTPException(status_code=404, detail=f"Услуга с id {service_id} не найдена")
                services.append(service)
            reservation.services = services

        if reservation.r_datearrival >= reservation.r_datedeparture:
            raise HTTPException(status_code=400, detail="Дата заезда должна быть раньше даты выезда")
        
        db.commit()
        db.refresh(reservation)
        db.refresh(client)
        
        return {
            "success": True,
            "message": "Бронирование обновлено",
            "reservation_id": reservation.r_id
        }
    except Exception as e:
        logger.error(f"Ошибка при обновлении бронирования: {str(e)}", exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")

@router.delete("/{r_id}")
def delete_reservation(r_id: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.r_id == r_id).first()
    
    if reservation is None:
        raise HTTPException(status_code=404, detail=f"Бронирование с id {r_id} не найдено")
    
    db.delete(reservation)
    db.commit()
    
    return {"message": f"Бронирование {r_id} успешно отменено"}

@router.get("/rooms/list", response_model=List[schemas.RoomResponse])
def get_rooms_list(db: Session = Depends(get_db)):
    return db.query(models.Room).all()

@router.get("/services/list", response_model=List[schemas.AdditionalServiceResponse])
def get_services_list(db: Session = Depends(get_db)):
    return db.query(models.AdditionalService).all()

@router.get("/admins/list", response_model=List[schemas.AdminResponse])
def get_admins_list(db: Session = Depends(get_db)):
    return db.query(models.Admin).all()