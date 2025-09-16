"""
Script para poblar la base de datos con datos de ejemplo
"""

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models import Base, Usuario, Destino
import random

# Crear las tablas
Base.metadata.create_all(bind=engine)

def poblar_datos_ejemplo():
    """
    Poblar la base de datos con datos de ejemplo
    """
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        if db.query(Usuario).count() > 0:
            print("La base de datos ya tiene datos. Saltando poblado.")
            return
        
        # Crear usuarios de ejemplo
        usuarios_ejemplo = [
            Usuario(
                email="juan.perez@email.com",
                nombre="Juan",
                apellido="Pérez",
                telefono="555-0001",
                puntos_totales=0
            ),
            Usuario(
                email="maria.gonzalez@email.com",
                nombre="María",
                apellido="González",
                telefono="555-0002",
                puntos_totales=0
            ),
            Usuario(
                email="carlos.rodriguez@email.com",
                nombre="Carlos",
                apellido="Rodríguez",
                telefono="555-0003",
                puntos_totales=0
            )
        ]
        
        for usuario in usuarios_ejemplo:
            db.add(usuario)
        
        # Crear destinos de ejemplo
        destinos_ejemplo = [
            Destino(
                nombre="Playa del Carmen",
                descripcion="Hermosa playa en la Riviera Maya con aguas cristalinas y arena blanca.",
                pais="México",
                ciudad="Playa del Carmen",
                precio=1200.50,
                puntos_otorgados=120
            ),
            Destino(
                nombre="Machu Picchu",
                descripcion="Antigua ciudadela inca ubicada en las montañas de los Andes peruanos.",
                pais="Perú",
                ciudad="Cusco",
                precio=2500.00,
                puntos_otorgados=250
            ),
            Destino(
                nombre="Cataratas del Iguazú",
                descripcion="Impresionantes cataratas ubicadas en la frontera entre Argentina y Brasil.",
                pais="Argentina",
                ciudad="Puerto Iguazú",
                precio=1800.75,
                puntos_otorgados=180
            ),
            Destino(
                nombre="Cartagena de Indias",
                descripcion="Ciudad histórica con arquitectura colonial y hermosas playas caribeñas.",
                pais="Colombia",
                ciudad="Cartagena",
                precio=1500.00,
                puntos_otorgados=150
            ),
            Destino(
                nombre="Torres del Paine",
                descripcion="Parque nacional con paisajes patagónicos únicos y montañas espectaculares.",
                pais="Chile",
                ciudad="Puerto Natales",
                precio=2200.00,
                puntos_otorgados=220
            ),
            Destino(
                nombre="Salar de Uyuni",
                descripcion="El mayor desierto de sal del mundo con paisajes surrealistas únicos.",
                pais="Bolivia",
                ciudad="Uyuni",
                precio=1600.00,
                puntos_otorgados=160
            ),
            Destino(
                nombre="Galápagos",
                descripcion="Islas volcánicas con fauna única y ecosistemas extraordinarios.",
                pais="Ecuador",
                ciudad="Puerto Ayora",
                precio=3500.00,
                puntos_otorgados=350
            ),
            Destino(
                nombre="Cristo Redentor",
                descripcion="Icónico monumento en la cima del Corcovado con vista panorámica de Río.",
                pais="Brasil",
                ciudad="Río de Janeiro",
                precio=2000.00,
                puntos_otorgados=200
            )
        ]
        
        for destino in destinos_ejemplo:
            db.add(destino)
        
        # Confirmar cambios
        db.commit()
        print("✅ Base de datos poblada con datos de ejemplo exitosamente!")
        print(f"   - {len(usuarios_ejemplo)} usuarios creados")
        print(f"   - {len(destinos_ejemplo)} destinos creados")
        
    except Exception as e:
        print(f"❌ Error al poblar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    poblar_datos_ejemplo()