from pydantic import BaseModel, Field
from typing import List, Union
from pydantic.fields import Field

class GeoJSON(BaseModel):
    type: str = Field(..., description="The type of geometry.")
    coordinates: Union[List[float], List[List[float]], List[List[List[float]]]] = Field(
        ..., description="The coordinates of the geometry.")

class Location(BaseModel):
    name: str
    description: str
    geometry: GeoJSON

external_data = {'name': 'Imovel', 'description': 'teste', 'geometry': GeoJSON(
    type='Polygon',
    coordinates=[[[0.0, 0.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]]]
)}

teste = Location(**external_data)
print(teste.geometry)
