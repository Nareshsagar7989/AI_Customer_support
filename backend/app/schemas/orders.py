from pydantic import BaseModel
from typing import Optional
from app.models.transactions import OrderTypeEnum, OrderStatusEnum

class OrderBase(BaseModel):
    restaurant_id: int
    customer_id: int
    order_type: OrderTypeEnum
    subtotal: float
    tax: float
    delivery_fee: float = 0.0
    discount: float = 0.0
    total_amount: float
    delivery_address: Optional[str] = None
    payment_status: Optional[str] = "PENDING"

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    order_number: str
    status: OrderStatusEnum
    
    class Config:
        from_attributes = True
