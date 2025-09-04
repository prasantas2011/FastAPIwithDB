from fastapi import FastAPI,HTTPException
from tortoise.contrib.fastapi import register_tortoise
from schemastortoise import Category_Pydantic, ExistMessage
from servicestortoise import *
from typing import Union
from typing import List

app = FastAPI()

@app.post("/categories/", response_model=Union[Category_Pydantic, ExistMessage])
async def create_category(name: str):
    return await create_category_service(name=name)

@app.get("/categories/", response_model=List[Category_Pydantic])
async def read_categories(skip: int = 0, limit: int = 100):
    return await get_categories_service(skip=skip, limit=limit)


@app.post("/items/", response_model=Union[Item_Pydantic, ExistMessage])
async def create_item(item: ItemCreate):
    return await create_item_service(
        name=item.name,
        description=item.description,
        price=item.price,
        tax=item.tax,
        category_id=item.category_id
    )

@app.get("/items/", response_model=List[Item_Pydantic])
async def read_items(skip: int = 0, limit: int = 100):
    return await get_items(skip=skip, limit=limit)

@app.put("/items/{item_id}", response_model=Union[Item_Pydantic, ExistMessage])
async def update_item(item_id: int, item: ItemUpdate):
    res = await update_item_service(
        item_id=item_id,
        name=item.name,
        description=item.description,
        price=item.price,
        tax=item.tax,
        category_id=item.category_id
    )
    if isinstance(res, ExistMessage):
        raise HTTPException(status_code=404, detail=res.detail)
    return res

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    res = await delete_item_service(item_id)
    if isinstance(res, ExistMessage):
        raise HTTPException(status_code=404, detail=res.detail)
    return {"detail": "Item deleted"}

# Tortoise ORM initialization
register_tortoise(
    app,
    db_url="sqlite://test2.db",
    modules={"models": ["modelstortoise"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
