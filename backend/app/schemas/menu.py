from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_available: bool = True

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(MenuItemBase):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    is_available: Optional[bool] = None

class MenuItemResponse(MenuItemBase):
    id: int
    category: Optional[str] = None

    class Config:
        from_attributes = True

MenuItem = MenuItemResponse
