from sqlalchemy.orm import Session
from models import Item, Category
from schemas import ExistMessage, CategoryResponse
from typing import Union
from fastapi import HTTPException

# -------------------------
# Category CRUD
# -------------------------
def create_category(db: Session, name: str)-> Union[CategoryResponse, ExistMessage]:
     # Check if category already exists
    existing_category = db.query(Category).filter(Category.name == name).first()
    if existing_category:
        return ExistMessage(message="Category already exists")
    # or
    # existing = db.query(Category).filter(Category.name == name).first()
    # if existing:
    #     raise HTTPException(status_code=400, detail="Category already exists")
    #or
    # category = db.query(Category).filter(Category.name == name).first()
    # if category:
    #     return category
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

# -------------------------
# Item CRUD
# -------------------------
def create_item(db: Session, name: str, description: str, price: float, category_id: int, tax: float = None):
    item = Item(name=name, description=description, price=price, tax=tax, category_id=category_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def update_item(db: Session, item_id: int, name: str = None, price: float = None):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return None
    if name:
        item.name = name
    if price is not None:
        item.price = price
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item
