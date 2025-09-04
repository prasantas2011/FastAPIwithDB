from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import schemas,crudservice
from typing import Union

# Create tables (dev only; in prod use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# Category Routes
# -------------------------
@app.post("/categories/", response_model = Union[schemas.CategoryResponse,schemas.ExistMessage])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crudservice.create_category(db, name=category.name)

@app.get("/categories/", response_model=list[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crudservice.get_categories(db, skip, limit)

# -------------------------
# Item Routes
# -------------------------
@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crudservice.create_item(
        db,
        name=item.name,
        description=item.description,
        price=item.price,
        tax=item.tax,
        category_id=item.category_id
    )

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crudservice.get_items(db, skip, limit)

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crudservice.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crudservice.update_item(db, item_id, name=item.name, price=item.price)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crudservice.delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted"}
