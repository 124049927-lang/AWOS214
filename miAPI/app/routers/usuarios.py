from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router = APIRouter(
    prefix="/v1/usuarios", tags=["CRUD HTTP"]
)

    
@router.get("/")
async def leer_usuarios(db:Session= Depends(get_db)):
    queryUsers = db.query(usuarioDB).all()
    return{
        "status": "200",
        "total": len(queryUsers),
        "usuarios": queryUsers
    }
    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP:usuario_create, db:Session= Depends(get_db)):
    nuevoUsuario = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    return{
        "mensaje": "Usuario agregado",
        "usuario": usuarioP
    }


@router.put("/", status_code=status.HTTP_200_OK)
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

@router.delete("/", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, username: str = Depends(verificar_peticion)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return{
                "mensaje": f"Usuario eliminado correctamente por: {username}",
            } 
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )