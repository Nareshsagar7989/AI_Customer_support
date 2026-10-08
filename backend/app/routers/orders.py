from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.orders import OrderCreate, OrderResponse
from app.services import order_service
from app.models.transactions import OrderStatusEnum

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, order)

@router.get("/{restaurant_id}", response_model=List[OrderResponse])
def get_orders(restaurant_id: int, db: Session = Depends(get_db)):
    return order_service.get_orders(db, restaurant_id)

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_status(order_id: int, status: OrderStatusEnum, db: Session = Depends(get_db)):
    order = order_service.update_order_status(db, order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
