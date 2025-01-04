from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import PolygonResponse, PolygonCreate
from typing import List
from crud import (
    create_polygon,
    get_polygons,
)

router = APIRouter()


@router.get("/geodata/", response_model=List[PolygonResponse])
def read_all_geodata_route(db: Session = Depends(get_db)):
    """Retrieve all geodata entries from the database."""
    geodata = get_polygons(db)
    return geodata

@router.post("/geodata/", response_model=PolygonResponse)
def create_geodata_route(geodata: PolygonCreate, db: Session = Depends(get_db)):
    """Create a new geodata entry from the provided geodata."""
    return create_polygon(db, geodata)
