import fastapi
from fastapi import Depends
from typing import Optional

from routers import products

from database import Base, engine
import models
import dependencies

Base.metadata.create_all(bind=engine)

app = fastapi.FastAPI()

app.include_router(products.router)

@app.get("/")
def say_hello():
    return {"message": "Hello, World"}

@app.get("/hello/{name}")
def say_hello_to_person(name: str):
    return {"message": f"Hello, {name}"}

@app.get("/items")
def get_items(commons: dict = Depends(dependencies.common_parameters)):
    skip = commons["skip"]
    limit = commons["limit"]
    all_items = ["carrots", "cabbages", "fruits", "spinach", "brussel sprouts", "onions", "green pepper", "salt", "thyme", "curry", "ground pepper", "paprika"]
    start = skip
    if limit is None:
        end = len(all_items)
    else:
        end = start + limit
    new_items = all_items[start:end]
    
    return {"items": new_items}