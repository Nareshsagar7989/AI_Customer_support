from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(50))
    title = Column(String(255))
    message = Column(String(1000))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

class WhatsAppIntegration(Base):
    __tablename__ = "whatsapp_integrations"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    phone_number = Column(String(50))
    phone_number_id = Column(String(100))
    business_account_id = Column(String(100))
    access_token = Column(String(500))
    webhook_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
