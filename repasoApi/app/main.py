from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="API Biblioteca Digital UPQ",
    description="Práctica 5 - Repaso General y Validaciones Pydantic",
    version="1.0.0"
)

# --- MODELOS DE DATOS (PYDANTIC) ---

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr

class Libro(BaseModel):
    id: int
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    # Validación: Año entre 1450 y el actual
    anio_publicacion: int = Field(..., gt=1450, le=datetime.now().year)
    # Validación: Entero positivo mayor a 1
    paginas: int = Field(..., gt=1)
    # Validación: Solo permite "disponible" o "prestado"
    estado: str = Field("disponible", pattern="^(disponible|prestado)$")

class Prestamo(BaseModel):
    libro_id: int
    usuario: Usuario

# --- BASE DE DATOS FICTICIA

libros_db = [
    Libro(
        id=1, 
        nombre="Cumbres Borrascosas", 
        autor="Emily Brontë", 
        anio_publicacion=1847, 
        paginas=416, 
        estado="disponible"
    ),
    Libro(
        id=2, 
        nombre="Rayuela", 
        autor="Julio Cortázar", 
        anio_publicacion=1963, 
        paginas=600, 
        estado="prestado"
    ),
    Libro(
        id=3, 
        nombre="El Aleph", 
        autor="Jorge Luis Borges", 
        anio_publicacion=1949, 
        paginas=146, 
        estado="disponible"
    ),
    Libro(
        id=4, 
        nombre="Frankenstein", 
        autor="Mary Shelley", 
        anio_publicacion=1818, 
        paginas=280, 
        estado="disponible"
    )
]

prestamos_db = [
    Prestamo(
        libro_id=2,
        usuario=Usuario(nombre="Rogelio Zea", correo="rogelio123@gmail.com")
    )
]

# --- ENDPOINTS ---

# a. Registrar un libro
@app.post("/libros/", status_code=status.HTTP_201_CREATED, tags=["Libros"])
async def registrar_libro(libro: Libro):
    for l in libros_db:
        if l.id == libro.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El ID del libro ya está registrado."
            )
    libros_db.append(libro)
    return {"mensaje": "Libro registrado exitosamente", "libro": libro}

# b. Listar todos los libros disponibles
@app.get("/libros/", tags=["Libros"])
async def listar_libros():
    disponibles = [l for l in libros_db if l.estado == "disponible"]
    return {"libros_disponibles": disponibles, "total": len(disponibles)}

# c. Buscar un libro por su nombre
@app.get("/libros/buscar/{nombre}", tags=["Libros"])
async def buscar_libro(nombre: str):
    resultados = [l for l in libros_db if nombre.lower() in l.nombre.lower()]
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron libros con ese nombre")
    return resultados

# d. Registrar el préstamo de un libro
@app.post("/prestamos/", status_code=status.HTTP_201_CREATED, tags=["Préstamos"])
async def registrar_prestamo(prestamo: Prestamo):
    for libro in libros_db:
        if libro.id == prestamo.libro_id:
            if libro.estado == "prestado":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, 
                    detail="El libro ya se encuentra prestado."
                )
            libro.estado = "prestado"
            prestamos_db.append(prestamo)
            return {"mensaje": "Préstamo registrado", "datos": prestamo}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# e. Marcar un libro como devuelto
@app.put("/prestamos/devolver/{libro_id}", status_code=status.HTTP_200_OK, tags=["Préstamos"])
async def devolver_libro(libro_id: int):
    for libro in libros_db:
        if libro.id == libro_id:
            libro.estado = "disponible"
            return {"mensaje": f"El libro '{libro.nombre}' ha sido devuelto."}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# f. Eliminar el registro de un préstamo
@app.delete("/prestamos/{libro_id}", tags=["Préstamos"])
async def eliminar_prestamo(libro_id: int):
    for p in prestamos_db:
        if p.libro_id == libro_id:
            prestamos_db.remove(p)
            return {"mensaje": "Registro de préstamo eliminado correctamente"}
    
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail="El registro de préstamo ya no existe"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)