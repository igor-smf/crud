from sqlalchemy.orm import Session
from datetime import datetime
from schemas import ProductCreate, ProductUpdate, StockMovementWithItemsCreate
from models import ProductModel, StockMovementModel, StockMovementItemModel

# Funções CRUD para Produtos
def create_product(db: Session, product_data: ProductCreate):
    new_product = ProductModel(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_product(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

def get_products(db: Session):
    return db.query(ProductModel).all()

def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product:
        product.name = product_data.name if product_data.name else product.name
        product.description = product_data.description if product_data.description else product.description
        product.price = product_data.price if product_data.price else product.price
        db.commit()
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product

# Funções CRUD para Movimentações de Estoque
def create_stock_movement(db: Session, movement_data: StockMovementWithItemsCreate):
    new_movement = StockMovementModel(
        type=movement_data.type,
        movement_date=movement_data.movement_date
    )
    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    for item_data in movement_data.items:
        new_item = StockMovementItemModel(
            movement_id=new_movement.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        db.add(new_item)
    db.commit()
    return new_movement

def get_stock_movements(db: Session):
    return db.query(StockMovementModel).all()

def get_stock_movement(db: Session, movement_id: int):
    return db.query(StockMovementModel).filter(StockMovementModel.id == movement_id).first()

def delete_stock_movement(db: Session, movement_id: int):
    movement = db.query(StockMovementModel).filter(StockMovementModel.id == movement_id).first()
    if movement:
        db.delete(movement)
        db.commit()
    return movement

def update_stock_movement(db: Session, movement_id: int, movement_data: StockMovementWithItemsCreate):
    movement = db.query(StockMovementModel).filter(StockMovementModel.id == movement_id).first()
    if movement:
        movement.type = movement_data.type
        movement.movement_date = movement_data.movement_date
        db.commit()
    return movement
