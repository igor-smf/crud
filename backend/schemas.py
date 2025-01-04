"""
Importa BaseModel da biblioteca Pydantic, que é usado para criar classes de validação de dados.
Optional, List, Union são tipos de dados usados para especificar o tipo de um atributo, 
como listas ou valores opcionais.
"""
from pydantic import BaseModel
from typing import Optional
from shapely.geometry import mapping, Polygon
from typing import List, Union
from pydantic.fields import Field

class GeoJSON(BaseModel):
    type: str = Field(..., description="The type of geometry.")
    coordinates: Union[List[float], List[List[float]], List[List[List[float]]]] = Field(
        ..., description="The coordinates of the geometry.")
    
"""
PolygonBase: Define a base de um polígono com nome, descrição opcional e geometria. 
A geometria é tratada como um dicionário, representando dados em formato GeoJSON.
PolygonCreate: Um modelo simples que herda de PolygonBase sem adições, usado para a criação 
de novos registros.
"""

class PolygonBase(BaseModel):
    name: str
    description: Optional[str] = None
    geometry: GeoJSON  # Armazena como dicionário

class PolygonCreate(PolygonBase):
    pass

"""
PolygonResponse: Inclui campos adicionais como id, que são típicos de dados 
retornados de um banco de dados. orm_mode = True permite que o Pydantic trate objetos ORM 
(como aqueles retornados pelo SQLAlchemy) como dicionários, facilitando a serialização.
"""
class PolygonResponse(PolygonBase):
    id: int

    class Config:
        from_attributes = True