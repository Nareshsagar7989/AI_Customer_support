from pydantic import BaseModel
from typing import Optional
from datetime import date, time
from app.models.transactions import ReservationStatusEnum

class ReservationBase(BaseModel):
    restaurant_id: int
    customer_id: int
    table_id: Optional[int] = None
    reservation_date: date
    start_time: time
    end_time: time
    party_size: int
    special_request: Optional[str] = None

class ReservationCreate(ReservationBase):
    pass

class ReservationBookRequest(BaseModel):
    restaurant_id: int = 1
    customer_name: str
    phone: str
    reservation_date: date
    start_time: time
    party_size: int
    special_request: Optional[str] = None

class ReservationResponse(BaseModel):
    id: int
    restaurant_id: int
    customer_id: int
    reservation_date: date
    start_time: time
    end_time: time
    party_size: int
    status: ReservationStatusEnum
    confirmation_code: Optional[str] = None
    special_request: Optional[str] = None
    
    class Config:
        from_attributes = True
