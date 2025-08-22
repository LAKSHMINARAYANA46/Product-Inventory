from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from products import (
    create_product,
    get_product,
    get_products,
    update_product,
    delete_product,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    get_db,  # Ensure get_db is a dependency that provides a Session
    create_product_table,
)

app = FastAPI()

@app.on_event("startup")
def startup():
    create_product_table()

@app.post("/products/", response_model=ProductResponse)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@app.get("/products/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.patch("/products/{product_id}", response_model=ProductResponse)
def update(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated = update_product(db, product_id, product)
    if updated is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@app.delete("/products/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    if not delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}
# Add this to your FastAPI app
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)