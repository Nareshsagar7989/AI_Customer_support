from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.menu import MenuItemCreate, MenuItemResponse
from app.services import menu_service

router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)

@router.post("/", response_model=MenuItemResponse)
def add_menu_item(item: MenuItemCreate, db: Session = Depends(get_db)):
    return menu_service.create_menu_item(db, item)

@router.get("/categories/{restaurant_id}")
def get_categories(restaurant_id: int, db: Session = Depends(get_db)):
    """Fetch categories dynamically from MySQL menu_categories table."""
    categories = menu_service.get_categories(db, restaurant_id)
    return [{"id": c.id, "name": c.name} for c in categories]

@router.get("/{restaurant_id}", response_model=List[MenuItemResponse])
def get_restaurant_menu(restaurant_id: int, db: Session = Depends(get_db)):
    return menu_service.get_menu_items(db, restaurant_id)

@router.delete("/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    success = menu_service.delete_menu_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return {"message": "Menu item deleted successfully"}
