from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import Compra, CompraCreate
from app.crud import crud_compra, crud_usuario, crud_destino

router = APIRouter()


@router.post("/compras/", response_model=Compra)
def realizar_compra(compra: CompraCreate, db: Session = Depends(get_db)):
    """
    Realizar una nueva compra de destino turístico
    """
    # Verificar que el usuario existe
    usuario = crud_usuario.get_usuario(db, compra.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar que el destino existe y está disponible
    destino = crud_destino.get_destino(db, compra.destino_id)
    if not destino:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    
    if not destino.disponible:
        raise HTTPException(status_code=400, detail="Destino no disponible")
    
    # Crear la compra
    db_compra = crud_compra.create_compra(db=db, compra=compra)
    if db_compra is None:
        raise HTTPException(status_code=400, detail="No se pudo realizar la compra")
    
    return db_compra


@router.get("/compras/usuario/{usuario_id}", response_model=List[Compra])
def listar_compras_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtener todas las compras de un usuario
    """
    # Verificar que el usuario existe
    usuario = crud_usuario.get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    compras = crud_compra.get_compras_usuario(db, usuario_id=usuario_id)
    return compras


@router.get("/compras/{compra_id}", response_model=Compra)
def obtener_compra(compra_id: int, db: Session = Depends(get_db)):
    """
    Obtener información detallada de una compra
    """
    db_compra = crud_compra.get_compra(db, compra_id=compra_id)
    if db_compra is None:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return db_compra