# Laboratory 1 — FastAPI + PostgreSQL document inventory

This is a **local educational lab** using synthetic data. It is not an authenticated multi-tenant production API.

## 1. Create the structure
```text
lab/
  compose.yml
  Dockerfile
  requirements.txt
  app.py
```

## 2. Docker
`compose.yml`:
```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: academy
      POSTGRES_USER: lab
      POSTGRES_PASSWORD: local_only
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U lab -d academy"]
      interval: 3s
      retries: 15
  api:
    build: .
    environment:
      DATABASE_URL: postgresql://lab:local_only@db:5432/academy
    ports: ["127.0.0.1:8000:8000"]
    depends_on:
      db: {condition: service_healthy}
```
`Dockerfile`:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```
`requirements.txt`:
```text
fastapi>=0.115,<1
uvicorn>=0.30,<1
psycopg[binary]>=3.2,<4
```

## 3. Application
`app.py`:
```python
import os
from hashlib import sha256
import psycopg
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Document(BaseModel):
    document_id: str
    text: str  # synthetic text only

@app.on_event("startup")
def startup():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS documents (
          tenant TEXT NOT NULL,
          id TEXT NOT NULL,
          digest TEXT NOT NULL,
          PRIMARY KEY (tenant,id))""")

@app.post("/documents")
def create(doc: Document, x_demo_tenant: str = Header(...)):
    digest = sha256(doc.text.encode()).hexdigest()
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        try:
            conn.execute("INSERT INTO documents VALUES (%s,%s,%s)",
                         (x_demo_tenant, doc.document_id, digest))
        except psycopg.errors.UniqueViolation:
            raise HTTPException(409, "Duplicate ID")
    return {"sha256": digest}

@app.get("/documents/{document_id}")
def read(document_id: str, x_demo_tenant: str = Header(...)):
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        result = conn.execute(
            "SELECT digest FROM documents WHERE tenant=%s AND id=%s",
            (x_demo_tenant, document_id)).fetchone()
    if result is None:
        raise HTTPException(404, "Not found")
    return {"sha256": result[0]}
```

## 4. Run locally
```bash
docker compose up --build -d
curl -X POST http://127.0.0.1:8000/documents -H 'content-type: application/json' -H 'x-demo-tenant: company-a' -d '{"document_id":"doc-1","text":"synthetic sample"}'
curl -H 'x-demo-tenant: company-b' http://127.0.0.1:8000/documents/doc-1
```
Expected: create succeeds; company-b receives 404. **Security limitation:** the tenant header is user-controlled and easily forged. In production require real authentication, server-side tenant binding, PostgreSQL RLS, secure migrations, TLS, secrets and audit logging.

## 5. Exercises with answers
**A. Why use `%s` in SQL?** Parameters prevent string-based SQL injection.
**B. Why composite PRIMARY KEY?** It scopes unique document identifiers per tenant.
**C. Does returning 404 prove tenant isolation?** No; the demo caller controls tenant selection.

[Academy index](README.md) · [Architecture](01-alfresco-ai.md) · [SHA-256 lab](03-digital-evidence.md)
