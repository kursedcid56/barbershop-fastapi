from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic.v1 import EmailStr
from enum import Enum

class PaymentMethodEnum(str, Enum):
    CASH = "cash"
    BANKING = "banking"

class StatusEnom(str,Enum):
    PAID = "paid"
    UNPAID ="unpaid"
    PARTIAL = "partial"



class UserBase(BaseModel):
    name: str
    phone_number: str

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "customer"

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdate(UserBase):
    pass    

class UserLogin(UserCreate):
    pass

class UserOut(BaseModel):
    id: int
    name: str
    phone_number: str
    role: Optional[str] = "customer"


class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class ServiceBase(BaseModel):
    name: str
    price: int
    duration_minutes: int

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class ServiceOut(ServiceBase):
    id: int

class ServiceResponse(ServiceBase):
    id: int
    
    model_config = {"from_attributes": True}

class BookingCreate(BaseModel):
    service_id: int
    appointment_time: datetime

class BookingOut(BaseModel):
    id:int
    user_id: int
    service_id: int
    appointment_time: datetime
    status: str
    created_at: datetime

    model_config = {"from_attributes": True} 

class BookingUpdate(BaseModel):
    service_id: Optional[int] = None
    appointment_time: Optional[datetime] = None    

class BookingStateUpdate(BaseModel):
    status: str


class InvoiceOut(BaseModel):
    id: int
    booking_id: int
    total_amount: float
    created_at: datetime
    status: StatusEnom
    model_config = {"from_attributes": True}

class PaymenCreate(BaseModel):
    invoice_id:int
    amount_paid:float
    payment_method: PaymentMethodEnum    

class PaymentOut(BaseModel):
    id:int
    invoice_id:int
    amount_paid: float
    created_at: datetime
    payment_method: PaymentMethodEnum

    model_config = {"from_attributes": True}










