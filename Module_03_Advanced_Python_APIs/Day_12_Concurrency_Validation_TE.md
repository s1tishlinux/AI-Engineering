# డే 12 (Day 12): కాంకరెన్సీ (Asyncio) & డేటా ధృవీకరణ (Pydantic)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను చాలా స్పష్టంగా అర్థం చేసుకుంటారు:
1. కాంకరెన్సీ మోడల్స్: **మల్టీథ్రెడ్డింగ్**, **మల్టీప్రాసెసింగ్** మరియు **Asyncio** (మరియు GIL అంటే ఏమిటి?).
2. నాన్‌-బ్లాకింగ్ ప్రోగ్రామింగ్: ఈవెంట్ లూప్ (Event Loop), కోరూటీన్స్, `async` మరియు `await`.
3. `asyncio.gather()` ద్వారా ఒకేసారి అనేక API కాల్స్‌ను సమాంతరంగా రన్ చేయడం.
4. డేటా మోడలింగ్: `@dataclass` మరియు పరిశ్రమలో నెం.1 టూల్ **Pydantic (`BaseModel`)**.
5. స్కీమా ధృవీకరణ (Validation) మరియు కస్టమ్ ఫీల్డ్ వాలిడేటర్స్.

---

## 1. ఆధునిక AI సర్వీసులలో Asyncio ఎందుకు అవసరం? (The "Why")

ఆధునిక AI అప్లికేషన్లలో పైథాన్ ఎక్కువగా లెక్కలు వేయదు; ఆ గణితమంతా గ్రాఫిక్స్ కార్డ్ (GPU) లేదా క్లౌడ్ సర్వర్‌లో జరుగుతుంది.
పైథాన్ సర్వర్ తన **95% సమయాన్ని వేచి చూడటంలోనే (Waiting)** గడుపుతుంది:
- OpenAI లేదా Gemini నుండి టోకెన్లు రావడానికి వేచి చూడటం (1.5 సెకన్లు).
- వెక్టర్ డేటాబేస్ (Chroma/Pinecone) సమాధానం ఇవ్వడానికి వేచి చూడటం (200 ms).
- డేటాబేస్ నుండి యూజర్ డేటా రావడానికి వేచి చూడటం (50 ms).

మీ సర్వర్ పాత పద్ధతిలో (Synchronous) ఉంటే, ఒక యూజర్ 2 సెకన్లు వెయిట్ చేస్తున్నంత సేపు సర్వర్ ఇతర యూజర్లందరినీ ఆపేస్తుంది (Block చేస్తుంది)!
**అదే `asyncio` వాడితే, కేవలం ఒకే ఒక్క థ్రెడ్‌తో ఒకేసారి 10,000 మంది యూజర్ల రిక్వెస్ట్‌లను మీ సర్వర్ సునాయాసంగా హ్యాండిల్ చేయగలదు.**

---

## 2. పోలిక: Threads vs Processes vs Asyncio

| మోడల్ | ఎలా పనిచేస్తుంది? | దేనికి అనువైనది? | GIL ప్రభావం ఉంటుందా? |
| :--- | :--- | :--- | :--- |
| **Multiprocessing** | వేర్వేరు ఆపరేటింగ్ సిస్టమ్ ప్రాసెస్‌లు (విడివిడి మెమొరీ) | **CPU-bound పనులు**: వీడియో ఎడిటింగ్, భారీ మ్యాట్రిక్స్ లెక్కలు, మోడల్ ట్రైనింగ్ | GIL అడ్డంకి ఉండదు (పూర్తిగా బైపాస్ అవుతుంది) |
| **Multithreading** | ఒకే ప్రాసెస్‌లో మెమొరీ షేర్ చేసుకునే థ్రెడ్స్ | **పాతకాలపు I/O పనులు**: ఫైల్స్ డౌన్‌లోడ్ చేసుకోవడం | GIL పరిమితి ఉంటుంది (ఒకేసారి ఒక థ్రెడ్) |
| **Asyncio** | ఒకే థ్రెడ్‌లో సహకార ఈవెంట్ లూప్ (Cooperative Loop) | **ఆధునిక హై-స్పీడ్ వెబ్ సర్వర్లు**: FastAPI, చాట్ స్ట్రీమింగ్, AI API కాల్స్ | GIL సమస్య ఉండదు, అత్యంత తక్కువ మెమొరీ |

### రెస్టారెంట్ ఉదాహరణ (Restaurant Metaphor):
- **సాధారణ పద్ధతి (Synchronous):** ఒక వెయిటర్ మొదటి టేబుల్ వద్ద ఆర్డర్ తీసుకుని, కిచెన్‌కి వెళ్లి పిజ్జా బేక్ అయ్యేంతవరకు అక్కడే నిలబడి చూస్తూ ఉంటాడు. పిజ్జా తెచ్చి మొదటి టేబుల్‌కి ఇచ్చాకే రెండో టేబుల్ వాళ్ళతో మాట్లాడతాడు!
- **Asyncio పద్ధతి:** వెయిటర్ మొదటి టేబుల్ ఆర్డర్ కిచెన్‌కి ఇచ్చి, పిజ్జా బేక్ అయ్యే సమయంలో ఖాళీగా ఉండకుండా వెంటనే రెండో టేబుల్ ఆర్డర్ తీసుకుంటాడు (`await`). కిచెన్ నుండి పిజ్జా రెడీ అని గంట మోగగానే మొదటి టేబుల్‌కి తెచ్చి ఇస్తాడు!

---

## 3. `async` మరియు `await` వాడే విధానం

- `async def`: ఒక కోరూటీన్ (ఆగి మళ్లీ మొదలయ్యే ఫంక్షన్) ను తయారు చేస్తుంది.
- `await`: ఆ పని పూర్తయ్యేంతవరకు ప్రస్తుత ఫంక్షన్‌ని ఆపి, ఈలోపు ఈవెంట్ లూప్‌ని వేరే పనులు చేసుకోమని చెబుతుంది.

```python
import asyncio
import time

# నెట్‌వర్క్ కాల్‌ను అనుకరిస్తున్నాం
async def fetch_ai_summary(document_id: int) -> str:
    print(f"⏳ [డాక్యుమెంట్ #{document_id}] Gemini API కి రిక్వెస్ట్ పంపాం...")
    await asyncio.sleep(1.0)  # ఇది నాన్‌-బ్లాకింగ్ వెయిటింగ్ (time.sleep లాగా సర్వర్‌ను ఆపదు!)
    print(f"✅ [డాక్యుమెంట్ #{document_id}] సమ్మరీ అందింది.")
    return f"డాక్యుమెంట్ #{document_id} సారాంశం"

async def main():
    start = time.perf_counter()
    
    # asyncio.gather() ద్వారా 3 కాల్స్‌ని ఒకేసారి నడపడం
    results = await asyncio.gather(
        fetch_ai_summary(101),
        fetch_ai_summary(102),
        fetch_ai_summary(103)
    )
    
    elapsed = time.perf_counter() - start
    print("\nఫలితాలు:", results)
    print(f"మొత్తం పట్టిన సమయం: {elapsed:.2f}s (పాత పద్ధతిలో అయితే 3.0 సెకన్లు పట్టేది!)")

# ఈవెంట్ లూప్‌ను రన్ చేయడం
asyncio.run(main())
```

---

## 4. డేటా వాలిడేషన్: పైథాన్‌కి ప్రాణం ప్యుడాంటిక్ (Pydantic)

పైథాన్‌లో అంతర్గతంగా `@dataclass` ఉన్నప్పటికీ, బయటి ప్రపంచం (APIs, వెబ్‌సైట్లు) నుండి వచ్చే డేటాను కచ్చితంగా చెక్ చేయడానికి **Pydantic** వాడతాం. (FastAPI, LangChain అన్నీ Pydantic పైనే నిర్మించబడ్డాయి!).

Pydantic కేవలం టైప్స్ చెప్పడమే కాదు, డేటాను సరిచూసి, అవసరమైతే ఆటోమేటిక్‌గా మారుస్తుంది:

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class UserRegistrationSchema(BaseModel):
    user_id: int
    username: str = Field(min_length=3, max_length=20, description="యూజర్ హ్యాండిల్")
    email: str
    age: int = Field(ge=18, le=100, description="యూజర్‌కి కనీసం 18 ఏళ్లు నిండి ఉండాలి")
    is_premium: bool = False
    registered_at: datetime = Field(default_factory=datetime.now)

    # మన సొంత బిజినెస్ రూల్ చెక్ చేయడం
    @field_validator("username")
    @classmethod
    def no_special_characters(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("యూజర్‌నేమ్‌లో కేవలం అక్షరాలు మరియు అంకెలు మాత్రమే ఉండాలి.")
        return v.lower()

# 1వ టెస్ట్: సరైన డేటా (స్ట్రింగ్ "24" ఆటోమేటిక్‌గా నెంబర్ 24 గా మారుతుంది!)
valid_payload = {
    "user_id": 901,
    "username": "KiranKumar26",
    "email": "kiran@company.com",
    "age": "24",
    "is_premium": True
}

user = UserRegistrationSchema(**valid_payload)
print("ధృవీకరించబడిన యూజర్ డేటా:\n", user.model_dump_json(indent=2))

# 2వ టెస్ట్: తప్పుడు డేటా (18 ఏళ్ల కంటే తక్కువ ఉన్నప్పుడు వెంటనే పట్టుకుంటుంది)
try:
    invalid_payload = {"user_id": 902, "username": "bad", "email": "x@y.com", "age": 16}
    UserRegistrationSchema(**invalid_payload)
except Exception as e:
    print("\n❌ Pydantic పట్టుకున్న ఎర్రర్:\n", e)
```

---

## 5. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Pitfalls)

1. **`async def` లోపల `time.sleep()` వాడటం:**
   - ⚠️ **అత్యంత ఘోరమైన తప్పు:** `async` ఫంక్షన్ లోపల `time.sleep(5)` రాస్తే, అది మొత్తం మెయిన్ థ్రెడ్‌ను జామ్ చేసి ఈవెంట్ లూప్‌ని స్తంభింపజేస్తుంది! ఎల్లప్పుడూ `await asyncio.sleep(5)` మాత్రమే వాడాలి.
2. **`await` చేయడం మర్చిపోవడం:**
   - `await` లేకుండా ఫంక్షన్‌ని పిలిస్తే అది రన్ అవ్వదు; కేవలం ఒక ఖాళీ `<coroutine object>` ని మాత్రమే ఇస్తుంది.
3. **`dataclass` ని Pydantic అనుకోవడం:**
   - `dataclass` లో `age="హలో"` అని ఇచ్చినా ఆబ్జెక్ట్ క్రియేట్ అయిపోతుంది (ఎర్రర్ రాదు). Pydantic మాత్రమే కచ్చితంగా వాలిడేట్ చేసి ఎర్రర్ ఇస్తుంది.

---

## 6. ప్రాక్టీస్ ల్యాబ్ (Daily Hands-On Lab)

### 🧪 టాస్క్: Pydantic & Asyncio తో కూడిన AI బ్యాచ్ ప్రాసెసర్
**సన్నివేశం:** మీ కంపెనీకి ఒకేసారి అనేక డాక్యుమెంట్ భాగాలు (Chunks) వస్తాయి. Pydantic ద్వారా చెడ్డ డేటాను తిరస్కరించి, మంచి డేటాను `asyncio` ద్వారా ఒకేసారి ఎంబెడ్డింగ్ మోడల్‌కి పంపండి.

```python
# =========================================================
# Day 12 Lab: కాంకరెంట్ AI ఇన్‌జెషన్ పైప్‌లైన్
# =========================================================
import asyncio
from pydantic import BaseModel, Field, ValidationError

class DocumentChunk(BaseModel):
    chunk_id: str
    text: str = Field(min_length=10, max_length=500)
    source: str
    priority: int = Field(default=1, ge=1, le=5)

async def simulate_ai_embedding(chunk: DocumentChunk) -> dict:
    """AI ఎంబెడ్డింగ్ మోడల్‌ను అసమకాలికంగా కాల్ చేస్తుంది."""
    print(f"🚀 [ప్రాసెసింగ్] చంక్ {chunk.chunk_id} ఎంబెడ్డింగ్ జరుగుతోంది (ప్రాధాన్యత: {chunk.priority})...")
    await asyncio.sleep(0.5)  # లేటెన్సీని అనుకరిస్తున్నాం
    return {
        "chunk_id": chunk.chunk_id,
        "vector_dimensions": 1536,
        "status": "EMBEDDED_SUCCESS"
    }

async def process_batch(raw_items: list[dict]):
    valid_chunks: list[DocumentChunk] = []

    # 1. Pydantic ద్వారా తనిఖీ చేయడం
    for raw in raw_items:
        try:
            chunk = DocumentChunk(**raw)
            valid_chunks.append(chunk)
        except ValidationError as err:
            print(f"❌ [తిరస్కరించబడింది] చెల్లని చంక్: {err.errors()[0]['msg']}")

    # 2. సరైన వాటిని ఒకేసారి సమాంతరంగా రన్ చేయడం
    print(f"\nమొత్తం {len(valid_chunks)} సరైన చంక్‌లను కాంకరెంట్‌గా ప్రాసెస్ చేస్తున్నాం...")
    tasks = [simulate_ai_embedding(c) for c in valid_chunks]
    results = await asyncio.gather(*tasks)

    print("\n--- ✅ బ్యాచ్ ప్రాసెసింగ్ పూర్తయింది ---")
    for r in results:
        print(f"  • {r['chunk_id']} -> {r['status']}")

# టెస్ట్ చేద్దాం:
sample_batch = [
    {"chunk_id": "CHK-001", "text": "LangChain provides modular abstraction for LLMs.", "source": "docs.pdf", "priority": 1},
    {"chunk_id": "CHK-002", "text": "Too short", "source": "chat.txt"},  # 10 అక్షరాల కంటే తక్కువ ఉంది (ఫెయిల్ అవుతుంది)
    {"chunk_id": "CHK-003", "text": "Retrieval Augmented Generation enhances accuracy.", "source": "kb.md", "priority": 3}
]

asyncio.run(process_batch(sample_batch))
```

---

## 7. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: పైథాన్‌లో GIL (Global Interpreter Lock) అంటే ఏమిటి?**
   - **సమాధానం:** GIL అనేది CPython లో ఒకే సమయంలో ఒకే ఒక నేటివ్ థ్రెడ్ మాత్రమే పైథాన్ బైట్‌కోడ్‌ను ఎగ్జిక్యూట్ చేసేలా నియంత్రించే ఒక మ్యూటెక్స్ లాక్. మెమొరీ మేనేజ్‌మెంట్‌ను సురక్షితంగా ఉంచడానికి ఇది రూపొందించబడింది, కానీ దీనివల్ల మల్టీ-కోర్ CPU లపై మల్టీథ్రెడింగ్ ద్వారా సమాంతర కంప్యూటేషన్ సాధ్యపడదు (దాని కోసం మల్టీప్రాసెసింగ్ వాడాలి).
2. **ప్రశ్న: ఒకే థ్రెడ్‌పై `asyncio` ఎలా అధిక పనితీరును (Concurrency) సాధిస్తుంది?**
   - **సమాధానం:** ఈవెంట్ లూప్ (Event Loop) మరియు కోఆపరేటివ్ మల్టీటాస్కింగ్ ద్వారా సాధిస్తుంది. ఒక టాస్క్ నెట్‌వర్క్ లేదా డిస్క్ I/O కోసం వేచి చూసే సమయంలో `await` వద్ద తాత్కాలికంగా ఆగిపోతుంది; ఆ సమయంలో ఈవెంట్ లూప్ ఇతర పెండింగ్ టాస్క్‌లను రన్ చేస్తుంది.
3. **ప్రశ్న: పైథాన్ `@dataclass` మరియు Pydantic `BaseModel` మధ్య తేడా ఏమిటి?**
   - **సమాధానం:** `@dataclass` అనేది కేవలం కోడ్ రాయడాన్ని సులభతరం చేసే టూల్ మాత్రమే, ఇది రన్‌టైమ్‌లో డేటా సరైనదా కాదా అని చెక్ చేయదు. కానీ Pydantic అనేది కఠినమైన డేటా ధృవీకరణ (Validation) మరియు టైప్ కన్వర్షన్ లైబ్రరీ. తప్పుడు డేటా వస్తే వెంటనే `ValidationError` విసురుతుంది.
