from fastapi import APIRouter, HTTPException, Response, status, Depends
from typing import List
import models

products_db = []
router = APIRouter()

@router.post("/products", response_model=models.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: models.Product):
    for existing_products in products_db:
        if existing_products.name == product.name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"Product with name '{product.name}' already exists."
                )  
    products_db.append(product)
    return product

@router.get("/products", response_model=List[models.ProductSummary])
def get_products():
    return products_db

@router.put("/products/{product_name}", response_model=models.Product)
def update_product(product_name: str, updated_product: models.Product):
    for index, existing_product in enumerate(products_db):
        if existing_product.name == product_name:
            products_db[index] = updated_product
            return updated_product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with name '{product_name}' doesn't exist."
    )

@router.delete("/products/{product_name}")
def delete_product(product_name: str):
    for index, existing_product in enumerate(products_db):
        if existing_product.name == product_name:
            products_db.pop(index)          
            return Response(status_code=status.HTTP_204_NO_CONTENT)    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with name '{product_name}' not found in the database."
    )