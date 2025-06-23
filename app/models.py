

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List


class Base(DeclarativeBase):
    pass 

db = SQLAlchemy(model_class=Base)


#==================================================


class Customer(Base):   
    __tablename__="customers"
        
    id:Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False)
    address: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(255),nullable=False)
    salary: Mapped[int] = mapped_column(nullable=False)
    password:Mapped[str] = mapped_column(db.String(255), nullable=False)
    
    service:Mapped[List["ServiceTickets"]]=db.relationship(back_populates="customers")

service_mechanic=db.Table(
    "service_mechanic",
    Base.metadata,
    db.Column("service_id",db.ForeignKey("service.id")),
    db.Column("mechanic_id",db.ForeignKey("mechanics.id"))
)
   
class ServiceTickets(Base):
    __tablename__="service"
    
    id:Mapped[int]=mapped_column(primary_key=True)
    mileage:Mapped[int]=mapped_column(nullable=False)
    VIN:Mapped[str]=mapped_column(db.String(225),nullable=False)
    customer_id:Mapped[int]=mapped_column(db.ForeignKey("customers.id"))
    
    customers:Mapped["Customer"]=db.relationship(back_populates="service")
    mechanics:Mapped[List["Mechanics"]]=db.relationship(secondary=service_mechanic,back_populates="service")
  
class Mechanics(Base):
    __tablename__="mechanics"
    
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(db.String(225),nullable=False)
    experiance:Mapped[int]=mapped_column(nullable=False)
  
    service:Mapped[List["ServiceTickets"]]=db.relationship(secondary=service_mechanic,back_populates="mechanics")
 