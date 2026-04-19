from sqlalchemy import Column, Integer, String, Identity, Date, ForeignKey
from database import Base

class Admin(Base):
    __tablename__ = "admin"
    
    a_id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, index=True)
    a_name = Column(String(50))
    a_lastname = Column(String(50))
    a_login = Column(String(50))
    a_password = Column(String(50))
    a_st = Column(String) 

class Room(Base):
    __tablename__ = "room"
    
    n_id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, index=True)
    n_count = Column(Integer)
    n_type = Column(String(50))
    n_cost = Column(Integer)
    n_st = Column(String)  

class Reservation(Base):
    __tablename__ = "reservation"
    
    r_id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, index=True)
    a_id = Column(Integer, ForeignKey("admin.a_id"))
    c_id = Column(Integer, ForeignKey("client.c_id")) 
    n_id = Column(Integer, ForeignKey("room.n_id"))
    as_id = Column(Integer, ForeignKey("additional_services.as_id"))  
    r_datearrival = Column(Date)  
    r_datedeparture = Column(Date)  
    r_st = Column(String(50))

# CLIENTS
class Client(Base):
    __tablename__ = "client"

    c_id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, index=True)
    c_name = Column(String(50))
    c_lastname = Column(String(50))
    c_tel = Column(String(50))


# ADDITIONAL SERVICES
class AdditionalService(Base):
    __tablename__ = "additional_services"

    as_id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, index=True)
    as_name = Column(String(50))
    as_cost = Column(Integer)
