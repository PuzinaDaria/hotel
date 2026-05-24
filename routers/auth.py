from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(prefix="/api", tags=["Authentication"])

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    login = data.get('login')
    password = data.get('password')
    
    if not login or not password:
        return JSONResponse({
            "success": False,
            "error": "Заполните все поля"
        })

    admin_user = db.query(models.Admin).filter(
        models.Admin.a_login == login,
        models.Admin.a_password == password
    ).first()
    
    if admin_user:
        return JSONResponse({
            "success": True,
            "user": {
                "id": admin_user.a_id,
                "name": admin_user.a_name,
                "lastname": admin_user.a_lastname,
                "login": admin_user.a_login,
                "status": admin_user.a_st
            }
        })
    else:
        return JSONResponse({
            "success": False,
            "error": "Неверный логин или пароль"
        })

@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    name = data.get('name')
    lastname = data.get('lastname')
    login = data.get('login')
    password = data.get('password')
    
    if not name or not lastname or not login or not password:
        return JSONResponse({
            "success": False,
            "error": "Заполните все поля"
        })
    
    existing = db.query(models.Admin).filter(models.Admin.a_login == login).first()
    if existing:
        return JSONResponse({
            "success": False,
            "error": "Пользователь с таким логином уже существует"
        })
    
    new_admin = models.Admin(
        a_name=name,
        a_lastname=lastname,
        a_login=login,
        a_password=password,
        a_st="активен"
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    return JSONResponse({
        "success": True,
        "user": {
            "id": new_admin.a_id,
            "name": new_admin.a_name,
            "lastname": new_admin.a_lastname,
            "login": new_admin.a_login
        }
    })