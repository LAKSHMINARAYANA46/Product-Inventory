from sqlalchemy import Column, Integer, String
from database import Base, get_db
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional


# --------------------
# SQLAlchemy Model
# --------------------
class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False, unique=True)
    product_quantity = Column(Integer, nullable=False)
    product_price = Column(Integer, nullable=False)


# --------------------
# Pydantic Models
# --------------------
class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=255, description="Product name is required")
    product_quantity: int = Field(1, ge=1, le=1000, description="Product quantity is required")
    product_price: float = Field(..., ge=1, description="Product Price is required")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field(None, min_length=1, max_length=255)
    product_quantity: Optional[int] = Field(None, ge=1, le=1000)
    product_price: Optional[int] = Field(None, ge=1)

class ProductResponse(ProductBase):
    product_id: int

    class Config:
        from_attributes = True


# --------------------
# Ensure Table Creation
# --------------------
def create_product_table():
    try:
        from database import engine
        from sqlalchemy import inspect
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        if "products" not in existing_tables:
            Base.metadata.tables["products"].create(bind=engine, checkfirst=True)
    except Exception:
        pass  # No logging


# --------------------
# CRUD Operations
# --------------------
def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(
        product_name=product.product_name,
        product_quantity=product.product_quantity,
        product_price=product.product_price,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.product_id == product_id).first()

#this functions gets the recent 3 products
def get_products(db: Session, skip: int = 0, limit: int = 3) -> List[Product]:
    return (
        db.query(Product)
        .order_by(Product.product_id.desc())  # Order by newest first
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if not db_product:
        return None

    update_data = product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True

