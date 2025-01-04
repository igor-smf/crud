from sqlalchemy.orm import Session
from models import PolygonData
from schemas import PolygonCreate, PolygonResponse
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape, mapping

def create_polygon(db: Session, polygon: PolygonCreate):
    # Cria um dicionário GeoJSON a partir do modelo Pydantic
    geojson_dict = {
        "type": polygon.geometry.type,
        "coordinates": polygon.geometry.coordinates
    }
    
    # Converte o dicionário GeoJSON em um objeto de geometria Shapely
    shapely_geom = shape(geojson_dict)
    db_polygon = PolygonData(
        name=polygon.name,
        description=polygon.description,
        geometry=from_shape(shapely_geom, srid=4326)  # Converte de Shapely para GeoAlchemy2
    )
    db.add(db_polygon)
    db.commit()
    db.refresh(db_polygon)

    # Converte WKBElement para um objeto de geometria Shapely para a resposta
    shapely_geom = to_shape(db_polygon.geometry)  # Converte WKBElement para geom Shapely diretamente

    # Converte o objeto de geometria Shapely para um dicionário GeoJSON
    geojson = mapping(shapely_geom)

    # Use o GeoJSON convertido na sua resposta
    return PolygonResponse(id=db_polygon.id, name=db_polygon.name, description=db_polygon.description, geometry=geojson)

from shapely.geometry import shape, mapping
from geoalchemy2.shape import to_shape

def get_polygons(db: Session, skip: int = 0, limit: int = 100):
    # Recupera os polígonos do banco de dados
    polygons = db.query(PolygonData).offset(skip).limit(limit).all()
    
    # Converte cada polígono para a resposta adequada
    response = []
    for polygon in polygons:
        # Converte WKBElement para um objeto de geometria Shapely
        shapely_geom = to_shape(polygon.geometry)

        # Converte o objeto de geometria Shapely para um dicionário GeoJSON
        geojson = mapping(shapely_geom)

        # Cria uma instância de PolygonResponse com a geometria convertida
        polygon_response = PolygonResponse(
            id=polygon.id,
            name=polygon.name,
            description=polygon.description,
            geometry=geojson
        )
        response.append(polygon_response)
    
    return response