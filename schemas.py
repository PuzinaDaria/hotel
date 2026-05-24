from pydantic import BaseModel
from typing import Optional
from datetime import date


class AdminCreate(BaseModel):
    a_name: str
    a_lastname: str
    a_login: str
    a_password: str
    a_st: Optional[str] = "активен"

class AdminUpdate(BaseModel):
    a_name: Optional[str] = None
    a_lastname: Optional[str] = None
    a_login: Optional[str] = None
    a_password: Optional[str] = None
    a_st: Optional[str] = None

class AdminResponse(BaseModel):
    a_id: int
    a_name: str
    a_lastname: str
    a_login: str
    a_password: str
    a_st: Optional[str] = None
    
    class Config:
        from_attributes = True

class RoomCreate(BaseModel):
    n_count: int
    n_type: str
    n_cost: int
    n_st: Optional[str] = "свободен"

class RoomUpdate(BaseModel):
    n_count: Optional[int] = None
    n_type: Optional[str] = None
    n_cost: Optional[int] = None
    n_st: Optional[str] = None  
    
    class Config:
        extra = "forbid"

class RoomResponse(BaseModel):
    n_id: int
    n_count: int
    n_type: str
    n_cost: int
    n_st: str
    
    class Config:
        from_attributes = True

class ReservationCreate(BaseModel):
    a_id: int
    c_id: int
    n_id: int
    as_id: int
    r_datearrival: date
    r_datedeparture: date
    r_st: Optional[str] = "активно"

class ReservationUpdate(BaseModel):
    a_id: Optional[int] = None
    c_id: Optional[int] = None
    n_id: Optional[int] = None
    as_id: Optional[int] = None
    r_datearrival: Optional[date] = None
    r_datedeparture: Optional[date] = None
    r_st: Optional[str] = None

class ReservationResponse(BaseModel):
    r_id: int
    a_id: int
    c_id: int
    n_id: int
    as_id: int
    r_datearrival: date
    r_datedeparture: date
    r_st: Optional[str] = None
    
    class Config:
        from_attributes = True

class ClientCreate(BaseModel):
    c_name: str
    c_lastname: str
    c_tel: str


class ClientUpdate(BaseModel):
    c_name: Optional[str] = None
    c_lastname: Optional[str] = None
    c_tel: Optional[str] = None


class ClientResponse(BaseModel):
    c_id: int
    c_name: str
    c_lastname: str
    c_tel: str

    class Config:
        from_attributes = True


class AdditionalServiceCreate(BaseModel):
    as_name: str
    as_cost: int


class AdditionalServiceUpdate(BaseModel):
    as_name: Optional[str] = None
    as_cost: Optional[int] = None


class AdditionalServiceResponse(BaseModel):
    as_id: int
    as_name: str
    as_cost: int

    class Config:
        from_attributes = True
