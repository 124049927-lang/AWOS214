#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios

#Instancia del servidor
app = FastAPI(
    title="Mi primera API",
    description="API echa por Rogelio Zea",
    version="1.0.0"
    )
app.include_router(usuarios.router)
app.include_router(varios.router)