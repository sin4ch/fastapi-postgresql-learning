from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String , Float, Boolean
from sqlalchemy.orm import relationship
from database import Base

class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    tax = Column(Float, nullable=True)

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    class Config:
        orm_mode = True

class ProductSummary(BaseModel):
    id: int
    name: str
    price: float
