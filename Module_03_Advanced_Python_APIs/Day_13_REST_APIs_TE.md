# డే 13 (Day 13): REST API ఇంటిగ్రేషన్ & ఆధునిక HTTP క్లయింట్లు (REST APIs & HTTPX)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను చాలా స్పష్టంగా అర్థం చేసుకుంటారు:
1. RESTful API ఆర్కిటెక్చర్: క్లయింట్-సర్వర్ సంబంధం మరియు HTTP రిక్వెస్ట్/రెస్పాన్స్ సైకిల్.
2. ముఖ్యమైన HTTP పద్ధతులు (`GET`, `POST`, `PUT`, `DELETE`) మరియు స్టేటస్ కోడ్‌లు (Status Codes).
3. పైథాన్‌లో సరికొత్త అసమకాలిక లైబ్రరీ **`httpx`** వాడకం (మరియు `requests` తో పోలిక).
4. అథెంటికేషన్ హెడర్స్ (Bearer Tokens, API Keys), క్వెరీ పారామీటర్లు మరియు JSON పేలోడ్స్ పంపడం.
5. ప్రొడక్షన్ స్థాయి సమస్యల పరిష్కారం: టైమ్-అవుట్స్, రేట్ లిమిట్స్ (`429 Too Many Requests`) మరియు ఎక్స్‌పోనెన్షియల్ బ్యాక్-ఆఫ్ (Exponential Backoff).

---

## 1. సాఫ్ట్‌వేర్ ప్రపంచానికి APIs ఎందుకు ప్రాణం? (The "Why")

మనం వాడే Gemini, ChatGPT లేదా Google Maps లాంటివి మన ల్యాప్‌టాప్‌లో రన్ అవ్వవు; అవి ప్రపంచంలో ఎక్కడో ఉన్న భారీ క్లౌడ్ డేటా సెంటర్లలో ఉంటాయి.
మన పైథాన్ ప్రోగ్రామ్ ఆ క్లౌడ్ సర్వర్లతో మాట్లాడటానికి **HTTP REST APIs** ను ఉపయోగిస్తుంది.
రేపు మీ కంపెనీలో ఒక పేమెంట్ గేట్‌వే (Stripe/Razorpay) తో మాట్లాడాలన్నా, లేదా LLM మోడల్ నుండి సమాధానం తెచ్చుకోవాలన్నా API కాల్స్ రాయడం తప్పనిసరి!

---

## 2. HTTP బేసిక్స్ & స్టేటస్ కోడ్‌లు (Status Codes)

ప్రతి HTTP లావాదేవీలో రెండు ఉంటాయి:
- **రిక్వెస్ట్ (Request):** మనం పంపే URL, మెథడ్ (GET/POST), హెడర్స్ (API Key), బాడీ (JSON).
- **రెస్పాన్స్ (Response):** సర్వర్ తిరిగి ఇచ్చే స్టేటస్ కోడ్ (Status Code), డేటా (JSON).

### ఇంటర్వ్యూలలో కచ్చితంగా అడిగే స్టేటస్ కోడ్స్:
| కేటగిరీ | అర్థం | ముఖ్యమైన ఉదాహరణలు |
| :--- | :--- | :--- |
| **2xx (Success)** | పని విజయవంతమైంది | `200 OK` (డేటా వచ్చింది), `201 Created` (కొత్త రికార్డ్ సేవ్ అయింది) |
| **3xx (Redirection)** | లొకేషన్ మారింది | `301 Moved Permanently` (వేరే పేజీకి వెళ్ళింది) |
| **4xx (Client Error)** | మన వైపు నుండి తప్పు జరిగింది | `400 Bad Request`, `401 Unauthorized` (టోకెన్ లేదు), `403 Forbidden` (పర్మిషన్ లేదు), `404 Not Found`, `429 Too Many Requests` (కోటా దాటిపోయింది) |
| **5xx (Server Error)** | అవతలి సర్వర్ క్రాష్ అయింది | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable` |

---

## 3. పాత `requests` కంటే సరికొత్త `httpx` ఎందుకు బెటర్?

సాధారణ `requests` లైబ్రరీ సింక్రోనస్‌గా పనిచేస్తుంది (సర్వర్ రెస్పాన్స్ ఇచ్చేంతవరకు కోడ్ ఆగిపోతుంది). కానీ **`httpx`** లైబ్రరీ ఆధునిక **async/await** మరియు HTTP/2 కి పూర్తి సపోర్ట్ ఇస్తుంది!

```python
import httpx
import asyncio

# అసమకాలికంగా GitHub నుండి డేటా తేవడం
async def fetch_github_user(username: str):
    url = f"https://api.github.com/users/{username}"
    headers = {"User-Agent": "TeachIn-Python-Client"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers=headers)
        
        # స్టేటస్ కోడ్ తనిఖీ చేయడం
        if response.status_code == 200:
            data = response.json()
            print(f"✅ పేరు: {data['name']} | పబ్లిక్ రిపోజిటరీలు: {data['public_repos']}")
        elif response.status_code == 404:
            print(f"❌ '{username}' అనే యూజర్ GitHub లో లేరు.")
        else:
            print(f"⚠️ ఊహించని స్టేటస్: {response.status_code}")

asyncio.run(fetch_github_user("torvalds"))
```

---

## 4. టోకెన్ మరియు JSON బాడీతో POST రిక్వెస్ట్ చేయడం

```python
import httpx
import asyncio

# AI మోడల్ సర్వర్‌కి రిక్వెస్ట్ పంపడం
async def call_ai_generation_api(prompt: str, api_token: str):
    endpoint = "https://api.example-ai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_token}",  # సీక్రెట్ టోకెన్ పంపడం
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta-llama/Llama-3-8B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # json=payload ఇస్తే ఆటోమేటిక్‌గా డిక్షనరీని JSON స్ట్రింగ్‌గా మారుస్తుంది
            response = await client.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()  # 4xx లేదా 5xx ఎర్రర్ వస్తే ఎక్సెప్షన్ లేపుతుంది!
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"🚨 సర్వర్ ఎర్రర్ ఇచ్చింది: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"🌐 ఇంటర్నెట్ లేదా నెట్‌వర్క్ ఫెయిల్ అయింది: {e}")
```

---

## 5. రేట్ లిమిట్స్ (`429`) & ఎక్స్‌పోనెన్షియల్ బ్యాక్-ఆఫ్ (Exponential Backoff)

OpenAI లాంటి AI సర్వీసులలో మనం నిమిషానికి నిర్దిష్ట టోకెన్ల కంటే ఎక్కువ వాడితే సర్వర్ `429 Too Many Requests` అని పంపుతుంది. అప్పుడు సర్వర్‌పై వరుసగా దాడి చేయకుండా కాసేపు వేచి చూసే పద్ధతినే **ఎక్స్‌పోనెన్షియల్ బ్యాక్-ఆఫ్** అంటారు:

```python
import asyncio
import random
import httpx

async def resilient_api_fetch(url: str, max_retries: int = 3):
    async with httpx.AsyncClient() as client:
        for attempt in range(1, max_retries + 1):
            try:
                response = await client.get(url, timeout=5.0)
                
                # రేట్ లిమిట్ వచ్చిందో లేదో చూడటం
                if response.status_code == 429:
                    # 2^1 = 2s, 2^2 = 4s ఇలా వెయిటింగ్ టైమ్ పెరుగుతుంది
                    wait_time = (2 ** attempt) + random.uniform(0.1, 0.5)
                    print(f"⚠️ [429 రేట్ లిమిట్] {wait_time:.2f} సెకన్లు ఆగుతున్నాం (ప్రయత్నం {attempt}/{max_retries})...")
                    await asyncio.sleep(wait_time)
                    continue

                response.raise_for_status()
                return response.json()

            except (httpx.TimeoutException, httpx.NetworkError) as err:
                print(f"⚠️ నెట్‌వర్క్ గ్లిచ్ (ప్రయత్నం #{attempt}): {err}")
                await asyncio.sleep(1.0)

    raise ConnectionError("అన్ని ప్రయత్నాలు విఫలమయ్యాయి. సర్వర్ అందుబాటులో లేదు.")
```

---

## 6. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Pitfalls)

1. **ప్రతి రిక్వెస్ట్‌కీ కొత్త `httpx.AsyncClient()` ఓపెన్ చేయడం:**
   - ప్రతిసారీ క్లయింట్ క్రియేట్ చేస్తే SSL హ్యాండ్‌షేక్ మళ్లీ మళ్లీ జరిగి సర్వర్ స్లో అయిపోతుంది. ఒకే షేర్డ్ క్లయింట్‌ను రీయూజ్ చేసుకోవాలి.
2. **టైమ్‌అవుట్ (Timeout) సెట్ చేయకపోవడం:**
   - డీఫాల్ట్‌గా నెట్‌వర్క్ ఆగితే మీ ప్రోగ్రామ్ అనంతకాలం వేచి చూస్తూనే ఉంటుంది. ఎల్లప్పుడూ `timeout=10.0` అని రాయాలి.
3. **స్టేటస్ కోడ్ చెక్ చేయకుండా `response.json()` పిలవడం:**
   - ఒకవేళ సర్వర్ క్రాష్ అయి HTML ఎర్రర్ పేజీని ఇస్తే, నేరుగా `json()` కాల్ చేసినప్పుడు `JSONDecodeError` తో ప్రోగ్రామ్ ఆగిపోతుంది.

---

## 7. ప్రాక్టీస్ ల్యాబ్ (Daily Hands-On Lab)

### 🧪 టాస్క్: బహుళ నగరాల వాతావరణ సమాచార సేకరణ (Weather Aggregator)
**సన్నివేశం:** హైదరాబాద్, బెంగళూరు మరియు శాన్ ఫ్రాన్సిస్కో నగరాల లైవ్ ఉష్ణోగ్రత మరియు గాలి వేగం వివరాలను పబ్లిక్ Open-Meteo REST API నుండి ఒకేసారి అసమకాలికంగా సేకరించాలి.

```python
# =========================================================
# Day 13 Lab: లైవ్ వెదర్ అగ్రిగేటర్
# =========================================================
import asyncio
import httpx

CITIES = [
    {"name": "హైదరాబాద్", "lat": 17.3850, "lon": 78.4867},
    {"name": "బెంగళూరు", "lat": 12.9716, "lon": 77.5946},
    {"name": "శాన్ ఫ్రాన్సిస్కో", "lat": 37.7749, "lon": -122.4194}
]

async def fetch_city_weather(client: httpx.AsyncClient, city: dict) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city["lat"],
        "longitude": city["lon"],
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto"
    }

    try:
        resp = await client.get(url, params=params, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()["current"]
        return {
            "city": city["name"],
            "temperature_c": data["temperature_2m"],
            "wind_speed_kmh": data["wind_speed_10m"],
            "status": "SUCCESS"
        }
    except Exception as e:
        return {"city": city["name"], "error": str(e), "status": "FAILED"}

async def main():
    print("🌍 ప్రపంచ నగరాల వాతావరణ వివరాలను సేకరిస్తున్నాం...\n")
    async with httpx.AsyncClient() as shared_client:
        tasks = [fetch_city_weather(shared_client, c) for c in CITIES]
        results = await asyncio.gather(*tasks)

    print("="*50)
    print("వాతావరణ నివేదిక సారాంశం")
    print("="*50)
    for r in results:
        if r["status"] == "SUCCESS":
            print(f"📍 {r['city']:15}: {r['temperature_c']}°C (గాలి వేగం: {r['wind_speed_kmh']} km/h)")
        else:
            print(f"📍 {r['city']:15}: లోపం వచ్చింది ({r['error']})")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 8. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: REST API లలో `POST` మరియు `PUT` మధ్య తేడా ఏమిటి?**
   - **సమాధానం:** `POST` అనేది సర్వర్‌లో సరికొత్త రిసోర్స్‌ను సృష్టించడానికి వాడతారు మరియు ఇది ఐడెంపోటెంట్ (Idempotent) కాదు (5 సార్లు కాల్ చేస్తే 5 కొత్త రికార్డులు పడతాయి). `PUT` అనేది ఇప్పటికే ఉన్న రిసోర్స్‌ను అప్‌డేట్ చేయడానికి వాడతారు మరియు ఇది ఐడెంపోటెంట్ (ఒకే డేటాతో 5 సార్లు కాల్ చేసినా సర్వర్ స్థితి ఒకేలా ఉంటుంది).
2. **ప్రశ్న: `401 Unauthorized` మరియు `403 Forbidden` మధ్య తేడా ఏమిటి?**
   - **సమాధానం:** `401 Unauthorized` అంటే **యూజర్ గుర్తింపు లేదు** (టోకెన్ ఇవ్వలేదు లేదా తప్పుడు టోకెన్ ఇచ్చారు). `403 Forbidden` అంటే **యూజర్ ఎవరో తెలిసింది, కానీ ఆ రిసోర్స్‌ను చూసే అధికారం లేదు** (ఉదాహరణకు సాధారణ యూజర్ అడ్మిన్ పేజీకి వెళ్లడానికి ప్రయత్నించినప్పుడు).
3. **ప్రశ్న: `httpx.AsyncClient` లో కనెక్షన్ పూలింగ్ (Connection Pooling) ఎందుకు ముఖ్యం?**
   - **సమాధానం:** ప్రతి HTTPS రిక్వెస్ట్‌కి కొత్త TCP కనెక్షన్ మరియు SSL హ్యాండ్‌షేక్ చేసుకోవడానికి 100 నుండి 300 మిల్లీసెకన్ల సమయం పడుతుంది. `AsyncClient` వాడినప్పుడు పాత కనెక్షన్‌ను అలానే ఉంచి (Keep-Alive) తర్వాతి రిక్వెస్ట్‌లకు వాడుకోవడం వల్ల సమయం చాలా ఆదా అవుతుంది.
