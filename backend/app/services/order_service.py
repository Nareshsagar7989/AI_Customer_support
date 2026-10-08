import uuid
from sqlalchemy.orm import Session
from app.models.transactions import Order, OrderStatusEnum
from app.schemas.orders import OrderCreate

def get_orders(db: Session, restaurant_id: int):
    return db.query(Order).filter(Order.restaurant_id == restaurant_id).all()

def create_order(db: Session, order: OrderCreate):
    # Generate a unique order number
    order_num = "ORD-" + str(uuid.uuid4())[:8].upper()
    db_order = Order(
        **order.model_dump(),
        status=OrderStatusEnum.PLACED,
        order_number=order_num
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status: OrderStatusEnum):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = status
        db.commit()
        db.refresh(order)
    return order
