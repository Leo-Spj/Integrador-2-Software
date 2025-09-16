from sqlalchemy.orm import Session
from app.models import Usuario, Destino, Compra, Canje
from app.schemas import (
    UsuarioCreate, UsuarioUpdate, 
    DestinoCreate, DestinoUpdate,
    CompraCreate, CanjeCreate
)
from typing import List, Optional


# CRUD para Usuarios
class CRUDUsuario:
    def get_usuario(self, db: Session, usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_usuario_por_email(self, db: Session, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return db.query(Usuario).filter(Usuario.email == email).first()

    def get_usuarios(self, db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtener lista de usuarios"""
        return db.query(Usuario).offset(skip).limit(limit).all()

    def create_usuario(self, db: Session, usuario: UsuarioCreate) -> Usuario:
        """Crear nuevo usuario"""
        db_usuario = Usuario(**usuario.model_dump())
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def update_usuario(self, db: Session, usuario_id: int, usuario: UsuarioUpdate) -> Optional[Usuario]:
        """Actualizar usuario"""
        db_usuario = self.get_usuario(db, usuario_id)
        if db_usuario:
            update_data = usuario.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_usuario, field, value)
            db.commit()
            db.refresh(db_usuario)
        return db_usuario

    def actualizar_puntos(self, db: Session, usuario_id: int, puntos: int) -> Optional[Usuario]:
        """Actualizar puntos del usuario"""
        db_usuario = self.get_usuario(db, usuario_id)
        if db_usuario:
            db_usuario.puntos_totales += puntos
            db.commit()
            db.refresh(db_usuario)
        return db_usuario


# CRUD para Destinos
class CRUDDestino:
    def get_destino(self, db: Session, destino_id: int) -> Optional[Destino]:
        """Obtener destino por ID"""
        return db.query(Destino).filter(Destino.id == destino_id).first()

    def get_destinos(self, db: Session, skip: int = 0, limit: int = 100, disponible: bool = True) -> List[Destino]:
        """Obtener lista de destinos"""
        query = db.query(Destino)
        if disponible is not None:
            query = query.filter(Destino.disponible == disponible)
        return query.offset(skip).limit(limit).all()

    def create_destino(self, db: Session, destino: DestinoCreate) -> Destino:
        """Crear nuevo destino"""
        db_destino = Destino(**destino.model_dump())
        db.add(db_destino)
        db.commit()
        db.refresh(db_destino)
        return db_destino

    def update_destino(self, db: Session, destino_id: int, destino: DestinoUpdate) -> Optional[Destino]:
        """Actualizar destino"""
        db_destino = self.get_destino(db, destino_id)
        if db_destino:
            update_data = destino.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_destino, field, value)
            db.commit()
            db.refresh(db_destino)
        return db_destino


# CRUD para Compras
class CRUDCompra:
    def get_compra(self, db: Session, compra_id: int) -> Optional[Compra]:
        """Obtener compra por ID"""
        return db.query(Compra).filter(Compra.id == compra_id).first()

    def get_compras_usuario(self, db: Session, usuario_id: int) -> List[Compra]:
        """Obtener compras de un usuario"""
        return db.query(Compra).filter(Compra.usuario_id == usuario_id).all()

    def create_compra(self, db: Session, compra: CompraCreate) -> Optional[Compra]:
        """Crear nueva compra"""
        # Obtener el destino para obtener precio y puntos
        destino = db.query(Destino).filter(Destino.id == compra.destino_id).first()
        if not destino or not destino.disponible:
            return None
            
        db_compra = Compra(
            usuario_id=compra.usuario_id,
            destino_id=compra.destino_id,
            precio_pagado=destino.precio,
            puntos_ganados=destino.puntos_otorgados
        )
        
        db.add(db_compra)
        
        # Actualizar puntos del usuario
        usuario = db.query(Usuario).filter(Usuario.id == compra.usuario_id).first()
        if usuario:
            usuario.puntos_totales += destino.puntos_otorgados
            
        db.commit()
        db.refresh(db_compra)
        return db_compra


# CRUD para Canjes
class CRUDCanje:
    def get_canjes_usuario(self, db: Session, usuario_id: int) -> List[Canje]:
        """Obtener canjes de un usuario"""
        return db.query(Canje).filter(Canje.usuario_id == usuario_id).all()

    def create_canje(self, db: Session, canje: CanjeCreate) -> Optional[Canje]:
        """Crear nuevo canje de puntos"""
        # Verificar que el usuario tenga suficientes puntos
        usuario = db.query(Usuario).filter(Usuario.id == canje.usuario_id).first()
        if not usuario or usuario.puntos_totales < canje.puntos_utilizados:
            return None
            
        # Calcular descuento (1 punto = 0.10 pesos de descuento)
        descuento = canje.puntos_utilizados * 0.10
        
        db_canje = Canje(
            usuario_id=canje.usuario_id,
            puntos_utilizados=canje.puntos_utilizados,
            descuento_obtenido=descuento,
            descripcion=canje.descripcion
        )
        
        db.add(db_canje)
        
        # Restar puntos del usuario
        usuario.puntos_totales -= canje.puntos_utilizados
        
        db.commit()
        db.refresh(db_canje)
        return db_canje


# Instancias de las clases CRUD
crud_usuario = CRUDUsuario()
crud_destino = CRUDDestino()
crud_compra = CRUDCompra()
crud_canje = CRUDCanje()