from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", response_model=schemas.ClientResponse)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.get("/", response_model=list[schemas.ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()


@router.get("/{c_id}", response_model=schemas.ClientResponse)
def get_client(c_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.c_id == c_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return client


@router.put("/{c_id}", response_model=schemas.ClientResponse)
def put_client(c_id: int, client_data: schemas.ClientCreate, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.c_id == c_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    for key, value in client_data.dict().items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client

@router.patch("/{c_id}", response_model=schemas.ClientResponse)
def patch_client(c_id: int, client_data: schemas.ClientUpdate, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.c_id == c_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    update_data = client_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client


@router.delete("/{c_id}")
def delete_client(c_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.c_id == c_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    db.delete(client)
    db.commit()
    return {"message": "Клиент удалён"}