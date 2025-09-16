from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioConCompras, EstadisticasUsuario
from app.crud import crud_usuario

router = APIRouter()


@router.post("/usuarios/", response_model=Usuario)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo usuario en el sistema
    """
    # Verificar si el email ya existe
    db_usuario = crud_usuario.get_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    return crud_usuario.create_usuario(db=db, usuario=usuario)


@router.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de usuarios
    """
    usuarios = crud_usuario.get_usuarios(db, skip=skip, limit=limit)
    return usuarios


@router.get("/usuarios/{usuario_id}", response_model=UsuarioConCompras)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtener información detallada de un usuario incluyendo sus compras y canjes
    """
    db_usuario = crud_usuario.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@router.put("/usuarios/{usuario_id}", response_model=Usuario)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    """
    Actualizar información de un usuario
    """
    db_usuario = crud_usuario.update_usuario(db, usuario_id=usuario_id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@router.get("/usuarios/{usuario_id}/estadisticas", response_model=EstadisticasUsuario)
def obtener_estadisticas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtener estadísticas completas de un usuario
    """
    db_usuario = crud_usuario.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Calcular estadísticas
    total_compras = len(db_usuario.compras)
    total_gastado = sum(compra.precio_pagado for compra in db_usuario.compras)
    canjes_realizados = len(db_usuario.canjes)
    
    return EstadisticasUsuario(
        usuario=db_usuario,
        total_compras=total_compras,
        total_gastado=total_gastado,
        puntos_disponibles=db_usuario.puntos_totales,
        canjes_realizados=canjes_realizados
    )