from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class MenuCategory(Base):
    __tablename__ = "menu_categories"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String(255))
    description = Column(String(1000))
    display_order = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    category_id = Column(Integer, ForeignKey("menu_categories.id"))
    name = Column(String(255))
    description = Column(String(1000))
    price = Column(Float)
    image_url = Column(String(255))
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    spice_level = Column(String(50))
    ingredients = Column(String(1000))
    allergens = Column(String(1000))
    is_available = Column(Boolean, default=True)
    preparation_time = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
