# Day 15: Testing (Pytest), Git & Containerization with Docker (Phase 1 Capstone)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Automated testing using **`pytest`**: Assertions, test discovery, and `@pytest.fixture`.
2. Integration testing FastAPI endpoints using `fastapi.testclient.TestClient`.
3. Professional Git workflows: Branching, commits, `.gitignore`, and secret hygiene.
4. **Docker Containerization**: Writing a multi-stage `Dockerfile`, building images, and running containers.
5. **Phase 1 Capstone Project**: A Dockerized, Fully Tested FastAPI AI Microservice.

---

## 1. The "Why": "It Works on My Machine" is Not an Excuse!

In enterprise engineering, code that only runs on your local laptop has zero business value.
- Without **automated tests (`pytest`)**: Every time you change 1 line of code, you live in fear of breaking 10 other features.
- Without **Docker**: Your app works on your Mac with Python 3.12, but immediately crashes when deployed on an Ubuntu cloud server with Python 3.10 due to missing C++ dependencies.
- **Docker packages your code, Python runtime, operating system libraries, and dependencies into a single immutable container that runs identically on any computer or cloud on Earth.**

---

## 2. Automated Testing with `pytest`

### Step 1: Install Pytest & TestClient
```bash
pip install pytest httpx
```

### Pytest Rules:
- Test files must start with `test_` (e.g., `test_api.py`).
- Test functions must start with `test_` (e.g., `test_calculate_tax()`).

```python
# app_logic.py
def calculate_token_cost(tokens: int, cost_per_token: float = 0.00002) -> float:
    if tokens < 0:
        raise ValueError("Token count cannot be negative.")
    return tokens * cost_per_token

# test_app_logic.py
import pytest
from app_logic import calculate_token_cost

def test_token_cost_calculation():
    # Plain Python assert statements!
    result = calculate_token_cost(1000)
    assert result == 0.02

def test_negative_tokens_raises_error():
    # Testing that exceptions are properly raised
    with pytest.raises(ValueError):
        calculate_token_cost(-50)
```

Run tests from the terminal:
```bash
pytest -v
```

---

## 3. Testing FastAPI Endpoints (`TestClient`)

FastAPI provides `TestClient` (built on `httpx`), allowing you to test HTTP endpoints in memory without needing to spin up a live web server:

```python
# test_api.py
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "HEALTHY"}

@app.post("/echo")
def echo(payload: dict):
    return {"echoed": payload}

# The Test Suite
client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "HEALTHY"}

def test_echo_post_endpoint():
    payload = {"message": "Hello AI"}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json()["echoed"]["message"] == "Hello AI"
```

---

## 4. Professional Git Workflow & Environment Hygiene

### The Sacred Git Golden Rules:
1. **NEVER commit `.env` files**: API keys committed to public GitHub repositories are scraped by automated botnets in seconds, resulting in thousands of dollars in stolen cloud credits!
2. Create a `.gitignore`:
```text
# Python
__pycache__/
*.pyc
.venv/
.env

# Testing & IDE
.pytest_cache/
.vscode/
```

### Essential Git Commands:
```bash
git init
git add .
git commit -m "feat: complete Phase 1 FastAPI microservice"
git branch -M main
git remote add origin https://github.com/your-username/ai-backend.git
git push -u origin main
```

---

## 5. Containerization with Docker

### The Shipping Container Analogy:
Before standard shipping containers existed in the 1950s, workers had to unpack and repack barrels, sacks, and wooden crates individually onto trains, ships, and trucks.
Docker does the same for software: it packs your app into an isolated, standardized container.

### Production `Dockerfile` for FastAPI:
```dockerfile
# Step 1: Use an official lightweight Python base image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 4: Install dependencies first (leverages Docker layer caching!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy application source code
COPY . .

# Step 6: Expose port 8000
EXPOSE 8000

# Step 7: Run Uvicorn when container boots
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Essential Docker Commands:
```bash
# 1. Build the Docker Image
docker build -t ai-service:1.0 .

# 2. Run the Container (Map port 8000 on host to 8000 in container)
docker run -d -p 8000:8000 --name my-ai-app ai-service:1.0

# 3. Check Running Containers
docker ps

# 4. View Application Logs inside the Container
docker logs -f my-ai-app
```

---

## 6. Common Fresher Pitfalls

1. **Hardcoding `127.0.0.1` inside Docker**:
   - In Docker, `CMD ["uvicorn", "main:app", "--host", "127.0.0.1"]` makes the container listen only to internal container localhost, making it unreachable from your computer! **Always bind to `0.0.0.0` inside Docker**.
2. **Copying source code before `requirements.txt` in Dockerfile**:
   - If you copy everything first, Docker cannot cache the `pip install` step, forcing you to re-download all libraries every time you edit a single line of code!
3. **Writing non-deterministic tests**:
   - Tests that depend on live internet connections or random numbers will fail unpredictably. Use mocks or fixed seeds.

---

## 7. Phase 1 Capstone Project: Production AI Microservice

A complete, battle-tested FastAPI microservice with Pydantic validation, structured tests, and a Docker container recipe.

```python
# =========================================================
# Phase 1 Capstone: main.py
# =========================================================
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Phase 1 Capstone: AI Summarizer API", version="1.0.0")

class SummarizeRequest(BaseModel):
    document_text: str = Field(min_length=20, max_length=5000, description="Source content")
    target_bullets: int = Field(default=3, ge=1, le=10)

class SummarizeResponse(BaseModel):
    original_char_count: int
    bullet_count: int
    summary_bullets: list[str]

@app.get("/health")
def health_check():
    return {"status": "ONLINE", "version": "1.0.0"}

@app.post("/v1/summarize", response_model=SummarizeResponse, status_code=status.HTTP_200_OK)
def summarize_document(payload: SummarizeRequest):
    # Simulated summarizer logic
    sentences = [s.strip() for s in payload.document_text.split(".") if len(s.strip()) > 5]
    if not sentences:
        raise HTTPException(status_code=400, detail="Document contains insufficient text structure.")
    
    extracted = sentences[:payload.target_bullets]
    formatted_bullets = [f"• {s}" for s in extracted]

    return SummarizeResponse(
        original_char_count=len(payload.document_text),
        bullet_count=len(formatted_bullets),
        summary_bullets=formatted_bullets
    )
```

### The Accompanying `test_main.py`:
```python
# =========================================================
# Phase 1 Capstone: test_main.py
# =========================================================
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ONLINE"

def test_successful_summarization():
    payload = {
        "document_text": "Python is an interpreted language. It is widely used in artificial intelligence. FastAPI enables high throughput backends.",
        "target_bullets": 2
    }
    res = client.post("/v1/summarize", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["bullet_count"] == 2
    assert len(data["summary_bullets"]) == 2

def test_validation_rejection_on_short_text():
    payload = {"document_text": "Too short", "target_bullets": 3}
    res = client.post("/v1/summarize", json=payload)
    assert res.status_code == 422  # Unprocessable Entity from Pydantic
```

---

## 8. Interview Quick-Fire Questions

1. **Q: What is a Docker Image vs a Docker Container?**
   - **Answer**: A **Docker Image** is a read-only, immutable template/snapshot containing the application code, libraries, and runtime environment (like a Class in OOP). A **Docker Container** is a running, stateful instance of that image (like an Object in OOP).
2. **Q: Why does the Dockerfile copy `requirements.txt` and run `pip install` before copying the rest of the application code?**
   - **Answer**: To leverage **Docker Layer Caching**. Docker executes each instruction as an immutable cached layer. Dependencies change rarely, but application source code changes frequently. By installing dependencies first, Docker skips the time-consuming `pip install` step on rebuilds if `requirements.txt` has not changed.
3. **Q: What is a Pytest fixture?**
   - **Answer**: A fixture (decorated with `@pytest.fixture`) is a reusable helper function that sets up test environments, mock databases, or client connections before tests run and tears them down after tests finish, ensuring clean, isolated test execution without duplicate boilerplate.
