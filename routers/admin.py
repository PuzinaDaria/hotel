from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from typing import List

router = APIRouter(prefix="/admin", tags=["Administrators"])

@router.get("/", response_model=List[schemas.AdminResponse])
def get_all_admins(db: Session = Depends(get_db)):
    admins = db.query(models.Admin).all()
    return admins

@router.post("/", response_model=schemas.AdminResponse)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(models.Admin).filter(
        models.Admin.a_login == admin.a_login
    ).first()
    
    if existing_admin:
        raise HTTPException(status_code=400, detail=f"Логин '{admin.a_login}' уже существует")
    
    new_admin = models.Admin(
        a_name=admin.a_name,
        a_lastname=admin.a_lastname,
        a_login=admin.a_login,
        a_password=admin.a_password,
        a_st=admin.a_st
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    return new_admin

@router.get("/{a_id}", response_model=schemas.AdminResponse)
def get_admin_by_id(a_id: int, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.a_id == a_id).first()
    
    if admin is None:
        raise HTTPException(status_code=404, detail=f"Администратор с id {a_id} не найден")
    
    return admin

@router.patch("/{a_id}", response_model=schemas.AdminResponse)
def update_admin(a_id: int, admin_update: schemas.AdminUpdate, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.a_id == a_id).first()
    
    if admin is None:
        raise HTTPException(status_code=404, detail=f"Администратор с id {a_id} не найден")
    
    update_data = admin_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(admin, field, value)
    
    db.commit()
    db.refresh(admin)
    
    return admin

@router.delete("/{a_id}")
def delete_admin(a_id: int, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.a_id == a_id).first()
    
    if admin is None:
        raise HTTPException(status_code=404, detail=f"Администратор с id {a_id} не найден")
    
    db.delete(admin)
    db.commit()
    
    return {"message": f"Администратор {admin.a_name} {admin.a_lastname} успешно удален"}