from typing import Optional, List
from enum import Enum
import time

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None
    is_on_sale: bool = False


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(
    *,
    item_id: int = Path(..., title="The ID of the item", gt=2),
    q: str,
):
    return {"item_id": item_id, "q": q}


@app.get("/items")
async def read_items(q: Optional[List[str]] = Query(['a', 'b'])):
    query_items = {"q": q}
    return query_items


@app.put("/item/{item_id}")
def update_item(item_id: int, item: Item):
    new_name = item.name.capitalize()
    return {"item_id": item_id, "item": item, "new_name": new_name}
    # return {"item_name": item.name, "item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep learning 1"}
    return {"model_name": model_name, "message": "Not suported"}
