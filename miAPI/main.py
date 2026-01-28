#Importaciones
from fastapi import FastAPI
import asyncio

#Instancia del servidor
app = FastAPI()

#Endpoint de bienvenida
@app.get("/")
async def bienvenida():
    return{"message": "¡Bienvenido a mi API!"}

@app.get("/HolaMundo")
async def hola():
    await asyncio.sleep(3)
    return{
        "message": "¡Bienvenido a mi API!",
        "estatus":"200"
        }