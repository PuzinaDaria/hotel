from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/services", tags=["Additional Services"])


@router.post("/", response_model=schemas.AdditionalServiceResponse)
def create_service(service: schemas.AdditionalServiceCreate, db: Session = Depends(get_db)):
    db_service = models.AdditionalService(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@router.get("/", response_model=list[schemas.AdditionalServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(models.AdditionalService).all()


@router.get("/{as_id}", response_model=schemas.AdditionalServiceResponse)
def get_service(as_id: int, db: Session = Depends(get_db)):
    service = db.query(models.AdditionalService).filter(models.AdditionalService.as_id == as_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return service


@router.patch("/{as_id}", response_model=schemas.AdditionalServiceResponse)
def update_service(as_id: int, data: schemas.AdditionalServiceUpdate, db: Session = Depends(get_db)):
    service = db.query(models.AdditionalService).filter(models.AdditionalService.as_id == as_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(service, k, v)

    db.commit()
    db.refresh(service)
    return service


@router.delete("/{as_id}")
def delete_service(as_id: int, db: Session = Depends(get_db)):
    service = db.query(models.AdditionalService).filter(models.AdditionalService.as_id == as_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")

    db.delete(service)
    db.commit()
    return {"message": "Услуга удалена"}