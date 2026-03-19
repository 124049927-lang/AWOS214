from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#definimos la URL de conexión a la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123456@localhost:5434/DB_miapi"
)

#creamos el motor de la base de datos
engine = create_engine(DATABASE_URL)

#creamos una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#creamos la base para los modelos
Base = declarative_base()