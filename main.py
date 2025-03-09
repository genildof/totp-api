from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pyotp import TOTP
import os
import base64

app = FastAPI(
    title="TOTP Generator API",
    description="API para gerar códigos TOTP para autenticação MFA",
    version="1.0.0"
)

security = HTTPBearer()
API_TOKEN = os.getenv("API_TOKEN", "seu-token-secreto-aqui")  # Configure no ambiente

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
        HTTPException: Se o segredo for inválido ou houver erro na geração.
    """
    # Validação básica do segredo Base32
    if not secret or len(secret) < 16:  # Segredos TOTP geralmente têm 16+ caracteres
        raise HTTPException(status_code=400, detail="Segredo Base32 inválido: muito curto ou vazio")
    try:
        # Verifica se o segredo é um Base32 válido (remove padding '=' se presente)
        secret = secret.replace("=", "").upper()
        base64.b32decode(secret, casefold=True)  # Levanta exceção se não for Base32
    except Exception:
        raise HTTPException(status_code=400, detail="Segredo Base32 inválido: deve ser codificado em Base32")

    try:
        totp = TOTP(secret)
        code = totp.now()  # Gera o código atual
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao gerar TOTP: {str(e)}")

@app.get("/health", summary="Verifica se a API está ativa")
async def health_check():
    return {"status": "ok"}
