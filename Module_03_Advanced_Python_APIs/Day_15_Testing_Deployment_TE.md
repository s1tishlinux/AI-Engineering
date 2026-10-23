# డే 15 (Day 15): టెస్టింగ్ (Pytest), Git & డాకర్ కంటైనరైజేషన్ (Phase 1 Capstone)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను చాలా స్పష్టంగా అర్థం చేసుకుంటారు:
1. ఆటోమేటెడ్ టెస్టింగ్: **`pytest`** ద్వారా అసెర్షన్స్ (Assertions) మరియు టెస్ట్‌లు రాయడం.
2. FastAPI ఎండ్‌పాయింట్లను టెస్ట్ చేయడానికి `fastapi.testclient.TestClient` వాడటం.
3. ప్రొఫెషనల్ Git వర్క్‌ఫ్లో: బ్రాంచ్‌లు, కమిట్స్ మరియు `.gitignore` భద్రత.
4. **డాకర్ (Docker) కంటైనరైజేషన్**: `Dockerfile` రాయడం, ఇమేజ్ బిల్డ్ చేయడం మరియు కంటైనర్ రన్ చేయడం.
5. **ఫేజ్ 1 క్యాప్‌స్టోన్ ప్రాజెక్ట్**: డాకరైజ్ చేసిన, పూర్తి టెస్టులతో కూడిన FastAPI AI మైక్రోసర్వీస్!

---

## 1. "నా సిస్టమ్‌లో పనిచేస్తోంది" అనే మాట ఐటీలో చెల్లదు! (The "Why")

కంపెనీలలో మీ ల్యాప్‌టాప్‌లో మాత్రమే రన్ అయ్యే కోడ్‌కి ఎలాంటి విలువా ఉండదు:
- **ఆటోమేటెడ్ టెస్ట్స్ (`pytest`) లేకపోతే:** మీరు కోడ్‌లో ఒక చిన్న మార్పు చేసిన ప్రతిసారీ పాత ఫీచర్లు ఎక్కడ పాడైపోయాయో అని భయపడుతూ బతకాల్సి వస్తుంది.
- **డాకర్ (Docker) లేకపోతే:** మీ మ్యాక్ ల్యాప్‌టాప్‌లో Python 3.12 తో అద్భుతంగా పనిచేసిన కోడ్, క్లౌడ్ సర్వర్‌లో వేయగానే అక్కడ పైథాన్ వెర్షన్ తేడా వల్ల వెంటనే క్రాష్ అయిపోతుంది!
- **డాకర్ ఏం చేస్తుందంటే - మీ కోడ్, పైథాన్ వెర్షన్, లైబ్రరీలు అన్నింటినీ కలిపి ఒక పటిష్టమైన కంటైనర్ డబ్బాలో ప్యాక్ చేస్తుంది.** దాంతో అది ప్రపంచంలో ఏ కంప్యూటర్‌లో రన్ చేసినా ఒకేలా పనిచేస్తుంది!

---

## 2. `pytest` తో ఆటోమేటెడ్ టెస్టింగ్

### స్టెప్ 1: Pytest ఇన్‌స్టాల్ చేయడం
```bash
pip install pytest httpx
```

### Pytest రూల్స్:
- టెస్ట్ ఫైల్ పేరు తప్పకుండా `test_` తో మొదలవ్వాలి (ఉదా: `test_api.py`).
- టెస్ట్ ఫంక్షన్ పేరు కూడా `test_` తో మొదలవ్వాలి (ఉదా: `test_calculate()`).

```python
# app_logic.py
def calculate_token_cost(tokens: int, cost_per_token: float = 0.00002) -> float:
    if tokens < 0:
        raise ValueError("టోకెన్ల సంఖ్య నెగటివ్ ఉండకూడదు.")
    return tokens * cost_per_token

# test_app_logic.py
import pytest
from app_logic import calculate_token_cost

def test_token_cost_calculation():
    # సరైన లెక్క వచ్చిందో లేదో assert చేస్తుంది!
    result = calculate_token_cost(1000)
    assert result == 0.02

def test_negative_tokens_raises_error():
    # నెగటివ్ నెంబర్ ఇస్తే ఎర్రర్ వస్తుందో లేదో టెస్ట్ చేస్తుంది
    with pytest.raises(ValueError):
        calculate_token_cost(-50)
```

టెర్మినల్ నుండి టెస్ట్‌లు రన్ చేయడం:
```bash
pytest -v
```

---

## 3. FastAPI ఎండ్‌పాయింట్లను టెస్ట్ చేయడం (`TestClient`)

సర్వర్‌ను బ్రౌజర్‌లో రన్ చేయకుండానే, మెమొరీలోనే API రిక్వెస్ట్‌లను టెస్ట్ చేయడానికి `TestClient` వాడతాం:

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

# టెస్ట్ సూట్
client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "HEALTHY"}

def test_echo_post_endpoint():
    payload = {"message": "నమస్కారం AI"}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json()["echoed"]["message"] == "నమస్కారం AI"
```

---

## 4. Git & GitHub భద్రతా నియమాలు

### జీవితంలో మర్చిపోకూడని గోల్డెన్ రూల్:
⚠️ **ఎప్పటికీ `.env` ఫైల్‌ని GitHub లోకి పుష్ చేయవద్దు!**
ఓపెన్ గిట్‌హబ్‌లోకి API కీలను పొరపాటున పంపితే, ఇంటర్నెట్‌లో తిరిగే బాట్స్ కొన్ని సెకన్లలోనే వాటిని దొంగిలించి మీ క్రెడిట్ కార్డుపై లక్షల్లో బిల్లు వేస్తాయి!

`.gitignore` ఫైల్‌లో ఇవి తప్పక ఉంచాలి:
```text
__pycache__/
*.pyc
.venv/
.env
.pytest_cache/
```

---

## 5. డాకర్ (Docker) కంటైనరైజేషన్

### షిప్పింగ్ కంటైనర్ ఉదాహరణ:
1950ల కంటే ముందు ఓడల్లో సరుకులను ప్యాక్ చేయడానికి నానా ఇబ్బందులు పడేవారు. అన్నీ ప్యాక్ చేయడానికి ఒకే విధమైన స్టాండర్డ్ మెటల్ కంటైనర్ డబ్బా కనిపెట్టాక విప్లవం వచ్చింది.
డాకర్ కూడా సాఫ్ట్‌వేర్ ప్రపంచంలో అదే చేసింది!

### FastAPI కోసం ప్రొడక్షన్ `Dockerfile`:
```dockerfile
# 1. పైథాన్ బేస్ ఇమేజ్ తీసుకోవడం
FROM python:3.11-slim

# 2. కంటైనర్ లోపల వర్కింగ్ డైరెక్టరీ సెట్ చేయడం
WORKDIR /app

# 3. పైథాన్ ఎన్విరాన్‌మెంట్ సెట్టింగ్స్
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. ముందుగా requirements.txt కాపీ చేసి ఇన్‌స్టాల్ చేయడం (Docker Caching కోసం)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. మిగిలిన మొత్తం కోడ్‌ని కాపీ చేయడం
COPY . .

# 6. పోర్ట్ 8000 ఓపెన్ చేయడం
EXPOSE 8000

# 7. కంటైనర్ స్టార్ట్ అయినప్పుడు రన్ అవ్వాల్సిన కమాండ్
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### ముఖ్యమైన డాకర్ కమాండ్లు:
```bash
# 1. ఇమేజ్ తయారు చేయడం
docker build -t ai-service:1.0 .

# 2. కంటైనర్‌ను రన్ చేయడం (ల్యాప్‌టాప్ 8000 పోర్ట్‌ని కంటైనర్ 8000 కి కనెక్ట్ చేయడం)
docker run -d -p 8000:8000 --name my-ai-app ai-service:1.0

# 3. రన్ అవుతున్న కంటైనర్లు చూడటం
docker ps

# 4. కంటైనర్ లోపల లాగ్స్ చూడటం
docker logs -f my-ai-app
```

---

## 6. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Pitfalls)

1. **డాకర్‌లో `127.0.0.1` బైండ్ చేయడం:**
   - కంటైనర్ లోపల `127.0.0.1` అని పెడితే మీ ల్యాప్‌టాప్ నుండి యాక్సెస్ అవ్వదు! డాకర్‌లో ఎల్లప్పుడూ `--host 0.0.0.0` అని మాత్రమే రాయాలి.
2. **`requirements.txt` కంటే ముందే మొత్తం కోడ్ కాపీ చేయడం:**
   - కోడ్ మారిన ప్రతిసారీ లైబ్రరీలన్నీ మళ్లీ గంటల తరబడి డౌన్‌లోడ్ అవుతాయి. ముందు `requirements.txt` కాపీ చేసి రన్ చేయాలి.
3. **నెట్‌వర్క్‌పై ఆధారపడే టెస్ట్‌లు రాయడం:**
   - యూనిట్ టెస్ట్‌లలో లైవ్ ఇంటర్నెట్ కాల్స్ చేయకూడదు; Mock చేసి టెస్ట్ చేయాలి.

---

## 7. ఫేజ్ 1 క్యాప్‌స్టోన్ ప్రాజెక్ట్: ప్రొడక్షన్ AI సమ్మరైజర్ మైక్రోసర్వీస్

గత 15 రోజుల్లో నేర్చుకున్న పైథాన్ ఫండమెంటల్స్, OOP, Asyncio, Pydantic, FastAPI, Pytest మరియు Docker అన్నీ కలిపి నిర్మించిన పూర్తి ప్రాజెక్ట్:

```python
# =========================================================
# Phase 1 Capstone: main.py
# =========================================================
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Phase 1 Capstone: AI సమ్మరైజర్ సర్వీస్", version="1.0.0")

class SummarizeRequest(BaseModel):
    document_text: str = Field(min_length=20, max_length=5000, description="సారాంశం కావాల్సిన టెక్స్ట్")
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
    sentences = [s.strip() for s in payload.document_text.split(".") if len(s.strip()) > 5]
    if not sentences:
        raise HTTPException(status_code=400, detail="డాక్యుమెంట్‌లో సరిపడా వాక్యాలు లేవు.")
    
    extracted = sentences[:payload.target_bullets]
    formatted_bullets = [f"• {s}" for s in extracted]

    return SummarizeResponse(
        original_char_count=len(payload.document_text),
        bullet_count=len(formatted_bullets),
        summary_bullets=formatted_bullets
    )
```

### దీని టెస్ట్ సూట్: `test_main.py`
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
        "document_text": "పైథాన్ అత్యంత సులభమైన ప్రోగ్రామింగ్ లాంగ్వేజ్. ఇది AI రంగంలో విరివిగా ఉపయోగించబడుతుంది. FastAPI మెరుపు వేగంతో పనిచేస్తుంది.",
        "target_bullets": 2
    }
    res = client.post("/v1/summarize", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["bullet_count"] == 2
    assert len(data["summary_bullets"]) == 2

def test_validation_rejection_on_short_text():
    payload = {"document_text": "చాలా చిన్న టెక్స్ట్", "target_bullets": 3}
    res = client.post("/v1/summarize", json=payload)
    assert res.status_code == 422  # Pydantic వాలిడేషన్ తిరస్కరించింది
```

---

## 8. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: డాకర్ ఇమేజ్ (Image) మరియు డాకర్ కంటైనర్ (Container) మధ్య తేడా ఏమిటి?**
   - **సమాధానం:** **డాకర్ ఇమేజ్** అనేది కోడ్, లైబ్రరీలు మరియు సిస్టమ్ ఫైల్స్‌తో కూడిన ఒక స్టాటిక్, రీడ్-ఓన్లీ బ్లూప్రింట్ (OOP లో Class లాంటిది). **డాకర్ కంటైనర్** అనేది ఆ ఇమేజ్ ఆధారంగా నిజంగా నడుస్తున్న ఒక ఐసోలేటెడ్ లైవ్ ఇన్‌స్టాన్స్ (OOP లో Object లాంటిది).
2. **ప్రశ్న: `Dockerfile` లో కోడ్ కంటే ముందే `requirements.txt` ని ఎందుకు కాపీ చేసి `pip install` చేస్తారు?**
   - **సమాధానం:** **డాకర్ లేయర్ కాషింగ్ (Layer Caching)** ఉపయోగించుకోవడానికి. లైబ్రరీలు తరచూ మారవు కానీ మన సోర్స్ కోడ్ నిరంతరం మారుతుంది. ముందుగా లైబ్రరీలు ఇన్‌స్టాల్ చేయడం వల్ల, కోడ్ మార్చిన ప్రతిసారీ మళ్లీ లైబ్రరీలు డౌన్‌లోడ్ కాకుండా పాత కాష్‌ను వాడుకుని కేవలం సెకన్లలో ఇమేజ్ రీబిల్డ్ అవుతుంది.
3. **ప్రశ్న: Pytest లో Fixtures అంటే ఏమిటి? ఎందుకు వాడతారు?**
   - **సమాధానం:** `@pytest.fixture` అనేది టెస్ట్‌లు రన్ కావడానికి ముందు కావాల్సిన డేటాబేస్ కనెక్షన్లు, క్లయింట్ కాన్ఫిగరేషన్లను సిద్ధం చేయడానికి (Setup) మరియు టెస్ట్ పూర్తయ్యాక వాటిని సురక్షితంగా క్లోజ్ చేయడానికి (Teardown) వాడే రీ-యూజబుల్ ఫంక్షన్.
