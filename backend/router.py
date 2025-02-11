from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import ProductResponse, ProductUpdate, ProductCreate, StockMovementWithItemsCreate, StockMovementResponse
from typing import List
from crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product,
    create_stock_movement,
    get_stock_movements,
    get_stock_movement,
    delete_stock_movement,
    update_stock_movement,
)

router = APIRouter()

# Rotas para produtos
@router.post("/products/", response_model=ProductResponse)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)

@router.get("/products/", response_model=List[ProductResponse])
def read_all_products_route(db: Session = Depends(get_db)):
    products = get_products(db)
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_route(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    db_product = update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Rotas para movimentações de estoque
@router.post("/stock-movements/", response_model=StockMovementResponse)
def create_stock_movement_route(movement: StockMovementWithItemsCreate, db: Session = Depends(get_db)):
    return create_stock_movement(db=db, movement_data=movement)

@router.get("/stock-movements/", response_model=List[StockMovementResponse])
def read_all_stock_movements_route(db: Session = Depends(get_db)):
    movements = get_stock_movements(db)
    return movements

@router.get("/stock-movements/{movement_id}", response_model=StockMovementResponse)
def read_stock_movement_route(movement_id: int, db: Session = Depends(get_db)):
    movement = get_stock_movement(db, movement_id=movement_id)
    if movement is None:
        raise HTTPException(status_code=404, detail="Stock movement not found")
    return movement

@router.delete("/stock-movements/{movement_id}", response_model=StockMovementResponse)
def delete_stock_movement_route(movement_id: int, db: Session = Depends(get_db)):
    movement = delete_stock_movement(db, movement_id=movement_id)
    if movement is None:
        raise HTTPException(status_code=404, detail="Stock movement not found")
    return movement

@router.put("/stock-movements/{movement_id}", response_model=StockMovementResponse)
def update_stock_movement_route(
    movement_id: int, movement: StockMovementWithItemsCreate, db: Session = Depends(get_db)
):
    updated_movement = update_stock_movement(db, movement_id=movement_id, movement_data=movement)
    if updated_movement is None:
        raise HTTPException(status_code=404, detail="Stock movement not found")
    return updated_movement
