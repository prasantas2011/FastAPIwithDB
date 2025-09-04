from modelstortoise import *
from schemastortoise import *
from typing import Union,List

async def create_category_service(name: str) -> Union[Category_Pydantic, ExistMessage]:
    # Check for existing category
    existing = await Category.filter(name=name).first()
    if existing:
        return ExistMessage(detail="Category already exists")

    category = await Category.create(name=name)
    return await Category_Pydantic.from_tortoise_orm(category)

async def get_categories_service(skip: int = 0, limit: int = 100) -> List[Category_Pydantic]:
    categories = Category.all().offset(skip).limit(limit)
    return await Category_Pydantic.from_queryset(categories)

async def get_items(skip: int = 0, limit: int = 100) -> List[Item_Pydantic]:
    items = Item.all().offset(skip).limit(limit)
    return await Item_Pydantic.from_queryset(items)

async def create_item_service(
    name: str,
    description: str,
    price: float,
    tax: float | None,
    category_id: int
) -> Union[Item_Pydantic, ExistMessage]:
    # Check if category exists
    category = await Category.filter(id=category_id).first()
    if not category:
        return ExistMessage(detail="Category does not exist")

    # Optional: Check if item with same name in this category exists
    existing_item = await Item.filter(name=name, category_id=category_id).first()
    if existing_item:
        return ExistMessage(detail="Item already exists in this category")

    # Create new item
    item = await Item.create(
        name=name,
        description=description,
        price=price,
        tax=tax,
        category_id=category_id
    )
    return await Item_Pydantic.from_tortoise_orm(item)

async def update_item_service(
    item_id: int,
    name: str | None = None,
    description: str | None = None,
    price: float | None = None,
    tax: float | None = None,
    category_id: int | None = None
) -> Union[Item_Pydantic, ExistMessage]:
    
    item = await Item.filter(id=item_id).first()
    if not item:
        return ExistMessage(detail="Item not found")
    
    # Optional: check if new category exists
    if category_id:
        category = await Category.filter(id=category_id).first()
        if not category:
            return ExistMessage(detail="Category does not exist")
        item.category_id = category_id
    
    # Update fields if provided
    if name is not None:
        item.name = name
    if description is not None:
        item.description = description
    if price is not None:
        item.price = price
    if tax is not None:
        item.tax = tax

    await item.save()
    return await Item_Pydantic.from_tortoise_orm(item)

async def delete_item_service(item_id: int) -> Union[bool, ExistMessage]:
    item = await Item.filter(id=item_id).first()
    if not item:
        return ExistMessage(detail="Item not found")
    
    await item.delete()
    return True