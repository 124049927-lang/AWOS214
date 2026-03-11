from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import asyncio


app = FastAPI(
    title="Examen 2do Parcial"
)

class ticket(BaseModel):
    id: int
    nombre: str = Field(..., min_length=5, max_length=50)
    descripcion: str = Field(..., min_length=10, max_length=200)
    prioridad: str = Field(..., regex="^(baja|media|alta)$")
    estado: str = Field(..., regex="(pendiente)")

tickets_db = [

    ticket(
        id = 1,
        nombre="Gabriel",
        descripcion="No puedo iniciar sesión en mi cuenta",
        prioridad="alta",
        estado="pendiente"
    ),

    ticket(
        id = 2,
        nombre="Mariana",
        descripcion="No puedo iniciar sesión en mi cuenta",
        prioridad="baja",
        estado="pendiente"
    ),

    ticket(
        id = 3,
        nombre="Abdiel",
        descripcion="No puedo iniciar sesión en mi cuenta",
        prioridad="media",
        estado="pendiente"
    )
]

@app.post("/Tickets", status_code=status.HTTP_201_CREATED, tags=["Libros"])
async def registrar_ticket(ticket= ticket):
    for l in tickets_db:
        if l.id == ticket.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El ID del libro ya está creado."
            )
    tickets_db.append(ticket)
    return {"mensaje": "Ticket creado exitosamente", "ticket": ticket}

@app.get("/Tickets", tags=["Libros"])
async def listar_ticket():
    return tickets_db


@app.get("/Tickets/{id}", tags=["Libros"])
async def buscar_ticket(id: int):
    for l in tickets_db:
        if l.id == id:
            return l
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="El ID del libro no fue encontrado."
    )

@app.put("/Tickets/{id}", tags=["Libros"])
async def actualizar_ticket(id: int, ticket: ticket):
    for i, l in enumerate(tickets_db):
        if l.id == id:
            tickets_db[i] = ticket
            return {"mensaje": "Ticket actualizado exitosamente", "ticket": ticket}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="El ID del libro no fue encontrado."
    )

@app.delete("/Tickets/{id}", tags=["Libros"])
async def eliminar_ticket(id: int):
    for i, l in enumerate(tickets_db):
        if l.id == id:
            del tickets_db[i]
            return {"mensaje": "Ticket eliminado exitosamente"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="El ID del libro no fue encontrado."
    )