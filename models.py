from sqlalchemy import Column, Integer, String, ForeignKey, Identity, Date
from database import Base


# CLIENTS
class Client(Base):
    __tablename__ = "clients"

    c_id = Column(Integer, Identity(start=1), primary_key=True)
    c_name = Column(String(50))
    c_lastname = Column(String(50))
    c_tel = Column(String(50))


# ADDITIONAL SERVICES
class AdditionalService(Base):
    __tablename__ = "additional_services"

    as_id = Column(Integer, Identity(start=1), primary_key=True)
    as_name = Column(String(50))
    as_cost = Column(Integer)


# ROOMS
class Room(Base):
    __tablename__ = "rooms"

    n_id = Column(Integer, Identity(start=1), primary_key=True)
    n_count = Column(Integer)
    n_type = Column(String(50))
    n_cost = Column(Integer)
    n_st = Column(String(50))


# ADMINS
class Admin(Base):
    __tablename__ = "admins"

    a_id = Column(Integer, Identity(start=1), primary_key=True)
    a_name = Column(String(50))
    a_lastname = Column(String(50))
    a_login = Column(String(50))
    a_password = Column(String(50))
    a_st = Column(String(50))


# RESERVATIONS
class Reservation(Base):
    __tablename__ = "reservations"

    r_id = Column(Integer, Identity(start=1), primary_key=True)

    a_id = Column(Integer, ForeignKey("admins.a_id"))
    c_id = Column(Integer, ForeignKey("clients.c_id"))
    n_id = Column(Integer, ForeignKey("rooms.n_id"))
    as_id = Column(Integer, ForeignKey("additional_services.as_id"))

    r_datearrival = Column(Date)
    r_datedeparture = Column(Date)
    r_st = Column(String(50))