from pydantic import BaseModel
from typing import List, Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemCreate(ItemBase):
    category_id: int

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class Item(ItemBase):
    id: int
    category_id: int

    model_config = {
        "from_attributes": True
    }

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    model_config = {
        "from_attributes": True
    }
class Category(CategoryBase):
    id: int
    items: List[Item] = []

    model_config = {
        "from_attributes": True
    }

class ExistMessage(BaseModel):
    category: Optional[Category] = None
    message: Optional[str] = None