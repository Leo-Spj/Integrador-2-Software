from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Usuario(Base):
    """
    Modelo para usuarios del sistema
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    puntos_totales = Column(Integer, default=0)  # Puntos acumulados
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    activo = Column(Boolean, default=True)

    # Relaciones
    compras = relationship("Compra", back_populates="usuario")
    canjes = relationship("Canje", back_populates="usuario")


class Destino(Base):
    """
    Modelo para destinos turísticos
    """
    __tablename__ = "destinos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    descripcion = Column(Text, nullable=False)
    pais = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    puntos_otorgados = Column(Integer, default=0)  # Puntos que se otorgan por comprar este destino
    disponible = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    compras = relationship("Compra", back_populates="destino")


class Compra(Base):
    """
    Modelo para compras de destinos
    """
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    destino_id = Column(Integer, ForeignKey("destinos.id"), nullable=False)
    precio_pagado = Column(Float, nullable=False)
    puntos_ganados = Column(Integer, default=0)
    fecha_compra = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String(50), default="completada")  # completada, cancelada, pendiente
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="compras")
    destino = relationship("Destino", back_populates="compras")


class Canje(Base):
    """
    Modelo para canjes de puntos por descuentos
    """
    __tablename__ = "canjes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    puntos_utilizados = Column(Integer, nullable=False)
    descuento_obtenido = Column(Float, nullable=False)  # Monto del descuento en dinero
    descripcion = Column(String(200), nullable=False)
    fecha_canje = Column(DateTime(timezone=True), server_default=func.now())
    usado = Column(Boolean, default=False)  # Si el descuento ya fue usado
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="canjes")