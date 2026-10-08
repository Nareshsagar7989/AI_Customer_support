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

class ReservationResponse(ReservationBase):
    id: int
    status: ReservationStatusEnum
    confirmation_code: Optional[str] = None
    
    class Config:
        from_attributes = True
