# TOTP Generator API

## Visão Geral

Esta API fornece endpoints para gerar códigos TOTP (Time-based One-Time Password) para autenticação de múltiplos fatores (MFA), utilizando FastAPI.

## Índice

- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Endpoints](#endpoints)
- [Autenticação](#autenticação)
- [Exemplos](#exemplos)
- [Desenvolvimento](#desenvolvimento)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Docker](#docker)

## Instalação

```bash
# Clone o repositório
git clone https://github.com/usuario/totp-generator-api.git

# Entre no diretório
cd totp-generator-api

# Instale as dependências
pip install -r requirements.txt
```

## Configuração

Configure a variável de ambiente para o token de API:

```bash
# Linux/MacOS
export API_TOKEN="seu-token-secreto-aqui"

# Windows (PowerShell)
$env:API_TOKEN="seu-token-secreto-aqui"
```

Ou configure-a no ambiente Easypanel se estiver utilizando essa plataforma.

## Uso

Para iniciar o servidor localmente:

```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.

A documentação automática da API estará disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/totp` | Gera um código TOTP de 6 dígitos | Requerida |
| GET | `/health` | Verifica se a API está ativa | Não requerida |

## Autenticação

A API utiliza autenticação Bearer Token. Para acessar endpoints protegidos, inclua o token no cabeçalho `Authorization`:

```
Authorization: Bearer seu-token-secreto-aqui
```

O token deve corresponder ao valor definido na variável de ambiente `API_TOKEN`.

## Exemplos

### Gerar um código TOTP

```bash
curl -X GET "http://localhost:8000/totp?secret=JBSWY3DPEHPK3PXP" \
  -H "Authorization: Bearer seu-token-secreto-aqui"
```

Resposta:
```json
{
  "code": "123456"
}
```

### Verificar status da API

```bash
curl -X GET "http://localhost:8000/health"
```

Resposta:
```json
{
  "status": "ok"
}
```

## Desenvolvimento

### Dependências

As principais dependências do projeto são:

```
fastapi==0.115.0
uvicorn==0.30.6
pyotp==2.9.0
```

## Estrutura do Projeto

```
.
├── main.py              # Código principal da API
├── requirements.txt     # Dependências do projeto
├── Dockerfile           # Configuração do Docker
└── README.md            # Este arquivo
```

## Docker

### Construir a imagem

```bash
docker build -t totp-generator-api .
```

### Executar o contêiner

```bash
docker run -p 8000:8000 -e API_TOKEN="seu-token-secreto-aqui" totp-generator-api
```

Isso iniciará a API no endereço `http://localhost:8000`.
