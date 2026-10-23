# Day 14: Backend Development with FastAPI

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Why **FastAPI** became the industry standard for Python web backends and AI model serving.
2. Building an application with routers, path parameters, query parameters, and request bodies.
3. Leveraging Pydantic schemas for automatic request validation and response filtering.
4. The power of FastAPI's **Dependency Injection (`Depends`)** system.
5. Interactive OpenAPI documentation (Swagger UI at `/docs`).

---

## 1. The "Why": Why FastAPI Over Flask and Django?

Historically, Python backends used **Django** (heavy, monolithic, batteries-included) or **Flask** (simple, but synchronous and lacks built-in data validation).
FastAPI revolutionized Python backends by combining three superpowers:
1. **Insane Asynchronous Speed**: Built on **Starlette** and `uvicorn`, matching Go and NodeJS in performance benchmarks.
2. **Zero-Boilerplate Validation**: Built on **Pydantic**. Invalid inputs are automatically rejected with a clean `422 Unprocessable Entity` error before touching your business logic!
3. **Automatic Documentation**: Free interactive Swagger UI (`/docs`) and ReDoc (`/redoc`) generated on the fly from your Python type hints!

---

## 2. Anatomy of a FastAPI Application

### Step 1: Install FastAPI & Uvicorn (ASGI Web Server)
```bash
pip install "fastapi[standard]"
```

### Step 2: Hello World with Interactive Docs
```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="TeachIn AI Platform API",
    version="1.0.0",
    description="Production-grade AI backend endpoints."
)

@app.get("/")
def health_check():
    return {"status": "HEALTHY", "service": "Core AI Gateway"}
```

Run with Uvicorn:
```bash
uvicorn main:app --reload
```
Open your browser at `http://127.0.0.1:8000/docs` to see the interactive Swagger UI!

---

## 3. Path Parameters, Query Parameters & Request Bodies

```python
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# 1. Pydantic Models for Request and Response
class ChatPromptRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=1000, description="User instruction")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    stream: bool = False

class ChatResponse(BaseModel):
    prompt_received: str
    generated_text: str
    tokens_used: int

# In-memory mock database
MOCK_USERS_DB = {
    101: {"username": "ananya_ai", "tier": "PRO"},
    102: {"username": "rahul_dev", "tier": "FREE"}
}

# 2. Path Parameter (/users/{user_id}) + Query Parameter (?include_metadata=true)
@app.get("/users/{user_id}")
async def get_user_profile(
    user_id: int = Path(..., description="The unique user ID", ge=1),
    include_metadata: bool = Query(default=False, description="Whether to include extra metadata")
):
    if user_id not in MOCK_USERS_DB:
        raise HTTPException(status_code=404, detail="User record not found.")
    
    user_data = MOCK_USERS_DB[user_id]
    return {"user_id": user_id, "data": user_data, "metadata_included": include_metadata}

# 3. POST Endpoint with Pydantic Request Body & Response Model
@app.post("/ai/generate", response_model=ChatResponse, status_code=201)
async def generate_ai_text(payload: ChatPromptRequest):
    # Simulated model inference
    mock_reply = f"AI response synthesized for: '{payload.prompt}' at temp {payload.temperature}"
    return ChatResponse(
        prompt_received=payload.prompt,
        generated_text=mock_reply,
        tokens_used=len(payload.prompt) // 4
    )
```

---

## 4. Dependency Injection (`Depends`)

Dependency Injection is a software pattern where a component receives its dependencies from an external source rather than hardcoding them.
In FastAPI, `Depends()` is used for:
- Database connection sessions.
- Authentication & Bearer token verification.
- Rate limiting guards.

```python
from fastapi import Depends, Header, HTTPException

# Reusable Dependency: Verifies Bearer Token in Authorization Header
async def verify_api_key(x_api_key: str = Header(..., description="Enterprise Secret API Key")):
    VALID_KEYS = {"techin-secret-token-1234", "admin-master-key-999"}
    if x_api_key not in VALID_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-KEY header.")
    return x_api_key

# Endpoint protected by the dependency
@app.get("/admin/system-metrics")
async def get_system_metrics(authorized_key: str = Depends(verify_api_key)):
    return {
        "authorized_by": authorized_key[:6] + "...",
        "gpu_utilization": "74%",
        "active_models": ["gemini-1.5-pro", "llama-3-70b"]
    }
```

---

## 5. Common Fresher Pitfalls

1. **Using `def` instead of `async def` for I/O operations**:
   - If your endpoint does `await httpx_client.get(...)`, your endpoint function **must** be declared `async def`.
2. **Returning raw database entities directly**:
   - Never return internal database models directly to clients (e.g., exposing hashed passwords!). Always use a Pydantic `response_model` to sanitize and whitelist fields.
3. **Confusing Query Parameters and Path Parameters**:
   - Path parameters are part of the URL path (`/users/{id}`). Query parameters come after the `?` delimiter (`/users?tier=pro&sort=asc`).

---

## 6. Daily Hands-On Lab

### 🧪 Exercise: Build an "AI Model Inference Service" with FastAPI
**Scenario**: Build a complete, production-ready FastAPI service that provides:
1. A GET health-check endpoint.
2. A POST prompt completion endpoint with input length validation.
3. A header-based API Key dependency.

```python
# ==========================================
# Day 14 Lab: Production FastAPI AI Service
# ==========================================
from fastapi import FastAPI, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn

app = FastAPI(title="Production AI Completion Gateway", version="1.0.0")

# Security Dependency
async def authenticate_client(authorization: Optional[str] = Header(None)):
    EXPECTED_TOKEN = "Bearer teachin-ai-key-2026"
    if authorization != EXPECTED_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized! Provide a valid 'Bearer <token>' in Authorization header."
        )
    return True

# Data Models
class CompletionRequest(BaseModel):
    model_name: str = Field(default="gemini-1.5-flash", examples=["gemini-1.5-flash", "gpt-4o"])
    prompt: str = Field(min_length=5, max_length=2000, description="User instruction")
    max_tokens: int = Field(default=256, ge=1, le=4096)

class CompletionResponse(BaseModel):
    model_used: str
    response_text: str
    tokens_consumed: int
    finish_reason: str

# Endpoints
@app.get("/health", tags=["Monitoring"])
async def health():
    return {"status": "HEALTHY", "active_workers": 4}

@app.post(
    "/v1/completions",
    response_model=CompletionResponse,
    status_code=status.HTTP_200_OK,
    tags=["AI Generation"]
)
async def create_completion(
    payload: CompletionRequest,
    is_authenticated: bool = Depends(authenticate_client)
):
    # Simulated model response
    mock_answer = f"Completed analysis for '{payload.prompt[:30]}...' using {payload.model_name}."
    return CompletionResponse(
        model_used=payload.model_name,
        response_text=mock_answer,
        tokens_consumed=len(payload.prompt) // 4,
        finish_reason="stop"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

## 7. Interview Quick-Fire Questions

1. **Q: How does FastAPI generate Swagger UI documentation automatically?**
   - **Answer**: FastAPI inspects the Python type hints, Pydantic request/response schemas, path parameters, and query parameters declared on endpoint functions. It automatically serializes this metadata into an **OpenAPI (JSON) specification**, which is then rendered by Swagger UI at `/docs`.
2. **Q: What is the role of `uvicorn` in running a FastAPI application?**
   - **Answer**: FastAPI is an application framework conforming to the **ASGI** (Asynchronous Server Gateway Interface) standard. FastAPI itself does not listen on network sockets or parse raw HTTP packets. `uvicorn` is the lightning-fast ASGI web server that accepts incoming TCP connections and passes requests to FastAPI's event loop.
3. **Q: Why should you use `response_model` in FastAPI endpoints?**
   - **Answer**: `response_model` performs data filtering, schema conversion, and documentation generation. It guarantees that any internal fields (like database IDs, passwords, or secret flags) present in the return object are stripped out and only fields defined in the schema are sent over the wire.
