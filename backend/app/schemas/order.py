from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from .menu import MenuItemResponse

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int

class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    item_price: Decimal
    menu_item: MenuItemResponse

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    delivery_address: str
    notes: Optional[str] = None
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemBase]

class OrderResponse(OrderBase):
    id: int
    tracking_id: Optional[str] = None
    status: str
    total_amount: Decimal
    created_at: datetime
    customer_id: Optional[int] = None
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str

Order = OrderResponse
OrderItem = OrderItemResponse
OrderItemCreate = OrderItemBase
