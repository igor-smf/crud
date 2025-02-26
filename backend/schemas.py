from pydantic import BaseModel, PositiveFloat, Field, PositiveInt 
from datetime import datetime
from typing import Optional, List

# Modelos para Produtos
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: PositiveFloat

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    """
    from_attributes  = True permite que o Pydantic trate objetos ORM 
    (como aqueles retornados pelo SQLAlchemy) como dicionários, facilitando a serialização.

    A serialização refere-se ao processo de converter objetos complexos do SQLAlchemy 
    (que são instâncias de classes de modelo representando dados do banco de dados) 
    em um formato mais simples, como JSON, que pode ser enviado através de uma API para 
    um cliente ou consumidor.
    """
    class Config:
        from_attributes  = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None

# Modelos para Movimentações de Estoque
class StockMovementBase(BaseModel):
    type: str  # 'entrada' ou 'saída'
    movement_date: datetime

class StockMovementCreate(StockMovementBase):
    items: List[dict] = Field(default_factory=list)
"""
Campo items
Tipo de Dados: List[dict]
    Função: Este campo armazena uma lista de dicionários, onde cada dicionário representa um item 
    da movimentação de estoque. Cada item incluirá pelo menos um product_id e uma quantity, mas pode 
    incluir outros dados relevantes para a movimentação.
Por que List[dict]?
    O uso de List[dict] aqui permite que a lista de itens seja flexível quanto às propriedades que 
    cada item pode ter. Por exemplo, além de product_id e quantity, cada item poderia potencialmente 
    incluir informações adicionais como batch_number, expiry_date, etc., dependendo das necessidades 
    específicas do seu sistema de gerenciamento de estoque.
Uso de Field(default_factory=list)
    Field: É uma função do Pydantic que é usada para fornecer configurações adicionais sobre os 
    campos do modelo. Aqui, ela é utilizada para especificar um valor padrão para o campo.
    default_factory: Quando você utiliza default_factory, você deve passar uma função que o 
    Pydantic pode chamar para obter um valor padrão para o campo. No caso de default_factory=list, 
    isso indica que o valor padrão para items é uma lista vazia. Isso é útil porque assegura que 
    items nunca será None; em vez disso, será uma lista vazia se nenhum item for especificado, 
    o que ajuda a prevenir erros de tipo durante a manipulação dos dados.
"""

class StockMovementItemBase(BaseModel):
    product_id: int
    quantity: PositiveInt

class StockMovementResponse(BaseModel):
    id: int
    type: str
    movement_date: datetime
    items: List[StockMovementItemBase]

    class Config:
        from_attributes  = True

# Este modelo é utilizado para adicionar itens a uma movimentação já existente.
class StockMovementItemCreate(StockMovementItemBase):
    pass

# Este modelo é utilizado para criar uma nova movimentação de estoque com os itens incluídos.
class StockMovementWithItemsCreate(StockMovementBase):
    items: List[StockMovementItemCreate]

class StockCalculationResponse(BaseModel):
    product_id: int
    product_name: Optional[str] = None
    current_stock: int
    description: Optional[str] = None

    class Config:
        from_attributes = True

class Error(BaseModel):
    error: str
    details: List[str]