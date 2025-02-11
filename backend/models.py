# Importações de classes do SQLAlchemy para construir o modelo ORM.
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Importação da classe Base do seu módulo de database; Base é tipicamente criado usando declarative_base().
from database import Base

from datetime import datetime

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    created_at = Column(DateTime(timezone=True), default=func.now())

class StockMovementModel(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True)
    type = Column(String)  # 'entrada' ou 'saída'
    movement_date = Column(DateTime)
    items = relationship("StockMovementItemModel", back_populates="movement")
    """
    Esta linha é usada na classe StockMovementModel para definir um relacionamento entre 
    uma movimentação de estoque e seus itens. Ela diz que cada instância de StockMovementModel 
    pode ter vários StockMovementItemModel associados, acessados pela propriedade items.
    back_populates="movement" garante que a relação seja bidirecional. 
    Isso significa que você pode acessar a movimentação a partir de um item usando a propriedade 
    movement no modelo StockMovementItemModel.

    Suponha que você tenha uma movimentação de estoque que pode incluir vários itens (produtos). 
    Essa relação é um exemplo clássico de um relacionamento "um para muitos", onde uma movimentação 
    (StockMovementModel) pode ter vários itens (StockMovementItemModel) associados a ela.

    Exemplo de uso:

    # Criando uma movimentação de estoque
    new_movement = StockMovementModel(type='entrada', movement_date=datetime.now())

    # Adicionando itens a esta movimentação
    item1 = StockMovementItemModel(product_id=1, quantity=100)
    item2 = StockMovementItemModel(product_id=2, quantity=150)

    # Associando itens à movimentação
    new_movement.items.append(item1)
    new_movement.items.append(item2)

    # Agora, new_movement.items conterá item1 e item2
    """

class StockMovementItemModel(Base):
    __tablename__ = "stock_movement_items"

    id = Column(Integer, primary_key=True)
    movement_id = Column(Integer, ForeignKey('stock_movements.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    movement = relationship("StockMovementModel", back_populates="items")
    product = relationship("ProductModel", back_populates="stock_items")

# Ajuste para relacionar ProductModel com os itens do estoque
ProductModel.stock_items = relationship("StockMovementItemModel", back_populates="product")

if __name__ == '__main__':
    # Suponha que estas instâncias estejam criadas e devidamente relacionadas:
    # Uma movimentação de estoque
    movement = StockMovementModel(type='entrada', movement_date=datetime(2025, 2, 4, 14, 0))

    # Itens associados a esta movimentação
    item1 = StockMovementItemModel(product_id=1, quantity=100, movement=movement)
    item2 = StockMovementItemModel(product_id=2, quantity=200, movement=movement)

    # Adicionando itens à movimentação
    movement.items = [item1, item2]

    # Agora vamos acessar a movimentação a partir de um dos itens, digamos item1
    related_movement = item1.movement

    # Exibindo informações sobre a movimentação
    print(f"Tipo de Movimentação: {related_movement.type}")
    print(f"Data da Movimentação: {related_movement.movement_date.strftime('%Y-%m-%d %H:%M:%S')}")