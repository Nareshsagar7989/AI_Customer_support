from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Date, Time, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class OrderTypeEnum(enum.Enum):
    DINE_IN = "DINE_IN"
    TAKEAWAY = "TAKEAWAY"
    DELIVERY = "DELIVERY"

class OrderStatusEnum(enum.Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class ReservationStatusEnum(enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    NO_SHOW = "NO_SHOW"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_number = Column(String(100), unique=True)
    order_type = Column(Enum(OrderTypeEnum))
    status = Column(Enum(OrderStatusEnum))
    subtotal = Column(Float)
    tax = Column(Float)
    delivery_fee = Column(Float)
    discount = Column(Float)
    total_amount = Column(Float)
    delivery_address = Column(String(1000))
    payment_status = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)
    special_instructions = Column(String(1000))
    created_at = Column(DateTime, default=func.now())

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    table_id = Column(Integer, ForeignKey("restaurant_tables.id"), nullable=True)
    reservation_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    party_size = Column(Integer)
    status = Column(Enum(ReservationStatusEnum))
    special_request = Column(String(1000))
    confirmation_code = Column(String(100))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
