# డే 09 (Day 09): ఫంక్షనల్ ప్రోగ్రామింగ్ & డెకరేటర్లు (Functional Programming & Decorators)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను చాలా స్పష్టంగా అర్థం చేసుకుంటారు:
1. పైథాన్‌లో ఫంక్షన్స్ అంటే ఫస్ట్-క్లాస్ సిటిజన్స్ (First-Class Citizens) ఎందుకు అంటారు?
2. ఫంక్షనల్ టూల్స్: `map()`, `filter()` మరియు `reduce()` ఎలా వాడాలి?
3. **క్లోజర్స్ (Closures):** క్లాస్ రాయకుండానే వేరియబుల్స్ విలువలను గుర్తుంచుకోవడం.
4. **డెకరేటర్లు (Decorators):** `@decorator` వాడి ఫంక్షన్లకు సరికొత్త శక్తులు ఇవ్వడం.
5. `@functools.wraps` ఎందుకు వాడాలి?

---

## 1. డెకరేటర్లు ఎందుకు ఇంత పాపులర్? (The "Why")

ఏదైనా పెద్ద కంపెనీలో లేదా AI అప్లికేషన్లలో మనం తరచూ ఇలాంటి పనులు చేయాల్సి వస్తుంది:
- ఒక AI మోడల్ సమాధానం ఇవ్వడానికి ఎంత సమయం (టైమింగ్) పట్టిందో లెక్కించడం.
- ఒక ఫంక్షన్‌ని ఎవరు రన్ చేస్తున్నారో లాగ్స్ రాయడం (Logging).
- యూజర్‌కి సరైన అడ్మిన్ పర్మిషన్ ఉందో లేదో చెక్ చేయడం (Security Check).
- నెట్‌వర్క్ ఎర్రర్ వస్తే 3 సార్లు మళ్లీ ప్రయత్నించడం (Retry Logic).

డెకరేటర్లు లేకపోతే, మీరు ప్రాజెక్ట్‌లోని **ప్రతి ఫంక్షన్ లోపలా** ఈ టైమర్లను, లాగర్లను కాపీ-పేస్ట్ చేయాల్సి వస్తుంది!
**డెకరేటర్ వాడితే కేవలం `@measure_time` అని ఫంక్షన్ పైన ఒకే ఒక్క లైన్ రాస్తే చాలు!**

---

## 2. ఫంక్షన్లు అంటే "ఫస్ట్-క్లాస్ సిటిజన్స్"

పైథాన్‌లో ఫంక్షన్లను సాధారణ వేరియబుల్స్‌లాగే భావించవచ్చు:
1. ఒక వేరియబుల్‌కి ఫంక్షన్‌ని అసైన్ చేయవచ్చు.
2. ఒక ఫంక్షన్‌ని వేరే ఫంక్షన్‌కి ఆర్గ్యుమెంట్‌గా పంపవచ్చు (**Higher-Order Functions**).
3. ఒక ఫంక్షన్ లోపలి నుండి ఇంకో ఫంక్షన్‌ని రిటర్న్ చేయవచ్చు.

```python
def shout(text):
    return text.upper() + "!"

def whisper(text):
    return text.lower() + "..."

# వేరే ఫంక్షన్‌ని ఆర్గ్యుమెంట్‌గా తీసుకునే ఫంక్షన్
def format_announcement(formatter_func, message):
    return formatter_func(message)

print(format_announcement(shout, "డెప్లాయ్‌మెంట్ పూర్తయింది"))
print(format_announcement(whisper, "ఇది సీక్రెట్ సమాచారం"))
```

---

## 3. మూడు అద్భుతమైన ఫంక్షన్లు: `map`, `filter`, `reduce`

```python
from functools import reduce

salaries = [45000, 60000, 85000, 120000, 38000]

# 1. map(): ప్రతి ఉద్యోగి జీతానికి 10% పెంచడం (Transformation)
hike_10_percent = list(map(lambda s: s * 1.10, salaries))
print("10% పెంపు తర్వాత:", hike_10_percent)

# 2. filter(): కేవలం ₹80,000 పైబడిన వారిని మాత్రమే ఫిల్టర్ చేయడం
high_earners = list(filter(lambda s: s >= 80000, salaries))
print("హై శాలరీ ఉన్నవారు (>= 80k):", high_earners)

# 3. reduce(): మొత్తం అందరి జీతాలను కూడి ఒకే నంబర్‌గా మార్చడం (Aggregation)
total_payroll = reduce(lambda acc, s: acc + s, salaries, 0)
print(f"మొత్తం కంపెనీ పేరోల్: ₹{total_payroll:,}")
```

---

## 4. క్లోజర్స్ (Closures - విలువల జ్ఞాపకశక్తి)

బయట ఉన్న పేరెంట్ ఫంక్షన్ రన్ అయి క్లోజ్ అయిపోయినా సరే, లోపల ఉన్న చైల్డ్ ఫంక్షన్ ఆ వేరియబుల్స్‌ను గుర్తుపెట్టుకునే ప్రక్రియనే **క్లోజర్ (Closure)** అంటారు!

```python
def make_multiplier(factor: float):
    # factor విలువను లోపలి ఫంక్షన్ తన మెమొరీలో దాచుకుంటుంది
    def multiplier(number: float) -> float:
        return number * factor
    return multiplier

double = make_multiplier(2)  # factor = 2 ని గుర్తుపెట్టుకుంది
triple = make_multiplier(3)  # factor = 3 ని గుర్తుపెట్టుకుంది

print("10 ని డబుల్ చేస్తే:", double(10))  # 20
print("10 ని ట్రిపుల్ చేస్తే:", triple(10))  # 30
```

---

## 5. డెకరేటర్ల రహస్యం (Decorators Demystified)

డెకరేటర్ అంటే ఒక ఫంక్షన్‌ని ఇన్‌పుట్‌గా తీసుకుని, దానికి అదనపు హంగులు అద్ది, అప్‌గ్రేడ్ చేసిన ఫంక్షన్‌ని తిరిగి ఇచ్చే ఒక స్పెషల్ ఫంక్షన్!

```python
import time
from functools import wraps

# 1. డెకరేటర్ తయారు చేయడం
def measure_execution_time(func):
    @wraps(func)  # అసలైన ఫంక్షన్ పేరు, డాక్యుమెంటేషన్ పోకుండా కాపాడుతుంది
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"⏱️ [ప్రారంభం] '{func.__name__}' రన్ అవుతోంది...")
        
        # అసలైన ఫంక్షన్‌ని కాల్ చేస్తున్నాం
        result = func(*args, **kwargs)
        
        duration = time.time() - start_time
        print(f"⏱️ [పూర్తయింది] '{func.__name__}' రన్ కావడానికి {duration:.4f} సెకన్లు పట్టింది.\n")
        return result
    return wrapper

# 2. '@' గుర్తుతో డెకరేటర్‌ని అప్లై చేయడం
@measure_execution_time
def simulate_ai_inference(tokens: int):
    """AI మోడల్ ఆలోచించి సమాధానం ఇచ్చే సమయాన్ని అనుకరిస్తుంది."""
    time.sleep(0.5)  # లేటెన్సీని సిమ్యులేట్ చేస్తున్నాం
    return f"{tokens} టోకెన్ల సమాధానం సిద్ధంగా ఉంది."

# 3. సాధారణ ఫంక్షన్‌లాగే కాల్ చేయడం
output = simulate_ai_inference(512)
print("ఫలితం:", output)
```

---

## 6. పారామీటర్లతో కూడిన డెకరేటర్లు (Advanced Pattern)

ఒకవేళ డెకరేటర్‌కే స్వయంగా ఆప్షన్లు ఇవ్వాల్సి వస్తే (ఉదా: `@retry(max_attempts=3)`):
దీని కోసం **3 లెవెల్స్ ఫంక్షన్లు** రాయాలి:

```python
def retry(max_attempts: int = 3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️ [ప్రయత్నం {attempt}/{max_attempts}] విఫలమైంది: {e}")
                    if attempt == max_attempts:
                        print("🚨 అన్ని ప్రయత్నాలు విఫలమయ్యాయి. ఎర్రర్ విసురుతున్నాం!")
                        raise
        return wrapper
    return decorator

@retry(max_attempts=3)
def unstable_api_call():
    import random
    if random.random() < 0.7:  # 70% ఫెయిల్ అయ్యే ఛాన్స్
        raise ConnectionResetError("సర్వర్ కనెక్షన్ కట్ అయింది!")
    print("✅ సర్వర్‌కి కనెక్ట్ అయింది!")

try:
    unstable_api_call()
except Exception:
    print("ఫెయిల్యూర్‌ని సేఫ్‌గా హ్యాండిల్ చేశాం.")
```

---

## 7. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Pitfalls)

1. **`@functools.wraps` మర్చిపోవడం:** `@wraps(func)` వాడకపోతే మీ ఫంక్షన్ పేరు మారిపోయి `"wrapper"` అని వస్తుంది. ఇది FastAPI లేదా టెస్టింగ్‌లో తీవ్రమైన సమస్యలు తెస్తుంది.
2. **`wrapper` లోపల `return` చేయడం మర్చిపోవడం:** అసలైన ఫంక్షన్ రిజల్ట్‌ని wrapper నుండి `return` చేయకపోతే మీ ఫంక్షన్ ఎల్లప్పుడూ `None` ని ఇస్తుంది.
3. **చిన్న విషయాలకి కూడా డెకరేటర్లు రాయడం:** ప్రతి చిన్న లాజిక్‌కి డెకరేటర్లు రాస్తే కోడ్ అర్థం కాకుండా అయోమయంగా మారుతుంది.

---

## 8. ప్రాక్టీస్ ల్యాబ్ (Daily Hands-On Lab)

### 🧪 టాస్క్: రోల్ బేస్డ్ యాక్సెస్ కంట్రోల్ డెకరేటర్ (RBAC Security Guard)
**సన్నివేశం:** మీ కంపెనీ AI సర్వీసులలో సున్నితమైన మోడల్స్‌ను డెప్లాయ్ చేయాలన్నా, డేటాబేస్ డిలీట్ చేయాలన్నా యూజర్‌కి సరైన అధికారాలు (Roles) ఉండాలి. ఒక సెక్యూరిటీ గార్డ్ డెకరేటర్ తయారు చేయండి.

```python
# ==========================================
# Day 9 Lab: సెక్యూరిటీ ఆథరైజేషన్ డెకరేటర్
# ==========================================
from functools import wraps

# ప్రస్తుతం లాగిన్ అయి ఉన్న యూజర్ వివరాలు
CURRENT_USER = {
    "username": "kavya_m",
    "role": "ai_researcher"
}

def require_role(allowed_roles: list[str]):
    """యూజర్‌కి సరైన రోల్ ఉంటేనే ఫంక్షన్‌ని రన్ చేయడానికి అనుమతిస్తుంది."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = CURRENT_USER.get("role")
            if user_role not in allowed_roles:
                raise PermissionError(
                    f"⛔ యాక్సెస్ నిరాకరించబడింది! '{CURRENT_USER['username']}' కి అనుమతి లేదు. "
                    f"కావాల్సిన రోల్స్: {allowed_roles}, యూజర్ రోల్: '{user_role}'"
                )
            print(f"🛡️ [అనుమతి లభించింది] '{CURRENT_USER['username']}' {func.__name__} ని రన్ చేయవచ్చు.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# రక్షించబడిన ఫంక్షన్లు (Protected Functions)
@require_role(allowed_roles=["admin", "ai_researcher"])
def deploy_model_to_production(model_name: str):
    return f"🚀 మోడల్ '{model_name}' క్లౌడ్ క్లస్టర్‌లోకి విజయవంతంగా డెప్లాయ్ చేయబడింది!"

@require_role(allowed_roles=["admin"])
def wipe_database():
    return "💥 ప్రొడక్షన్ డేటాబేస్ క్లియర్ చేయబడింది!"

# టెస్ట్ చేసి చూద్దాం:
print(deploy_model_to_production("Llama-3-70B-FineTuned"))

try:
    wipe_database()
except PermissionError as err:
    print(err)
```

---

## 9. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: పైథాన్‌లో క్లోజర్ (Closure) అంటే ఏమిటి? ఎప్పుడు వాడతారు?**
   - **సమాధానం:** బయటి పేరెంట్ ఫంక్షన్ ఎగ్జిక్యూషన్ పూర్తయి క్లోజ్ అయిపోయినప్పటికీ, లోపలి చైల్డ్ ఫంక్షన్ ఆ బయటి వేరియబుల్స్‌ను తన మెమొరీలో దాచుకుని యాక్సెస్ చేయగలగడాన్ని క్లోజర్ అంటారు. గ్లోబల్ వేరియబుల్స్ వాడకుండా డేటాను కాపాడటానికి మరియు డెకరేటర్లు తయారు చేయడానికి క్లోజర్స్ వాడతారు.
2. **ప్రశ్న: డెకరేటర్లలో `@functools.wraps` ఎందుకు తప్పనిసరిగా వాడాలి?**
   - **సమాధానం:** ఒక ఫంక్షన్‌ని డెకరేట్ చేసినప్పుడు దాని అసలు పేరు (`__name__`), డాక్యుమెంటేషన్ (`__doc__`) రాపర్ పేరుతో రీప్లేస్ అయిపోతాయి. `@functools.wraps` ఒరిజినల్ ఫంక్షన్ మెటాడేటాను కాపాడి రాపర్‌కి బదిలీ చేస్తుంది.
3. **ప్రశ్న: ఒకే ఫంక్షన్‌పై రెండు డెకరేటర్లు పెడితే అవి ఏ క్రమంలో రన్ అవుతాయి?**
   - **సమాధానం:** డెకరేటర్లు కింద నుండి పైకి (Bottom-Up) ఫంక్షన్‌కి చుట్టుకుంటాయి. కానీ ఫంక్షన్ కాల్ అయినప్పుడు పైనుండి కిందకి (Top-Down) ఎగ్జిక్యూట్ అవుతాయి.
