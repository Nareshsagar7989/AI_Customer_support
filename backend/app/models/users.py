from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"

RoleEnum = UserRoleEnum

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    password_hash = Column(String(64), nullable=False) # 64-character SHA-256 hash
    role = Column(String(50), default="CUSTOMER")      # "CUSTOMER" or "ADMIN"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String(255))
    phone = Column(String(50))
    email = Column(String(255))
    notes = Column(String(1000))
    total_orders = Column(Integer, default=0)
    total_reservations = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class RestaurantMember(Base):
    __tablename__ = "restaurant_members"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(Enum(RoleEnum))
    created_at = Column(DateTime, default=func.now())
