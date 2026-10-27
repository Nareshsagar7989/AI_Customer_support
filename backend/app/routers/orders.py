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

from typing import List, Optional
from app.models.transactions import Order, OrderItem, OrderStatusEnum
from app.models.menu import MenuItem
from app.models.users import Customer

@router.get("/history/list")
def get_order_history(phone: Optional[str] = None, db: Session = Depends(get_db)):
    """Fetches past orders with item details. If phone is supplied, filters by customer."""
    query = db.query(Order)
    
    if phone and phone.strip():
        clean_phone = phone.strip()
        cust_ids = [c.id for c in db.query(Customer).filter(Customer.phone == clean_phone).all()]
        if cust_ids:
            query = query.filter(
                (Order.customer_id.in_(cust_ids)) | (Order.delivery_address.contains(clean_phone))
            )
        else:
            query = query.filter(Order.delivery_address.contains(clean_phone))

    orders = query.order_by(Order.id.desc()).all()
    results = []

    for ord in orders:
        # Fetch items for this order
        order_items = db.query(OrderItem).filter(OrderItem.order_id == ord.id).all()
        items_list = []
        for oi in order_items:
            m_item = db.query(MenuItem).filter(MenuItem.id == oi.menu_item_id).first()
            items_list.append({
                "name": m_item.name if m_item else "Special Dish",
                "quantity": oi.quantity,
                "unit_price": oi.unit_price,
                "total_price": oi.total_price
            })

        results.append({
            "id": ord.id,
            "order_number": ord.order_number,
            "order_type": ord.order_type.value if hasattr(ord.order_type, "value") else str(ord.order_type),
            "status": ord.status.value if hasattr(ord.status, "value") else str(ord.status),
            "subtotal": ord.subtotal or 0.0,
            "tax": ord.tax or 0.0,
            "delivery_fee": ord.delivery_fee or 0.0,
            "total_amount": ord.total_amount or 0.0,
            "delivery_address": ord.delivery_address or "Spice Garden Dine-in",
            "payment_status": ord.payment_status or "PAID",
            "created_at": ord.created_at.strftime("%I:%M %p, %d %b %Y") if ord.created_at else "Just now",
            "items": items_list
        })

    return results

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_status(order_id: int, status: OrderStatusEnum, db: Session = Depends(get_db)):
    order = order_service.update_order_status(db, order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
