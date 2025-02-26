from sqlalchemy.orm import Session
from datetime import datetime
from schemas import ProductCreate, ProductUpdate, StockMovementWithItemsCreate, StockCalculationResponse
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

    # Lista para armazenar mensagens de erro
    errors = []

    for item_data in movement_data.items:
        if movement_data.type == 'saída':  # Verificação realizada apenas para movimentações de saída
            current_stock_response = calculate_stock(db, item_data.product_id)
            if item_data.quantity > current_stock_response.current_stock:
                errors.append(f"Not enough stock for product ID {item_data.product_id}. Available: {current_stock_response.current_stock}, Requested: {item_data.quantity}")
                continue  # Pula a adição deste item ao banco de dados

        new_item = StockMovementItemModel(
            movement_id=new_movement.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        db.add(new_item)

    if errors:
        db.rollback()  # Desfaz todas as alterações se houver erros
        return {"error": "Failed to create movement due to stock limitations", "details": errors}

    db.commit()
    return new_movement

def get_stock_movements(db: Session):
    return db.query(StockMovementModel).all()

def get_stock_movement(db: Session, movement_id: int):
    return db.query(StockMovementModel).filter(StockMovementModel.id == movement_id).first()

def delete_stock_movement(db: Session, movement_id: int):
    # Primeiro, obtemos o movimento de estoque
    movement = db.query(StockMovementModel).filter(StockMovementModel.id == movement_id).first()
    
    if movement:
        # Antes de deletar o movimento, deletamos todos os itens associados
        db.query(StockMovementItemModel).filter(StockMovementItemModel.movement_id == movement_id).delete()
        
        # Agora deletamos o movimento
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

def calculate_stock(db: Session, product_id: int):

    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if product:
        # Busca todas as movimentações de entrada para o produto
        entries = db.query(StockMovementItemModel).join(StockMovementModel).filter(
            StockMovementItemModel.product_id == product_id,
            StockMovementModel.type == 'entrada'
        ).all()

        # Busca todas as movimentações de saída para o produto
        exits = db.query(StockMovementItemModel).join(StockMovementModel).filter(
            StockMovementItemModel.product_id == product_id,
            StockMovementModel.type == 'saída'
        ).all()

        # Calcula a quantidade total de entradas
        total_entries = sum(item.quantity for item in entries)

        # Calcula a quantidade total de saídas
        total_exits = sum(item.quantity for item in exits)

        # Calcula o estoque atual subtraindo as saídas das entradas
        stock = total_entries - total_exits

        return StockCalculationResponse(
            product_id=product.id,
            product_name=product.name,
            current_stock=stock,
            description=product.description
        )
    else:
        return {"error": "Product not found"}