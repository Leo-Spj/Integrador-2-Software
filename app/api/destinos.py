from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import Destino, DestinoCreate, DestinoUpdate
from app.crud import crud_destino

router = APIRouter()


@router.post("/destinos/", response_model=Destino)
def crear_destino(destino: DestinoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo destino turístico
    """
    return crud_destino.create_destino(db=db, destino=destino)


@router.get("/destinos/", response_model=List[Destino])
def listar_destinos(skip: int = 0, limit: int = 100, disponible: bool = True, db: Session = Depends(get_db)):
    """
    Obtener lista de destinos turísticos
    """
    destinos = crud_destino.get_destinos(db, skip=skip, limit=limit, disponible=disponible)
    return destinos


@router.get("/destinos/{destino_id}", response_model=Destino)
def obtener_destino(destino_id: int, db: Session = Depends(get_db)):
    """
    Obtener información detallada de un destino
    """
    db_destino = crud_destino.get_destino(db, destino_id=destino_id)
    if db_destino is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    return db_destino


@router.put("/destinos/{destino_id}", response_model=Destino)
def actualizar_destino(destino_id: int, destino: DestinoUpdate, db: Session = Depends(get_db)):
    """
    Actualizar información de un destino
    """
    db_destino = crud_destino.update_destino(db, destino_id=destino_id, destino=destino)
    if db_destino is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    return db_destino