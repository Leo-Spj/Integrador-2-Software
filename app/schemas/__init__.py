from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


# Esquemas para Usuario
class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str
    telefono: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None


class Usuario(UsuarioBase):
    id: int
    puntos_totales: int
    fecha_registro: datetime
    activo: bool

    class Config:
        from_attributes = True


# Esquemas para Destino
class DestinoBase(BaseModel):
    nombre: str
    descripcion: str
    pais: str
    ciudad: str
    precio: float
    puntos_otorgados: int = 0


class DestinoCreate(DestinoBase):
    pass


class DestinoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    pais: Optional[str] = None
    ciudad: Optional[str] = None
    precio: Optional[float] = None
    puntos_otorgados: Optional[int] = None
    disponible: Optional[bool] = None


class Destino(DestinoBase):
    id: int
    disponible: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True


# Esquemas para Compra
class CompraBase(BaseModel):
    destino_id: int


class CompraCreate(CompraBase):
    usuario_id: int


class Compra(CompraBase):
    id: int
    usuario_id: int
    precio_pagado: float
    puntos_ganados: int
    fecha_compra: datetime
    estado: str
    destino: Destino

    class Config:
        from_attributes = True


# Esquemas para Canje
class CanjeBase(BaseModel):
    puntos_utilizados: int
    descripcion: str


class CanjeCreate(CanjeBase):
    usuario_id: int


class Canje(CanjeBase):
    id: int
    usuario_id: int
    descuento_obtenido: float
    fecha_canje: datetime
    usado: bool

    class Config:
        from_attributes = True


# Esquemas para respuestas
class UsuarioConCompras(Usuario):
    compras: List[Compra] = []
    canjes: List[Canje] = []


class EstadisticasUsuario(BaseModel):
    usuario: Usuario
    total_compras: int
    total_gastado: float
    puntos_disponibles: int
    canjes_realizados: int