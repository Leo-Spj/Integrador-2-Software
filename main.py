from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import usuarios, destinos, compras, puntos
from app.db.database import engine
from app.models import Base

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Destinos Turísticos",
    description="""
    API para una plataforma de venta de destinos turísticos con sistema de puntos.
    
    ## Características:
    - Gestión de usuarios
    - Catálogo de destinos turísticos
    - Sistema de compras
    - Sistema de puntos y canjes por descuentos
    
    ## Sistema de Puntos:
    - Los usuarios ganan puntos con cada compra
    - Los puntos se pueden canjear por descuentos
    - Tasa de conversión: 1 punto = 0.10 pesos de descuento
    """,
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers de la API
app.include_router(usuarios.router, prefix="/api/v1", tags=["usuarios"])
app.include_router(destinos.router, prefix="/api/v1", tags=["destinos"])
app.include_router(compras.router, prefix="/api/v1", tags=["compras"])
app.include_router(puntos.router, prefix="/api/v1", tags=["puntos"])


@app.get("/")
def root():
    """
    Endpoint raíz de la API
    """
    return {
        "mensaje": "API de Destinos Turísticos",
        "version": "1.0.0",
        "documentacion": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Endpoint para verificar el estado de la API
    """
    return {"status": "OK", "mensaje": "La API está funcionando correctamente"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)