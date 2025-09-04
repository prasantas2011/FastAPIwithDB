from tortoise.contrib.pydantic import pydantic_model_creator
from modelstortoise import Category, Item
from pydantic import BaseModel,Field
from typing import Optional

Category_Pydantic = pydantic_model_creator(Category, name="Category")
Item_Pydantic = pydantic_model_creator(Item, name="Item")

class ItemCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    category_id: int

    model_config = {
        "from_attributes": True  # Required for Pydantic v2 + ORM objects
    }

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None
    category_id: Optional[int] = None

    model_config = {"from_attributes": True}
    
class ExistMessage(BaseModel):
    detail: str
