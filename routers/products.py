from fastapi import APIRouter, HTTPException, Response, status, Depends
from typing import List
from sqlalchemy.orm import Session

import models
from main import common_parameters
from database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=models.ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: models.ProductBase, db: Session = Depends(get_db)):
    db_product = db.query(models.ProductDB).filter(models.ProductDB.name == product.name).first()
    
    if db_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Product with name '{product.name}' already exists."
            )  

    new_product = models.ProductDB(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[models.ProductSummaryRead])
def get_products(db: Session = Depends(get_db), commons: dict = Depends(common_parameters)):
    skip = commons["skip"]
    limit = commons["limit"]
    products = db.query(models.ProductDB).offset(skip).limit(limit).all()
    return products

@router.put("/products/{product_name}", response_model=models.ProductBase)
def update_product(product_id: str, updated_product_data: models.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.ProductDB).filter(models.ProductDB.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Check if the updated name conflicts with another existing product
    if updated_product_data.name != db_product.name:
        existing_with_new_name = db.query(models.ProductDB).filter(models.ProductDB.name == updated_product_data.name).first()
        if existing_with_new_name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Product with name '{updated_product_data.name}' already exists."
            )

    # Update the fields of the existing product object
    # Use Pydantic's .dict(exclude_unset=True) if you want partial updates
    update_data = updated_product_data.model_dump()
    for key, value in update_data.items():
        setattr(db_product, key, value) # Update attributes dynamically

    db.add(db_product) # Add the updated object back to the session (SQLAlchemy tracks changes)
    db.commit() # Commit changes
    db.refresh(db_product) # Refresh to get updated state if needed
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT) # Delete by ID now
# 1. Inject DB session dependency
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.ProductDB).filter(models.ProductDB.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(db_product) # Mark the object for deletion
    db.commit() # Commit the deletion
    # No body needed for 204 response
    return Response(status_code=status.HTTP_204_NO_CONTENT)
