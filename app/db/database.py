from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# URL de conexión a la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./turismo.db")

# Motor de la base de datos
engine = create_engine(DATABASE_URL)

# Sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de la BD
def get_db():
    """
    Función generadora que proporciona una sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()