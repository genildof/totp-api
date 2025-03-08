from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pyotp import TOTP  # Biblioteca Python para TOTP (compatível com otpauth)
import os

app = FastAPI(
    title="TOTP Generator API",
    description="API para gerar códigos TOTP para autenticação MFA",
    version="1.0.0"
)

# Configuração de autenticação (token Bearer)
security = HTTPBearer()
API_TOKEN = os.getenv("API_TOKEN", "seu-token-secreto-aqui")  # Defina no ambiente ou no Easypanel

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifica se o token fornecido é válido."""
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

@app.get("/totp",
         response_model=dict,
         summary="Gera um código TOTP",
         description="Recebe um segredo Base32 e retorna um código TOTP de 6 dígitos.")
async def generate_totp(secret: str, authenticated: bool = Depends(verify_token)):
    """
    Gera um código TOTP baseado no segredo fornecido.

    Args:
        secret (str): Segredo Base32 do TOTP (ex.: obtido do Microsoft Authenticator).

    Returns:
        dict: {"code": "xxxxxx"} com o código de 6 dígitos.

    Raises:
        HTTPException: Se o segredo for inválido.
    """
    try:
        totp = TOTP(secret)
        code = totp.now()  # Gera o código atual
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao gerar TOTP: {str(e)}")

# Endpoint de health check (opcional, sem autenticação)
@app.get("/health", summary="Verifica se a API está ativa")
async def health_check():
    return {"status": "ok"}
