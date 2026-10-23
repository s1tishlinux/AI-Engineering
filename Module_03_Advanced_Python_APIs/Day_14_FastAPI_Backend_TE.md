# డే 14 (Day 14): ఫాస్ట్‌ఏపీఐ ద్వారా బ్యాకెండ్ డెవలప్‌మెంట్ (FastAPI Backend)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను చాలా స్పష్టంగా అర్థం చేసుకుంటారు:
1. పాత ఫ్రేమ్‌వర్కులు (Flask, Django) కంటే **FastAPI** నేడు కంపెనీలలో ఎందుకు ఇంత ఫేవరెట్ అయింది?
2. FastAPI అప్లికేషన్ స్ట్రక్చర్: పాత్ పారామీటర్లు, క్వెరీ పారామీటర్లు మరియు రిక్వెస్ట్ బాడీలు.
3. Pydantic మోడల్స్ ద్వారా ఇన్‌పుట్‌లను ఆటోమేటిక్‌గా ధృవీకరించడం (Validation).
4. FastAPI లో సూపర్ పవర్: **డిపెండెన్సీ ఇంజెక్షన్ (`Depends`)** వాడకం.
5. కోడ్ రాయగానే ఆటోమేటిక్‌గా తయారయ్యే ఇంటరాక్టివ్ డాక్యుమెంటేషన్ (Swagger UI at `/docs`).

---

## 1. అసలు FastAPI ఎందుకు వాడాలి? (The "Why")

గతంలో పైథాన్ డెవలపర్లు **Django** (చాలా పెద్దది, నేర్చుకోవడం కష్టం) లేదా **Flask** (సింపుల్ కానీ చాలా స్లో, టైప్ సేఫ్టీ ఉండదు) వాడేవారు.
కానీ FastAPI వచ్చి మొత్తం మార్చేసింది:
1. **విపరీతమైన వేగం (Speed):** Starlette మరియు `uvicorn` పై నిర్మించబడింది. ఇది NodeJS మరియు Go లాంగ్వేజ్‌లతో సమానమైన స్పీడ్‌ని ఇస్తుంది!
2. **ఆటోమేటిక్ డేటా చెకింగ్:** Pydantic వల్ల మనం ఎలాంటి మాన్యువల్ చెకింగ్ రాయాల్సిన పనిలేదు. యూజర్ తప్పుడు డేటా పంపితే ఆటోమేటిక్‌గా `422 Unprocessable Entity` ఎర్రర్‌తో ఆపేస్తుంది!
3. **ఉచిత ఇంటరాక్టివ్ డాక్యుమెంటేషన్:** మనం ఒక్క లైన్ డాక్యుమెంటేషన్ రాయకపోయినా, మన టైప్ హింట్స్ చూసి బ్రౌజర్‌లో అందమైన Swagger UI (`/docs`) పేజీని ఆటోమేటిక్‌గా జనరేట్ చేస్తుంది!

---

## 2. FastAPI ప్రాథమిక నిర్మాణం & Uvicorn

### స్టెప్ 1: FastAPI మరియు Uvicorn ఇన్‌స్టాల్ చేయడం
```bash
pip install "fastapi[standard]"
```

### స్టెప్ 2: మొదటి FastAPI ప్రోగ్రామ్
```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="టీచిన్ AI ప్లాట్‌ఫారమ్ API",
    version="1.0.0",
    description="ప్రొడక్షన్ లెవల్ AI బ్యాకెండ్ ఎండ్‌పాయింట్స్."
)

@app.get("/")
def health_check():
    return {"status": "HEALTHY", "message": "సర్వర్ అద్భుతంగా పనిచేస్తోంది!"}
```

సర్వర్‌ను రన్ చేయడం:
```bash
uvicorn main:app --reload
```
ఇప్పుడు మీ బ్రౌజర్‌లో `http://127.0.0.1:8000/docs` ఓపెన్ చేయండి. మొత్తం API ని అక్కడే క్లిక్ చేసి టెస్ట్ చేసుకోవచ్చు!

---

## 3. పాత్, క్వెరీ పారామీటర్లు & Pydantic బాడీలు

```python
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# 1. Pydantic స్కీమా (ఇన్‌పుట్ & అవుట్‌పుట్ నియమాలు)
class ChatPromptRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=1000, description="యూజర్ అడిగే ప్రశ్న")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    stream: bool = False

class ChatResponse(BaseModel):
    prompt_received: str
    generated_text: str
    tokens_used: int

# శాంపిల్ యూజర్ల డేటాబేస్
MOCK_USERS_DB = {
    101: {"username": "ananya_ai", "tier": "PRO"},
    102: {"username": "rahul_dev", "tier": "FREE"}
}

# 2. పాత్ పారామీటర్ (/users/{user_id}) మరియు క్వెరీ పారామీటర్ (?include_metadata=true)
@app.get("/users/{user_id}")
async def get_user_profile(
    user_id: int = Path(..., description="యూజర్ ప్రత్యేక ఐడీ", ge=1),
    include_metadata: bool = Query(default=False, description="అదనపు మెటాడేటా కావాలా?")
):
    if user_id not in MOCK_USERS_DB:
        raise HTTPException(status_code=404, detail="ఈ ఐడీతో యూజర్ దొరకలేదు.")
    
    user_data = MOCK_USERS_DB[user_id]
    return {"user_id": user_id, "data": user_data, "metadata_included": include_metadata}

# 3. POST ఎండ్‌పాయింట్: Pydantic బాడీని తీసుకుని మోడల్ ద్వారా సమాధానం ఇవ్వడం
@app.post("/ai/generate", response_model=ChatResponse, status_code=201)
async def generate_ai_text(payload: ChatPromptRequest):
    mock_reply = f"AI సమాధానం: '{payload.prompt}' కి తగిన రిప్లై సిద్ధమైంది."
    return ChatResponse(
        prompt_received=payload.prompt,
        generated_text=mock_reply,
        tokens_used=len(payload.prompt) // 4
    )
```

---

## 4. డిపెండెన్సీ ఇంజెక్షన్ (`Depends` - FastAPI సూపర్ పవర్)

డిపెండెన్సీ ఇంజెక్షన్ అంటే ఒక ఎండ్‌పాయింట్‌కి కావాల్సిన డేటాబేస్ కనెక్షన్ లేదా అథెంటికేషన్ చెక్‌లను విడిగా తయారు చేసి సులభంగా జత చేయడం:

```python
from fastapi import Depends, Header, HTTPException

# రీ-యూజబుల్ సెక్యూరిటీ చెక్: సీక్రెట్ కీ ఉంటేనే అనుమతిస్తుంది
async def verify_api_key(x_api_key: str = Header(..., description="ఎంటర్‌ప్రైజ్ సీక్రెట్ API కీ")):
    VALID_KEYS = {"techin-secret-token-1234", "admin-master-key-999"}
    if x_api_key not in VALID_KEYS:
        raise HTTPException(status_code=401, detail="చెల్లని లేదా లేని X-API-KEY హెడర్.")
    return x_api_key

# ఈ ఎండ్‌పాయింట్ కేవలం సరైన కీ ఉన్నవారికి మాత్రమే ఓపెన్ అవుతుంది:
@app.get("/admin/system-metrics")
async def get_system_metrics(authorized_key: str = Depends(verify_api_key)):
    return {
        "authorized_by": authorized_key[:6] + "...",
        "gpu_utilization": "74%",
        "active_models": ["gemini-1.5-pro", "llama-3-70b"]
    }
```

---

## 5. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Pitfalls)

1. **నెట్‌వర్క్ కాల్స్ ఉన్నప్పుడు `def` వాడటం:** మీ ఫంక్షన్ లోపల `await` ఉంటే తప్పకుండా ఫంక్షన్‌ని `async def` అని మాత్రమే డిక్లేర్ చేయాలి.
2. **డేటాబేస్ పాస్‌వర్డ్‌లు డైరెక్ట్‌గా రిటర్న్ చేయడం:** ఎల్లప్పుడూ Pydantic `response_model` ని వాడాలి. అప్పుడు పాస్‌వర్డ్‌లు లాంటి అంతర్గత ఫీల్డ్స్ క్లయింట్‌కి వెళ్లకుండా ఫిల్టర్ అయిపోతాయి.
3. **పాత్ పారామీటర్ మరియు క్వెరీ పారామీటర్ తేడా మర్చిపోవడం:** URL పాత్‌లో భాగమైతే పాత్ పారామీటర్ (`/users/101`). `?` తర్వాత క్వెరీ స్ట్రింగ్‌లో వస్తే క్వెరీ పారామీటర్ (`/users?tier=pro`).

---

## 6. ప్రాక్టీస్ ల్యాబ్ (Daily Hands-On Lab)

### 🧪 టాస్క్: AI మోడల్ ఇన్ఫరెన్స్ మైక్రోసర్వీస్ తయారు చేయడం
**సన్నివేశం:** మీ కంపెనీ కోసం పూర్తి స్థాయి FastAPI సర్వీస్‌ను నిర్మించండి. అందులో:
1. సర్వర్ బాగుందో లేదో చూసే హెల్త్-చెక్ (`/health`).
2. ప్రాంప్ట్ తీసుకొని సమాధానం ఇచ్చే POST ఎండ్‌పాయింట్.
3. హెడర్ ద్వారా Bearer టోకెన్ వెరిఫై చేసే సెక్యూరిటీ గార్డ్.

```python
# ==========================================
# Day 14 Lab: ప్రొడక్షన్ FastAPI AI సర్వీస్
# ==========================================
from fastapi import FastAPI, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn

app = FastAPI(title="AI Completion Gateway", version="1.0.0")

# సెక్యూరిటీ డిపెండెన్సీ
async def authenticate_client(authorization: Optional[str] = Header(None)):
    EXPECTED_TOKEN = "Bearer teachin-ai-key-2026"
    if authorization != EXPECTED_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="అనుమతి లేదు! సరైన 'Bearer <token>' ని హెడర్‌లో ఇవ్వండి."
        )
    return True

# డేటా మోడల్స్
class CompletionRequest(BaseModel):
    model_name: str = Field(default="gemini-1.5-flash")
    prompt: str = Field(min_length=5, max_length=2000, description="యూజర్ ఇన్‌స్ట్రక్షన్")
    max_tokens: int = Field(default=256, ge=1, le=4096)

class CompletionResponse(BaseModel):
    model_used: str
    response_text: str
    tokens_consumed: int
    finish_reason: str

# ఎండ్‌పాయింట్లు
@app.get("/health", tags=["సిస్టమ్ మానిటరింగ్"])
async def health():
    return {"status": "HEALTHY", "active_workers": 4}

@app.post(
    "/v1/completions",
    response_model=CompletionResponse,
    status_code=status.HTTP_200_OK,
    tags=["AI జనరేషన్"]
)
async def create_completion(
    payload: CompletionRequest,
    is_authenticated: bool = Depends(authenticate_client)
):
    mock_answer = f"AI విశ్లేషణ పూర్తయింది: '{payload.prompt[:30]}...' (మోడల్: {payload.model_name})."
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

## 7. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: FastAPI ఎలా ఆటోమేటిక్‌గా Swagger UI డాక్యుమెంటేషన్‌ను తయారు చేస్తుంది?**
   - **సమాధానం:** FastAPI మనం రాసిన పైథాన్ టైప్ హింట్స్, Pydantic స్కీమాలు మరియు పాత్ పారామీటర్లను విశ్లేషిస్తుంది. వాటి నుండి అంతర్జాతీయ ప్రమాణమైన **OpenAPI (JSON) స్పెసిఫికేషన్‌** ను ఆటోమేటిక్‌గా రూపొందిస్తుంది. ఆ JSON ఫైల్‌ను Swagger UI బ్రౌజర్‌లో అందమైన ఇంటరాక్టివ్ పేజీగా `/docs` వద్ద చూపిస్తుంది.
2. **ప్రశ్న: FastAPI అప్లికేషన్‌ను రన్ చేయడానికి `uvicorn` ఎందుకు అవసరం?**
   - **సమాధానం:** FastAPI అనేది కేవలం వెబ్ ఫ్రేమ్‌వర్క్ మాత్రమే (ఇది ASGI ప్రమాణాన్ని పాటిస్తుంది). ఇది నేరుగా నెట్‌వర్క్ సాకెట్లను ఓపెన్ చేయదు. `uvicorn` అనేది మెరుపు వేగంతో పనిచేసే **ASGI వెబ్ సర్వర్**. ఇది ఇంటర్నెట్ నుండి వచ్చే TCP కనెక్షన్‌లను స్వీకరించి FastAPI ఈవెంట్ లూప్‌కి అందజేస్తుంది.
3. **ప్రశ్న: FastAPI ఎండ్‌పాయింట్లలో `response_model` ప్రాముఖ్యత ఏమిటి?**
   - **సమాధానం:** `response_model` అనేది డేటాను ఫిల్టర్ చేయడానికి మరియు భద్రతకు అత్యంత అవసరం. మన ఫంక్షన్ లోపల నుండి డేటాబేస్ రికార్డ్ మొత్తం బయటకు వచ్చినా, `response_model` లో మనం పేర్కొన్న పబ్లిక్ ఫీల్డ్స్‌ను మాత్రమే క్లయింట్‌కి పంపుతుంది (పాస్‌వర్డ్స్ లేదా సీక్రెట్ కీలు బయటకు వెళ్లకుండా ఆపుతుంది).
