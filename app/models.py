from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, server_default='customer', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()')) 

class Service(Base):
    __tablename__ = "services"
     
    id = Column(Integer,primary_key=True ,nullable=False)
    name = Column(String, nullable=False)  
    price = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)

class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True,nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"),nullable=False)
    service_id = Column(Integer, ForeignKey(
        "services.id", ondelete="CASCADE"),nullable=False)
    appointment_time = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(String, server_default="pending", nullable=False )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Invoices(Base):
    __tablename__ = "invoices"

    id = Column(Integer,primary_key=True,nullable=False)
    booking_id = Column(Integer, ForeignKey(
        "bookings.id", ondelete="CASCADE"), nullable=False
    )
    total_amount = Column(Float,nullable=False)
    status = Column(String, nullable=False, default="unpaid")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= func.now())

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer,primary_key=True,nullable=False)
    invoice_id = Column(Integer, ForeignKey(
        "invoices.id", ondelete="CASCADE"),nullable=False)
    amount_paid =  Column(Float,nullable=False)
    payment_method = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= func.now())
    


