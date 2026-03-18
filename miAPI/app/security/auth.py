from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import Depends, HTTPException, status

#Seguridad HTTP Basic
security = HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credenciales.username, "Rogelio")
    passAuth = secrets.compare_digest(credenciales.password, "123456")
    if not (usuarioAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credenciales.username