from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import Canje, CanjeCreate
from app.crud import crud_canje, crud_usuario

router = APIRouter()


@router.post("/puntos/canjear/", response_model=Canje)
def canjear_puntos(canje: CanjeCreate, db: Session = Depends(get_db)):
    """
    Canjear puntos por descuento
    Tasa de conversión: 1 punto = 0.10 pesos de descuento
    """
    # Verificar que el usuario existe
    usuario = crud_usuario.get_usuario(db, canje.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar que el usuario tenga suficientes puntos
    if usuario.puntos_totales < canje.puntos_utilizados:
        raise HTTPException(
            status_code=400, 
            detail=f"Puntos insuficientes. Tienes {usuario.puntos_totales} puntos, necesitas {canje.puntos_utilizados}"
        )
    
    # Verificar que se canjen al menos 10 puntos
    if canje.puntos_utilizados < 10:
        raise HTTPException(status_code=400, detail="Mínimo 10 puntos para canjear")
    
    # Crear el canje
    db_canje = crud_canje.create_canje(db=db, canje=canje)
    if db_canje is None:
        raise HTTPException(status_code=400, detail="No se pudo realizar el canje")
    
    return db_canje


@router.get("/puntos/usuario/{usuario_id}/canjes", response_model=List[Canje])
def listar_canjes_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtener todos los canjes de un usuario
    """
    # Verificar que el usuario existe
    usuario = crud_usuario.get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    canjes = crud_canje.get_canjes_usuario(db, usuario_id=usuario_id)
    return canjes


@router.get("/puntos/usuario/{usuario_id}/saldo")
def obtener_saldo_puntos(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtener el saldo actual de puntos de un usuario
    """
    usuario = crud_usuario.get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "usuario_id": usuario_id,
        "puntos_totales": usuario.puntos_totales,
        "valor_en_descuento": usuario.puntos_totales * 0.10
    }