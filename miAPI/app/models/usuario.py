from pydantic import BaseModel, Field

#Modelo de validación Pydantic
class usuario_create(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, example="Rogelio")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")