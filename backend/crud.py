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
    
    """
    GeoJSON para Shapely: O GeoJSON é um formato de intercâmbio de dados geográficos amplamente
      utilizado em aplicações web e APIs. No entanto, para manipulação geométrica mais complexa,
        muitas bibliotecas Python, como Shapely, não trabalham diretamente com GeoJSON. 
        Shapely é excelente para manipular formas, calcular áreas, verificar interseções, etc., 
        mas necessita dos dados em seu próprio formato de objeto geométrico. 
        A conversão do GeoJSON para objetos Shapely permite aproveitar essas funcionalidades.
    """
    shapely_geom = shape(geojson_dict)

    db_polygon = PolygonData(
        name=polygon.name,
        description=polygon.description,
        geometry=from_shape(shapely_geom, srid=4326)  # Converte de Shapely para GeoAlchemy2
    )
    """
    Shapely para GeoAlchemy2: GeoAlchemy2 estende o SQLAlchemy para suportar tipos geométricos 
    em bancos de dados, como PostGIS (uma extensão do PostgreSQL). Contudo, 
    GeoAlchemy2 trabalha com formatos específicos como WKT (Well-Known Text) e 
    WKB (Well-Known Binary), que são formatos padrões em sistemas de banco de dados espaciais. 
    Shapely não produz diretamente esses formatos, então a conversão é necessária para 
    armazenar as geometrias no banco de dados.
    """
    db.add(db_polygon)
    db.commit()
    db.refresh(db_polygon)

    # Converte WKBElement para um objeto de geometria Shapely para a resposta
    shapely_geom = to_shape(db_polygon.geometry)  # Converte WKBElement para geom Shapely diretamente

    # Converte o objeto de geometria Shapely para um dicionário GeoJSON
    geojson = mapping(shapely_geom)

    # Use o GeoJSON convertido na sua resposta
    return PolygonResponse(id=db_polygon.id, name=db_polygon.name, description=db_polygon.description, geometry=geojson)

def get_polygons(db: Session, skip: int = 0, limit: int = 100):
    
    """
    skip: Define o número de registros a serem pulados antes de começar a retornar os 
    resultados. Isso é útil para navegar pelas páginas de resultados. 
    Por exemplo, se skip for 30, os primeiros 30 registros serão ignorados, e a contagem 
    começará a partir do 31º registro.
    
    limit: Limita o número de registros retornados pela consulta. 
    Isso controla quantos registros são mostrados em uma única página ou chamada de API. 
    Por exemplo, se limit for 10, apenas 10 registros serão retornados.
    """
    
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