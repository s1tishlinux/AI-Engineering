# డే 04 (Day 04): స్ట్రింగ్స్ & ఫంక్షన్స్ (Strings & Functions)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను క్షుణ్ణంగా నేర్చుకుంటారు:
1. పైథాన్‌లో స్ట్రింగ్ మానిప్యులేషన్ (క్లీనింగ్, స్ప్లిటింగ్, జాయినింగ్, లేటెస్ట్ f-strings).
2. కోడ్‌ని పదే పదే రాయకుండా **DRY (Don't Repeat Yourself)** సిద్ధాంతంతో ఫంక్షన్స్ రాయడం.
3. ఫంక్షన్ పారామీటర్లు: Positional, Keyword, Default మరియు `*args`, `**kwargs`.
4. వేరియబుల్ పరిధి (Scope) మరియు **LEGB** నియమం.
5. సింగిల్ లైన్ ఫంక్షన్స్: **లాంబ్డా ఎక్స్‌ప్రెషన్స్ (Lambda Functions)** ఎప్పుడు వాడాలి?

---

## 1. స్ట్రింగ్స్ & ఫంక్షన్స్ ఎందుకు అత్యంత కీలకం? (The "Why")

ముఖ్యంగా ఆధునిక **ఆర్టిఫిషియల్ ఇంటెలిజెన్స్ (AI / GenAI)** రంగంలో:
- **స్ట్రింగ్స్ అంటే AI కి కరెన్సీ లాంటివి:** మనం ChatGPT లేదా Gemini కి పంపే ప్రాంప్ట్, డాక్యుమెంట్స్ నుండి తీసుకునే టెక్స్ట్, AI తిరిగి ఇచ్చే రెస్పాన్స్... అన్నీ స్ట్రింగ్స్ రూపంలోనే ఉంటాయి. స్ట్రింగ్స్‌ని క్లీన్ చేయడం రాకపోతే AI అప్లికేషన్లను తయారు చేయడం అసాధ్యం!
- **ఫంక్షన్స్ అంటే లెగో బ్లాక్స్ (Lego Bricks) లాంటివి:** ఎలాంటి ఫంక్షన్స్ లేకుండా 500 లైన్ల కోడ్ ఒకే పేజీలో రాస్తే దాన్ని డీబగ్ చేయడం నరకం. ఫంక్షన్స్ రాస్తే ఆ కోడ్‌ని ఎవరైనా సులభంగా అర్థం చేసుకోవచ్చు మరియు మళ్లీ మళ్లీ వాడుకోవచ్చు.

---

## 2. స్ట్రింగ్స్‌తో ఆడుకోవడం (String Manipulation)

పైథాన్‌లో స్ట్రింగ్స్ **ఇమ్మ్యూటబుల్ (Immutable)**. అంటే ఒకసారి క్రియేట్ చేసిన స్ట్రింగ్‌ని మార్చలేము; ఏ మార్పు చేసినా కొత్త స్ట్రింగ్ వస్తుంది.

```python
raw_prompt = "   ### USER QUESTION: AI మోడల్ ఎలా ట్రైన్ చేయాలి?   \n"

# 1. అనవసరమైన స్పేస్‌లు మరియు కొత్త లైన్లను తీసివేయడం (.strip())
clean_prompt = raw_prompt.strip()
print(f"క్లీన్ చేసిన టెక్స్ట్: '{clean_prompt}'")

# 2. క్యాపిటల్ / స్మాల్ లెటర్స్‌గా మార్చడం
print("Upper:", clean_prompt.upper())
print("Lower:", clean_prompt.lower())

# 3. విడదీయడం (.split()) మరియు కలపడం (.join())
sentence = "python,fastapi,docker,langchain,chroma"
tags = sentence.split(",")                # స్ట్రింగ్‌ని లిస్ట్‌గా మారుస్తుంది
print("ట్యాగ్స్ లిస్ట్:", tags)

reconstructed = " | ".join(tags)          # లిస్ట్‌ని మళ్లీ స్ట్రింగ్‌గా కలుపుతుంది
print("కలిపిన స్ట్రింగ్:", reconstructed)

# 4. ముందు/వెనుక పదాలు చెక్ చేయడం (.endswith(), .startswith())
filename = "invoice_2026_march.pdf"
print("ఇది PDF ఫైలా?:", filename.endswith(".pdf"))
print("ఇది ఇన్వాయిస్ ఫైలా?:", filename.startswith("invoice_"))

# 5. లేటెస్ట్ f-strings (అంకెలను అందంగా ఫార్మాట్ చేయడం)
cpu_usage = 84.5678
active_users = 14250
print(f"సర్వర్ లోడ్: {cpu_usage:.1f}% | యాక్టివ్ యూజర్లు: {active_users:,}")
```

---

## 3. ఫంక్షన్స్ రాయడం & పిలవడం (Defining & Calling Functions)

### గోల్డెన్ రూల్: ఒక ఫంక్షన్ కేవలం ఒకే ఒక బాధ్యతను నిర్వర్తించాలి (Single Responsibility)

```python
# ఫంక్షన్ నిర్వచనం (def అంటే define)
def calculate_tax(income: float, tax_rate: float = 0.18) -> float:
    """ఇచ్చిన ఆదాయంపై పన్నును లెక్కిస్తుంది. డీఫాల్ట్‌గా 18% GST తీసుకుంటుంది."""
    calculated_tax = income * tax_rate
    return calculated_tax

# ఫంక్షన్‌ని ఉపయోగించడం (Calling)
service_bill = 5000.0

# 1. డీఫాల్ట్ టాక్స్ (18%) తో లెక్కించడం:
tax_default = calculate_tax(service_bill)

# 2. మనకు నచ్చిన టాక్స్ (5%) ఇచ్చి లెక్కించడం:
tax_custom = calculate_tax(service_bill, tax_rate=0.05)

print(f"డీఫాల్ట్ పన్ను (18%): ₹{tax_default}")
print(f"కస్టమ్ పన్ను (5%)  : ₹{tax_custom}")
```

---

## 4. ఫంక్షన్ ఆర్గ్యుమెంట్స్: `*args` మరియు `**kwargs`

ఓపెన్ సోర్స్ AI లైబ్రరీలలో (LangChain, Hugging Face) ఎక్కడ చూసినా `*args` మరియు `**kwargs` కనిపిస్తాయి. చాలామంది ఫ్రెషర్స్ వీటిని చూసి భయపడతారు. కానీ కాన్సెప్ట్ చాలా సులభం:

```python
# 1. *args: ఎన్ని నెంబర్లైనా లేదా విలువనైనా పంపవచ్చు -> అవి TUPLE గా మారతాయి
def calculate_cart_total(*prices):
    total = sum(prices)
    return total

print("కార్ట్ 1 మొత్తం:", calculate_cart_total(100, 250, 400))  # 750
print("కార్ట్ 2 మొత్తం:", calculate_cart_total(50, 20))         # 70

# 2. **kwargs: ఎన్ని కీ-వాల్యూ (కీవర్డ్) ఆప్షన్లయినా పంపవచ్చు -> అవి DICTIONARY గా మారతాయి
def create_ai_agent(agent_name, model="gemini-1.5-pro", **config):
    print(f"\nAI ఏజెంట్ ప్రారంభం: '{agent_name}' (మోడల్: {model})")
    for key, value in config.items():
        print(f"  - సెట్టింగ్ [{key}]: {value}")

create_ai_agent(
    "CodeReviewer",
    temperature=0.2,
    max_tokens=2048,
    memory_type="vector_store"
)
```

---

## 5. వేరియబుల్ పరిధి (Scope) & LEGB నియమం

పైథాన్ ఒక వేరియబుల్‌ని వెతికేటప్పుడు **LEGB** క్రమాన్ని పాటిస్తుంది:
1. **L**ocal: ప్రస్తుత ఫంక్షన్ లోపల వెతుకుతుంది.
2. **E**nclosing: బయట ఉన్న పేరెంట్ ఫంక్షన్లలో వెతుకుతుంది.
3. **G**lobal: మొత్తం ఫైల్ మొదట్లో డిఫైన్ చేసిన వేరియబుల్స్.
4. **B**uilt-in: పైథాన్ స్వతహాగా ఇచ్చేవి (`print`, `len`, `int`).

```python
# గ్లోబల్ స్కోప్ (Global)
company_name = "TechIn AI Labs"

def generate_badge(employee_name):
    # లోకల్ స్కోప్ (Local)
    department = "ఇంజనీరింగ్"
    badge_info = f"[{company_name}] {employee_name} - {department}"
    return badge_info

print(generate_badge("సతీష్"))
# print(department) # ❌ NameError వస్తుంది! ఎందుకంటే ఫంక్షన్ బయట department ఉండదు.
```

---

## 6. లాంబ్డా ఫంక్షన్స్ (Lambda Functions - అనామక ఫంక్షన్లు)

పేరు లేకుండా ఒకే లైన్‌లో రాసే చిన్న ఫంక్షన్లను లాంబ్డా అంటారు.
**సింటాక్స్**: `lambda arguments: expression`

```python
# సాధారణ ఫంక్షన్
def double(x):
    return x * 2

# అదే పని చేసే లాంబ్డా ఫంక్షన్
double_lambda = lambda x: x * 2
print(double_lambda(5))  # 10

# డేటాను సార్ట్ (Sort) చేయడంలో లాంబ్డా చాలా అద్భుతంగా పనిచేస్తుంది:
students = [
    {"name": "స్నేహ", "gpa": 8.9},
    {"name": "అర్జున్", "gpa": 9.4},
    {"name": "కావ్య", "gpa": 7.8}
]

# GPA ఎక్కువ ఉన్నవారిని మొదటి వరుసలో ఉంచడం:
sorted_by_gpa = sorted(students, key=lambda s: s["gpa"], reverse=True)
print("టాప్ స్టూడెంట్స్:", sorted_by_gpa)
```

---

## 7. ఫ్రెషర్స్ చేసే అతి పెద్ద తప్పు (Warning Trap!)

⚠️ **మ్యూటబుల్ డీఫాల్ట్ ఆర్గ్యుమెంట్ ట్రాప్ (Python No.1 Interview Trap):**
```python
# ❌ ప్రమాదకరమైన పద్ధతి: ఫంక్షన్ డిఫైన్ చేసినప్పుడు డీఫాల్ట్ లిస్ట్ ఒక్కసారే క్రియేట్ అవుతుంది!
def add_item(item, basket=[]):
    basket.append(item)
    return basket

print(add_item("Apple"))   # ['Apple']
print(add_item("Banana"))  # ['Apple', 'Banana'] -> పాత ఆపిల్ కూడా కలిసిపోయింది!

# ✅ సరైన పద్ధతి: None ని డీఫాల్ట్‌గా పెట్టాలి
def add_item_safe(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

---

## 8. ప్రాక్టీస్ ల్యాబ్ (Daily Hands-On Lab)

### 🧪 టాస్క్: AI ప్రాంప్ట్ శానిటైజర్ & టోకెన్ ఖర్చు అంచనా ప్రోగ్రామ్
**సన్నివేశం:** AI మోడల్స్‌కి యూజర్లు ఇచ్చే టెక్స్ట్‌లో స్పేస్‌లు శుభ్రం చేయాలి, పాస్‌వర్డ్‌లు లాంటి రహస్య పదాలను తొలగించి `[REDACTED]` పెట్టాలి మరియు API ఖర్చును లెక్కించాలి (దాదాపు 4 అక్షరాలు = 1 టోకెన్).

```python
# ==========================================
# Day 4 Lab: AI ప్రాంప్ట్ శానిటైజర్
# ==========================================

BANNED_WORDS = {"password", "secret_key", "aadhaar", "ssn"}

def sanitize_prompt(raw_text: str) -> str:
    """అనవసరమైన స్పేస్‌లను తొలగిస్తుంది."""
    cleaned = " ".join(raw_text.strip().split())
    return cleaned

def redact_sensitive_info(text: str, sensitive_words: set) -> str:
    """రహస్య సమాచారాన్ని [REDACTED] తో భర్తీ చేస్తుంది."""
    words = text.split()
    redacted_words = [
        "[REDACTED]" if word.lower().strip(".,!?") in sensitive_words else word
        for word in words
    ]
    return " ".join(redacted_words)

def estimate_tokens_and_cost(text: str, cost_per_1k_tokens_usd: float = 0.0015) -> dict:
    """టోకెన్లు మరియు ఖర్చును అంచనా వేస్తుంది."""
    char_count = len(text)
    estimated_tokens = max(1, char_count // 4)
    estimated_cost_usd = (estimated_tokens / 1000) * cost_per_1k_tokens_usd
    estimated_cost_inr = estimated_cost_usd * 83.0

    return {
        "అక్షరాలు": char_count,
        "అంచనా టోకెన్లు": estimated_tokens,
        "ఖర్చు డాలర్లలో": f"${estimated_cost_usd:.6f}",
        "ఖర్చు రూపాయల్లో": f"₹{estimated_cost_inr:.4f}"
    }

# టెస్ట్ చేద్దాం
user_input = "   నా password వెరిఫై చేసి ఎంప్లాయ్ 901 కి సాలరీ పంపండి.   "

print("అసలైన టెక్స్ట్   :", repr(user_input))
clean_step = sanitize_prompt(user_input)
safe_step = redact_sensitive_info(clean_step, BANNED_WORDS)
metrics = estimate_tokens_and_cost(safe_step)

print("శానిటైజ్ చేసిన టెక్స్ట్:", safe_step)
print("ఖర్చు వివరాలు     :", metrics)
```

---

## 9. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: పైథాన్‌లో మ్యూటబుల్ డీఫాల్ట్ ఆర్గ్యుమెంట్ బగ్ అంటే ఏమిటి?**
   - **సమాధానం:** ఫంక్షన్ నిర్వచించినప్పుడు మాత్రమే డీఫాల్ట్ ఆర్గ్యుమెంట్‌లు ఎవల్యూట్ అవుతాయి. లిస్ట్ లేదా డిక్షనరీ లాంటి మ్యూటబుల్ ఆబ్జెక్టులను డీఫాల్ట్‌గా పెడితే, ఫంక్షన్‌ను ఎన్నిసార్లు పిలిచినా అదే ఆబ్జెక్ట్‌ను షేర్ చేసుకుంటాయి. దీని పరిష్కారంగా `None` ను డీఫాల్ట్‌గా పెట్టి ఫంక్షన్ లోపల కొత్త లిస్ట్‌ను క్రియేట్ చేయాలి.
2. **ప్రశ్న: LEGB నియమం అంటే ఏమిటి?**
   - **సమాధానం:** పైథాన్ ఒక వేరియబుల్‌ని వెతికే ఆర్డర్ ఇది: Local (ఫంక్షన్ లోపల), Enclosing (బయటి ఫంక్షన్లలో), Global (మొత్తం ఫైల్‌లో), Built-in (పైథాన్ అంతర్నిర్మిత ఫంక్షన్లలో).
3. **ప్రశ్న: `*args` మరియు `**kwargs` మధ్య తేడా ఏమిటి?**
   - **సమాధానం:** `*args` అనేది పొజిషనల్ ఆర్గ్యుమెంట్లను టపుల్ (Tuple) రూపంలో తీసుకుంటుంది. `**kwargs` అనేది కీవర్డ్ ఆర్గ్యుమెంట్లను డిక్షనరీ (Dictionary) రూపంలో తీసుకుంటుంది.
