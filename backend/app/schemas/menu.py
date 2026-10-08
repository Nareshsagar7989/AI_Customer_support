from pydantic import BaseModel
from typing import Optional

# Common properties
class MenuItemBase(BaseModel):
    restaurant_id: int
    category_id: int
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_vegetarian: bool = False
    is_vegan: bool = False
    spice_level: Optional[str] = None
    ingredients: Optional[str] = None
    allergens: Optional[str] = None
    is_available: bool = True
    preparation_time: Optional[int] = None

# Properties required to create an item
class MenuItemCreate(MenuItemBase):
    pass

# Properties returned from the API
class MenuItemResponse(MenuItemBase):
    id: int
    
    class Config:
        from_attributes = True # Converts SQLAlchemy model to Pydantic format
