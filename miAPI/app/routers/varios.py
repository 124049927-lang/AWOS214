import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter


router= APIRouter(tags=["varios"])


#Endpoint de bienvenida
@router.get("/")
async def bienvenida():
    return{"message": "¡Bienvenido a mi API!"}
 
@router.get("/HolaMundo",)
async def hola():
    await asyncio.sleep(3)#simulación de una petición
    return{
        "message": "¡Bienvenido a mi API!",
        "estatus":"200"
        }

@router.get("/V1/parametroOb")
async def consultaUno(id:int):
    return{
        "Se encontro usuario": id,
        }

@router.get("/v1/parametroOp/")
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje":"Usuario encontrado","usuario":usuario}
        return{"mensaje":"usuario no encontrado","usuario":id}
    else:
        return{"mensaje":"No se proporciono id"} 