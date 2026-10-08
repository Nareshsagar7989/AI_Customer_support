from fastapi import APIRouter, Depends
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

@router.get("/{restaurant_id}", response_model=List[MenuItemResponse])
def get_restaurant_menu(restaurant_id: int, db: Session = Depends(get_db)):
    return menu_service.get_menu_items(db, restaurant_id)
