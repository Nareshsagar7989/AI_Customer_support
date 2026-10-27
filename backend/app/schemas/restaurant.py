from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RestaurantBase(BaseModel):
    name: str
    phone: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = "Asia/Kolkata"
    is_active: bool = True

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None
    is_active: Optional[bool] = None

class RestaurantResponse(RestaurantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
