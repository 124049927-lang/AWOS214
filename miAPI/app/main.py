#Importaciones
from fastapi import FastAPI, status, HTTPException 
import asyncio
from typing import Optional

#Instancia del servidor
app = FastAPI(
    title="Mi primera API",
    description="API echa por Rogelio Zea",
    version="1.0.0"
    )


#TB ficticia
usuarios = [
    {"id": 1, "nombre": "Rogelio", "edad": 30},
    {"id": 2, "nombre": "Jefed", "edad": 25},
    {"id": 3, "nombre": "Gabo Jobs", "edad": 28}
]

#Endpoint de bienvenida
@app.get("/", tags=["Inicio"])
async def bienvenida():
    return{"message": "¡Bienvenido a mi API!"}
 
@app.get("/HolaMundo", tags=["Bienvenidad Asincrona"])
async def hola():
    await asyncio.sleep(3)#simulación de una petición
    return{
        "message": "¡Bienvenido a mi API!",
        "estatus":"200"
        }

@app.get("/V1/parametroOb", tags=["Paramatros obligatorios"])
async def consultaUno(id:int):
    return{
        "Se encontro usuario": id,
        }

@app.get("/V1/parametroOp", tags=["Paramatros opcional"])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "Usuario encontrado", "usuario": usuario}
        return {"mensaje": "Usuario no encontrado", "usuario": id}
    else:
        return {"mensaje": "no se proporciono id"}
    
@app.get("/V1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return{
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }
    
@app.post("/V1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje": "Usuario agregado",
        "usuario": usuario
    }


@app.put("/V1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def actualizar_usuario(id:int, usuario_actualizado:dict):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuario.update(usuario_actualizado)
            return{
                "mensaje": "Usuario actualizado",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )

@app.delete("/V1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return{
                "mensaje": "Usuario eliminado",
                "usuario": usuario
            } 
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )