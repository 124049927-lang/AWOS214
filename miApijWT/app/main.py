from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field
import asyncio

# --- CONFIGURACIÓN JWT  ---
SECRET_KEY = "TIID214" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="miApiJWT",
    description="API protegida con OAuth2 y JWT - Practica 7",
    version="1.1.0"
)

# TB ficticia
usuarios = [
    {"id": 1, "nombre": "Rogelio", "edad": 30},
    {"id": 2, "nombre": "Jefed", "edad": 25},
    {"id": 3, "nombre": "Gabo Jobs", "edad": 28}
]

class usuario_create(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=3, max_length=50)
    edad: int = Field(..., ge=1, le=123)

# --- FUNCIONES DE SEGURIDAD [cite: 29] ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")

# --- ENDPOINT PARA OBTENER TOKEN [cite: 9, 10] ---
@app.post("/token", tags=["Seguridad"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validación simple (Sustituye a HTTP Basic) 
    if form_data.username == "Rogelio" and form_data.password == "123456":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

# --- ENDPOINTS EXISTENTES ---
@app.get("/", tags=["Inicio"])
async def bienvenida():
    return {"message": "¡Bienvenido a mi API con JWT!"}

@app.get("/V1/usuarios/", tags=['CRUD'])
async def leer_usuarios():
    return {"usuarios": usuarios}

# --- PROTECCIÓN DE ENDPOINTS (PUT Y DELETE)  ---

@app.put("/V1/usuarios/", tags=['CRUD'], status_code=status.HTTP_200_OK)
async def actualizar_usuario(id: int, usuario_act: dict, token: str = Depends(validar_token)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuario.update(usuario_act)
            return {"mensaje": "Usuario actualizado", "por": token}
    raise HTTPException(status_code=404, detail="No encontrado")

@app.delete("/V1/usuarios/", tags=['CRUD'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, token: str = Depends(validar_token)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {"mensaje": f"Eliminado correctamente por: {token}"}
    raise HTTPException(status_code=404, detail="No encontrado")