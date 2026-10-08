from sqlalchemy.orm import Session
from app.models.menu import MenuItem
from app.schemas.menu import MenuItemCreate

def get_menu_items(db: Session, restaurant_id: int):
    # Get all menu items for a specific restaurant
    return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()

def create_menu_item(db: Session, item: MenuItemCreate):
    # Convert Pydantic object to SQLAlchemy model dictionary using model_dump()
    db_item = MenuItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
