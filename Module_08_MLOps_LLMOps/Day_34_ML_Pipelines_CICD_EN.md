# Day 34: ML Pipelines & CI/CD for Machine Learning (Docker & GitHub Actions) 🚀

---

## 1. Day 34 Learning Objectives
- Design reproducible **Machine Learning Pipelines** that separate data preprocessing, model training, evaluation, and serving into deterministic steps.
- Package inference models into lightweight, secure **Docker Containers** using multi-stage builds.
- Build automated **GitHub Actions CI/CD workflows** for ML: automated linting, unit testing data transformations, model validation thresholds, and container image publishing.
- Implement **Automated Model Promotion**: Automatically deploying models to staging or production only if their benchmark performance surpasses the current production champion.
- Understand reproducible environments using pinned `uv`, `poetry`, or `requirements.txt` constraints.

---

## 2. Real-World Analogy

> 💡 **Analogy: Handcrafted Clay Pottery vs. Automated Car Factory**
>
> - **Manual ML Deployment (Handcrafted Clay):**
>   A data scientist trains a model on their Mac laptop, saves a `.pkl` file, emails it to a backend engineer who tries to run it on an Ubuntu production server. It immediately crashes: "Numpy version mismatch", "missing C++ library", "pickle deserialization error". Nobody knows how to recreate the exact environment.
> - **CI/CD + Docker (Automated Car Factory):**
>   A developer pushes new training code to GitHub.
>   1. **Robot 1 (GitHub Actions Runner):** Automatically runs tests on the data pipeline.
>   2. **Robot 2 (Training & Eval):** Trains the model and compares its F1-score against the current production model.
>   3. **Robot 3 (Docker):** If and only if the new model is superior, it is sealed inside an airtight, identical shipping container (Docker Image) with the exact Python runtime and dependencies.
>   4. **Robot 4 (CD Deploy):** The container rolls out to Kubernetes without zero downtime.

---

## 3. Architecture Overview: The ML CI/CD Pipeline

```
  Developer commits code
            │
            ▼
┌───────────────────────┐
│     GitHub Repo       │
└───────────┬───────────┘
            │ git push
            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     GITHUB ACTIONS CI/CD RUNNER                         │
│                                                                         │
│   Step 1: Lint & Code Quality   (ruff, flake8, mypy)                    │
│                        │                                                │
│                        ▼                                                │
│   Step 2: Data & Preprocessing Tests (pytest)                           │
│                        │                                                │
│                        ▼                                                │
│   Step 3: Run Training & Evaluation Pipeline                            │
│           - Train candidate model                                       │
│           - Compare candidate.accuracy >= production.accuracy + 0.02    │
│                        │ Passed benchmark?                              │
│                        ▼                                                │
│   Step 4: Build Docker Container                                        │
│           - FastAPI inference server                                    │
│           - Packaged model artifact                                     │
│                        │                                                │
│                        ▼                                                │
│   Step 5: Push Image to Registry (DockerHub / AWS ECR / GCP Artifact)   │
└────────────────────────┬────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     PRODUCTION SERVING (Cloud Run / EKS)                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Multi-Stage Dockerfile for ML Inference

Machine learning libraries (PyTorch, Scikit-learn, Pandas) are notoriously heavy. A bad Dockerfile can produce a 4GB+ bloated image. A clean multi-stage or slim build keeps it under 250MB:

```dockerfile
# Multi-stage Dockerfile for FastAPI ML Inference
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final lightweight runtime
FROM python:3.11-slim AS runner

WORKDIR /app

# Create a non-root user for enterprise container security
RUN useradd -m -u 1000 appuser

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ /app/app/
COPY models/ /app/models/

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 5. Coding Walkthrough: Automated Model Evaluation & Gatekeeper

Here is the evaluation script that runs inside CI to ensure a newly trained candidate model is strictly better than the current baseline before permitting deployment:

```python
# evaluate_and_gatekeep.py
"""
CI/CD Gatekeeper Script: Evaluates candidate vs baseline.
Exits with 0 if candidate qualifies; exits with 1 if candidate fails threshold.
"""
import sys
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier

def evaluate_models():
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    # 1. Simulate Current Production Champion Baseline
    baseline_model = RandomForestClassifier(n_estimators=10, max_depth=2, random_state=42)
    baseline_model.fit(X_train, y_train)
    baseline_f1 = f1_score(y_test, baseline_model.predict(X_test))

    # 2. Train New Candidate Challenger Model
    candidate_model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    candidate_model.fit(X_train, y_train)
    candidate_f1 = f1_score(y_test, candidate_model.predict(X_test))

    print(f"Current Production Baseline F1: {baseline_f1:.4f}")
    print(f"New Candidate Challenger F1  : {candidate_f1:.4f}")

    # 3. Governance Evaluation Rules
    MINIMUM_ABSOLUTE_F1 = 0.90
    IMPROVEMENT_DELTA = 0.01  # Must beat baseline by at least 1%

    if candidate_f1 < MINIMUM_ABSOLUTE_F1:
        print(f"❌ CI FAILED: Candidate F1 ({candidate_f1:.4f}) is below minimum floor of {MINIMUM_ABSOLUTE_F1}")
        sys.exit(1)

    if candidate_f1 < (baseline_f1 + IMPROVEMENT_DELTA):
        print(f"⚠️ CI REJECTED: Candidate does not improve baseline by required {IMPROVEMENT_DELTA*100}% margin.")
        sys.exit(1)

    print("✅ CI PASSED: Candidate model surpasses baseline! Proceeding to Docker packaging & deploy.")
    sys.exit(0)

if __name__ == "__main__":
    evaluate_models()
```

### GitHub Actions Workflow Definition:

```yaml
# .github/workflows/ml_pipeline.yml
name: ML Pipeline CI/CD

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test_and_evaluate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff pytest

      - name: Code Quality & Linting
        run: |
          ruff check .

      - name: Run Unit Tests
        run: |
          pytest tests/

      - name: Run Model Benchmark Gatekeeper
        run: |
          python evaluate_and_gatekeep.py

  build_and_publish_docker:
    needs: test_and_evaluate
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Container Image
        run: |
          docker build -t my-ml-service:${{ github.sha }} .
          echo "Docker image built successfully for commit ${{ github.sha }}"
```

---

## 6. Common Fresher Pitfalls

| Pitfall | Why It Causes Production Nightmares | Best Practice |
| :--- | :--- | :--- |
| **Running Docker as `root`** | Default Docker containers run as the Linux root user. If an API vulnerability exists in your FastAPI endpoint, hackers gain root access to the underlying host node. | Always specify a non-root user in the Dockerfile (`USER appuser`). |
| **Unpinned Dependencies in `requirements.txt`** | Writing `pandas` instead of `pandas==2.2.1`. Two months later, pandas releases a major version with breaking changes, causing your CI build to fail without code changes. | Always freeze exact dependencies (`pip freeze > requirements.txt`) or use modern lockfiles (`uv.lock` / `poetry.lock`). |
| **Silent Data Leakage in CI Tests** | Evaluating the model on the training set or fitting scalers on the full dataset before splitting. | Fit transformers and scalers strictly on `X_train`, then transform `X_test` in isolation. |

---

## 7. Hands-on Lab: Automated Model Serving with FastAPI

### Objective:
Create a minimal inference service with FastAPI that loads a serialized model and exposes a health-check and predict endpoint.

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import numpy as np

app = FastAPI(title="ML Production Serving API", version="1.0.0")

class InferenceRequest(BaseModel):
    features: list[float] = Field(..., example=[14.2, 20.5, 92.4, 654.1, 0.086])

class InferenceResponse(BaseModel):
    prediction: int
    confidence: float

@app.get("/health")
def health_check():
    return {"status": "HEALTHY", "model_version": "v1.2.0"}

@app.post("/predict", response_model=InferenceResponse)
def predict(request: InferenceRequest):
    if len(request.features) != 5:
        raise HTTPException(status_code=400, detail="Expected exactly 5 numerical features.")
    
    # Mock inference logic
    score = float(np.mean(request.features) / 1000.0)
    pred = 1 if score > 0.05 else 0
    return {"prediction": pred, "confidence": min(round(score, 4), 1.0)}
```

---

## 8. Top 3 Interview Questions & Answers

### Q1: What is a "Champion-Challenger" model evaluation strategy in CI/CD?
**Answer:**
A Champion-Challenger strategy compares an existing, deployed production model (the Champion) against a newly trained candidate model (the Challenger) using the exact same unseen test benchmark dataset. The automated pipeline enforces strict gates: the Challenger is only promoted to production if it outperforms the Champion by a pre-configured margin (e.g., +1% F1-score) without regressing on critical secondary metrics like latency or fairness.

### Q2: Why are Multi-Stage Docker builds essential for Python ML applications?
**Answer:**
Python ML packages require C/C++ compilation tools (like `gcc`, `g++`, `make`) to build binary wheels. In a single-stage Dockerfile, these heavy compilers remain in the final image, swelling image size by several gigabytes and introducing security attack surfaces. Multi-stage builds compile packages in a temporary `builder` stage and copy only the final clean Python wheels into a slim `runner` image, drastically reducing build size and cold-start latency.

### Q3: What tests should run in an ML CI pipeline before model training even begins?
**Answer:**
1. **Linting and Type Checking:** Ruff and Mypy to catch syntax and typing errors.
2. **Data Schema Validation:** Checking that input features match expected types, missing value thresholds, and category cardinality using Great Expectations or Pydantic.
3. **Unit Tests on Feature Transforms:** Verifying that mathematical transformations (one-hot encoding, log scaling, imputation) produce deterministic, non-null outputs.
