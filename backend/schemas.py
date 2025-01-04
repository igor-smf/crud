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
PolygonBase: Este modelo define os campos básicos que todos os registros de Polygon terão, 
incluindo nome, descrição e geometria. A geometria é tratada como um dicionário, 
assumindo que os dados são recebidos e enviados em formato GeoJSON.
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

"""
PolygonUpdate: Permite atualizações parciais dos dados, onde todos os campos são opcionais. 
Isso é útil para APIs que suportam atualizações PATCH, permitindo que os usuários modifiquem 
somente certos campos de um registro existente.
"""
# class PolygonUpdate(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     geometry: Optional[dict] = None