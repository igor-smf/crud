from sqlalchemy import Column, Integer, String
from database import Base
from geoalchemy2 import Geometry

class PolygonData(Base):
    __tablename__ = "polygon_data"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    geometry = Column(Geometry(geometry_type='GEOMETRY', srid=4326))
