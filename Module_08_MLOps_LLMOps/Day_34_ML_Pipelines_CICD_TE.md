# Day 34: ML పైప్‌లైన్స్ & CI/CD ఆటోమేషన్ (Docker & GitHub Actions) 🚀

---

## 1. ఈ రోజు మన గోల్స్ (Day 34 Learning Objectives)
- డేటా క్లీనింగ్, మోడల్ ట్రైనింగ్, మరియు ఎవాల్యుయేషన్ లను ఆటోమేట్ చేసే పునరావృత **ML Pipelines** ను నిర్మించడం.
- మెషిన్ లెర్నింగ్ మోడల్స్ ని **Docker Containers** లో భద్రపరిచి, సైజ్ తక్కువగా ఉండేలా (Multi-Stage Builds) ప్యాక్ చేయడం.
- **GitHub Actions** ద్వారా ఆటోమేటెడ్ CI/CD పైప్‌లైన్ సెటప్ చేయడం: కోడ్ లించింగ్, డేటా టెస్టింగ్ మరియు ఆటోమేటెడ్ మోడల్ ప్రమోషన్.
- **Champion vs Challenger** పద్ధతి: పాత ప్రొడక్షన్ మోడల్ కంటే కొత్త మోడల్ ఎక్కువ ఖచ్చితత్వం (Accuracy/F1) ఇస్తేనే ఆటోమేటిక్ గా డిప్లాయ్ అయ్యే గేట్‌కీపర్ లాజిక్ రాయడం.
- డాకర్ కంటైనర్ లో సెక్యూరిటీ: రూట్ (root) యూజర్ కాకుండా నాన్-రూట్ యూజర్ తో రన్ చేయడం.

---

## 2. రియల్ వరల్డ్ అనలాజీ (Real-World Analogy)

> 💡 **అనలాజీ: చేతితో చేసిన మట్టి కుండ vs ఆటోమేటెడ్ కార్ల ఫ్యాక్టరీ**
>
> - **మాన్యువల్ మోడల్ డిప్లాయ్‌మెంట్ (మట్టి కుండ):**
>   ఒక డేటా సైంటిస్ట్ తన పర్సనల్ లాప్‌టాప్ లో కోడ్ రాసి, ఒక `.pkl` ఫైల్ సేవ్ చేసి, ఈమెయిల్ లో డెవెలపర్‌కి పంపాడు. డెవలపర్ దాన్ని సర్వర్ లో రన్ చేస్తే: *"Numpy వర్షన్ సరిపోవట్లేదు"*, *"C++ లైబ్రరీ మిస్సయింది"*, *"Pickle ఎర్రర్"* అని వెంటనే క్రాష్ అయింది. ఏ లాప్‌టాప్ లో ఎలా పని చేసిందో ఎవరికీ అర్థం కాదు.
> - **CI/CD + Docker (ఆటోమేటెడ్ కార్ల ఫ్యాక్టరీ):**
>   డెవలపర్ కొత్త కోడ్ రాసి GitHub లోకి పుష్ చేయగానే:
>   1. **రోబోట్ 1 (GitHub Actions):** కోడ్ క్వాలిటీ మరియు టెస్టులను ఆటోమేటిక్ గా చెక్ చేస్తుంది.
>   2. **రోబోట్ 2 (ట్రైనింగ్ & టెస్టింగ్):** కొత్త మోడల్ ని పాత ప్రొడక్షన్ మోడల్ తో పోల్చి చూస్తుంది. కొత్తది 1% ఎక్కువ ఖచ్చితత్వం ఇస్తేనే గ్రీన్ సిగ్నల్ ఇస్తుంది.
>   3. **రోబోట్ 3 (Docker):** పైథాన్ వర్షన్, లైబ్రరీలు మరియు మోడల్ అన్నింటినీ ఒక గాలి చొరబడని షిప్పింగ్ కంటైనర్ (Docker Image) లో ప్యాక్ చేస్తుంది.
>   4. **రోబోట్ 4 (CD Deploy):** ఏ సర్వర్ లోనైనా (AWS, GCP, Azure) ఎలాంటి లోపాలు లేకుండా క్షణాల్లో ప్రత్యక్ష ప్రసారం (Zero Downtime) అవుతుంది!

---

## 3. ML CI/CD ఆర్కిటెక్చర్ ఫ్లో

```
   డెవలపర్ కోడ్ ని GitHub కి పుష్ చేస్తారు
                   │
                   ▼
┌───────────────────────────────────────┐
│            GitHub Repo                │
└──────────────────┬────────────────────┘
                   │ git push
                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     GITHUB ACTIONS CI/CD రన్నర్                         │
│                                                                         │
│   స్టెప్ 1: కోడ్ క్వాలిటీ & లించింగ్ (ruff check)                       │
│                        │                                                │
│                        ▼                                                │
│   స్టెప్ 2: డేటా ప్రాసెసింగ్ యూనిట్ టెస్టులు (pytest)                   │
│                        │                                                │
│                        ▼                                                │
│   స్టెప్ 3: ట్రైనింగ్ & ఎవాల్యుయేషన్ గేట్‌కీపర్                         │
│           - కొత్త ఛాలెంజర్ మోడల్ ని టెస్ట్ చేయడం                       │
│           - Champion.F1 కంటే Challenger.F1 >= 1% ఎక్కువ ఉందా?           │
│                        │ గ్రీన్ సిగ్నల్ వస్తే                           │
│                        ▼                                                │
│   స్టెప్ 4: తేలికపాటి Docker ఇమేజ్ ని బిల్డ్ చేయడం                      │
│           - FastAPI ఇన్ఫరెన్స్ కోడ్ + మోడల్ ఫైల్                        │
│                        │                                                │
│                        ▼                                                │
│   స్టెప్ 5: DockerHub లేదా Cloud Container Registry కి పుష్ చేయడం       │
└────────────────────────┬────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  ప్రొడక్షన్ క్లౌడ్ (Cloud Run / AWS ECS)                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Multi-Stage Dockerfile (తేలికపాటి ఇమేజ్ బిల్డ్ చేయడం)

మెషిన్ లెర్నింగ్ లో లైబ్రరీలు చాలా బరువుగా ఉంటాయి. సాధారణ డాకర్‌ఫైల్ రాస్తే ఇమేజ్ 3-4 GB అయిపోతుంది. కింద చూపిన **Multi-Stage Build** ద్వారా సైజును 250MB కి తగ్గించవచ్చు:

```dockerfile
# దశ 1: బిల్డర్ దశ (Builder Stage) - అవసరమైన ప్యాకేజీలు కంపైల్ చేస్తుంది
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# దశ 2: ఫైనల్ రన్నర్ దశ (Runner Stage) - తేలికపాటి ప్రొడక్షన్ ఇమేజ్
FROM python:3.11-slim AS runner

WORKDIR /app

# సెక్యూరిటీ కోసం నాన్-రూట్ యూజర్ ని క్రియేట్ చేయడం
RUN useradd -m -u 1000 appuser

# బిల్డర్ దశ నుండి సిద్ధమైన పైథాన్ ప్యాకేజీలను మాత్రమే కాపీ చేసుకోవడం
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

## 5. కోడింగ్ వాక్‌త్రూ: ఆటోమేటెడ్ మోడల్ గేట్‌కీపర్ (Champion vs Challenger)

CI పైప్‌లైన్ లో రన్ అయ్యే ఈ స్క్రిప్ట్, కొత్త మోడల్ పాతదానికంటే మెరుగ్గా ఉంటేనే పాస్ అవుతుంది, లేదంటే CI ని ఫెయిల్ చేసి ఆపేస్తుంది:

```python
# evaluate_and_gatekeep.py
import sys
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier

def gatekeeper_check():
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    # 1. ప్రస్తుత ప్రొడక్షన్ ఛాంపియన్ మోడల్ (Baseline)
    champion = RandomForestClassifier(n_estimators=10, max_depth=2, random_state=42)
    champion.fit(X_train, y_train)
    champion_f1 = f1_score(y_test, champion.predict(X_test))

    # 2. కొత్తగా ట్రైన్ అయిన ఛాలెంజర్ మోడల్ (Candidate)
    challenger = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42)
    challenger.fit(X_train, y_train)
    challenger_f1 = f1_score(y_test, challenger.predict(X_test))

    print(f"📊 ప్రస్తుత ప్రొడక్షన్ మోడల్ F1-స్కోరు: {champion_f1:.4f}")
    print(f"🚀 కొత్త ఛాలెంజర్ మోడల్ F1-స్కోరు      : {challenger_f1:.4f}")

    MINIMUM_F1_THRESHOLD = 0.90
    IMPROVEMENT_DELTA = 0.01  # కనీసం 1% ఇంప్రూవ్‌మెంట్ ఉండాలి

    # రూల్ 1: కనీస థ్రెషోల్డ్ దాటాలి
    if challenger_f1 < MINIMUM_F1_THRESHOLD:
        print(f"❌ CI తిరస్కరించబడింది: కొత్త మోడల్ స్కోరు {MINIMUM_F1_THRESHOLD} కంటే తక్కువగా ఉంది.")
        sys.exit(1)

    # రూల్ 2: పాత మోడల్ కంటే మెరుగ్గా ఉండాలి
    if challenger_f1 < (champion_f1 + IMPROVEMENT_DELTA):
        print("⚠️ CI తిరస్కరించబడింది: కొత్త మోడల్ పాతదానికంటే 1% ఎక్కువ మెరుగుదలను చూపించలేదు.")
        sys.exit(1)

    print("✅ CI పాస్ అయింది: కొత్త మోడల్ అర్హత సాధించింది! ప్రొడక్షన్ డిప్లాయ్ కి అనుమతిస్తున్నాం.")
    sys.exit(0)

if __name__ == "__main__":
    gatekeeper_check()
```

---

## 6. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు & పరిష్కారాలు

| తప్పు | ఎందుకు ప్రమాదకరం? | సరైన పద్ధతి |
| :--- | :--- | :--- |
| **డాకర్ కంటైనర్ ని Root యూజర్ తో రన్ చేయడం** | ఒకవేళ API హ్యాక్ అయితే, హ్యాకర్‌కి సర్వర్ మెషిన్ మొత్తం మీద కంట్రోల్ వచ్చేస్తుంది. | డాకర్‌ఫైల్ లో `USER appuser` అని పెట్టి సాధారణ యూజర్ అనుమతులతో మాత్రమే రన్ చేయాలి. |
| **`requirements.txt` లో వర్షన్లు ఫిక్స్ చేయకపోవడం** | కేవలం `pandas` అని రాస్తే, భవిష్యత్తులో కొత్త వర్షన్ వచ్చినప్పుడు కోడ్ సడెన్ గా బ్రేక్ అవుతుంది. | తప్పకుండా `pandas==2.2.1` అని నిర్దిష్ట వర్షన్ మాత్రమే వాడాలి. |
| **CI లో ట్రైనింగ్ డేటా లీకేజ్** | మోడల్ టెస్ట్ చేయడానికి ముందే టెస్ట్ డేటా పై స్కేలర్ ని ఫిట్ చేస్తే తప్పుడు అధిక స్కోర్లు వస్తాయి. | ఎల్లప్పుడూ కేవలం ట్రైనింగ్ సెట్ పైనే ట్రాన్స్‌ఫార్మర్లను ఫిట్ చేయాలి. |

---

## 7. ప్రాక్టికల్ ల్యాబ్ (Hands-on Lab)

### లక్ష్యం:
FastAPI తో ఒక సింపుల్ ప్రిడిక్షన్ API సర్వీస్ ను డిజైన్ చేయండి:
1. `/health` ఎండ్‌పాయింట్: మోడల్ వర్షన్ మరియు స్టేటస్ ఇవ్వాలి.
2. `/predict` ఎండ్‌పాయింట్: యూజర్ పంపిన ఫీచర్స్ ఆధారంగా ప్రిడిక్షన్ ని రిటర్న్ చేయాలి.

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="ML Serving API", version="1.0.0")

class CancerFeatures(BaseModel):
    features: List[float]

@app.get("/health")
def health_check():
    return {"status": "HEALTHY", "model": "CancerDiagnosticClassifier_v2"}

@app.post("/predict")
def predict_diagnosis(data: CancerFeatures):
    if len(data.features) < 3:
        raise HTTPException(status_code=400, detail="కనీసం 3 ఫీచర్లు ఇవ్వాలి.")
    avg = sum(data.features) / len(data.features)
    prediction = "Malignant" if avg > 50 else "Benign"
    return {"prediction": prediction, "mean_value": round(avg, 2)}
```

---

## 8. టాప్ 3 ఇంటర్వ్యూ ప్రశ్నలు & సమాధానాలు

### Q1: ML CI/CD లో Champion vs Challenger మోడల్ అంటే ఏమిటి?
**సమాధానం:**
ప్రస్తుతం కస్టమర్లకు సేవలు అందిస్తున్న లైవ్ మోడల్ ని **Champion** అంటారు. కొత్తగా ట్రైన్ అయి పరీక్షించబడుతున్న మోడల్ ని **Challenger** అంటారు. ఆటోమేటెడ్ పైప్‌లైన్ ఒకే టెస్ట్ డేటాపై రెండింటినీ రన్ చేసి, ఛాలెంజర్ మోడల్ నిర్దిష్ట శాతం కంటే ఎక్కువ మెరుగుదలను చూపించినప్పుడు మాత్రమే పాత ఛాంపియన్ స్థానంలో కొత్తదాన్ని ఆటోమేటిక్ గా డిప్లాయ్ చేస్తుంది.

### Q2: Python ML ప్రాజెక్టులకు Multi-Stage Docker Builds ఎందుకు తప్పనిసరి?
**సమాధానం:**
Scikit-Learn, PyTorch లాంటి ప్యాకేజీలకు C/C++ కంపైలర్లు (gcc) అవసరమవుతాయి. సింగిల్ స్టేజ్ లో ఇవన్నీ ఫైనల్ ఇమేజ్ లోకి వచ్చి ఇమేజ్ సైజ్ 3-4 GB దాటిపోతుంది. Multi-stage build లో కంపైల్ చేయడానికి బిల్డర్ స్టేజ్ వాడి, రన్నర్ స్టేజ్ లో కేవలం తయారైన ప్యాకేజీలను మాత్రమే కాపీ చేయడం వల్ల ఇమేజ్ సైజ్ 200MB కి తగ్గిపోయి సర్వర్ చాలా వేగంగా స్టార్ట్ అవుతుంది.

### Q3: మోడల్ ట్రైనింగ్ కి ముందే CI పైప్‌లైన్ లో ఏ టెస్టులు రన్ అవ్వాలి?
**సమాధానం:**
1. **Linter & Type Checking:** Ruff లేదా Flake8 తో సింటాక్స్ మరియు టైపింగ్ తప్పులు చెక్ చేయాలి.
2. **డేటా స్కీమా వాలిడేషన్:** ఇన్పుట్ డేటా లో నల్ (Null) విలువలు లేవని, కాలమ్ పేర్లు మరియు డేటాటైప్స్ సరిగ్గా ఉన్నాయని చెక్ చేయాలి.
3. **ఫీచర్ ఇంజనీరింగ్ టెస్టులు:** మ్యాథమెటికల్ ట్రాన్స్‌ఫార్మేషన్లు అనుకున్న ఫలితాన్ని ఇస్తున్నాయో లేదో నిర్ధారించే యూనిట్ టెస్టులు రన్ చేయాలి.
