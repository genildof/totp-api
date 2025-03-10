from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pyotp import TOTP
import os
import base64
import time

app = FastAPI(
    title="TOTP Generator API",
    description="API para gerar códigos TOTP para autenticação MFA",
    version="1.0.0"
)

security = HTTPBearer()
API_TOKEN = os.getenv("API_TOKEN", "M5SW42LMMRXWMZLSOJSWS4TB")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

@app.get("/totp", response_model=dict)
async def generate_totp(secret: str, authenticated: bool = Depends(verify_token)):
    if not secret or len(secret) < 16:
        raise HTTPException(status_code=400, detail="Segredo Base32 inválido: muito curto ou vazio")
    try:
        secret_clean = secret.replace("=", "")
        base64.b32decode(secret_clean, casefold=True)
    except Exception:
        raise HTTPException(status_code=400, detail="Segredo Base32 inválido: deve ser Base32")

    try:
        totp = pyotp.TOTP(secret_clean, interval=30, digits=6, digest="sha1")  # Parâmetros explícitos
        code = totp.now()
        timestamp = int(time.time())
        print(f"Gerado TOTP: {code} para segredo {secret_clean} em {timestamp}")
        return {"code": code, "timestamp": timestamp}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao gerar TOTP: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
