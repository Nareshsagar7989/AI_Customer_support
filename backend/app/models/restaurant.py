from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Time
from sqlalchemy.sql import func
from app.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(1000))
    logo_url = Column(String(255))
    phone = Column(String(50))
    email = Column(String(255))
    website = Column(String(255))
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class BusinessHour(Base):
    __tablename__ = "business_hours"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    day_of_week = Column(String(20))
    opening_time = Column(Time)
    closing_time = Column(Time)
    is_closed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    table_number = Column(String(50))
    capacity = Column(Integer)
    location = Column(String(100))
    status = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
