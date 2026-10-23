# డే 05 (Day 05): ఫైల్ హ్యాండ్లింగ్ & ఎక్సెప్షన్ మేనేజ్‌మెంట్ (Module 01 Capstone)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను క్షుణ్ణంగా నేర్చుకుంటారు:
1. `with` స్టేట్‌మెంట్ (**Context Managers**) ఉపయోగించి ఫైల్స్‌ను సురక్షితంగా చదవడం మరియు రాయడం.
2. కంపెనీలలో అత్యధికంగా వాడే ఫార్మాట్లు: **JSON** మరియు **CSV** ఫైల్స్ హ్యాండ్లింగ్.
3. ప్రోగ్రామ్ క్రాష్ అవ్వకుండా ఎర్రర్ హ్యాండ్లింగ్ చేయడం (`try`, `except`, `else`, `finally`).
4. అనవసరపు `print` వాడకుండా ప్రొడక్షన్ లెవల్ **లాగింగ్ (Logging)** సెటప్ చేయడం.
5. **మాడ్యూల్ 01 క్యాప్‌స్టోన్ మినీ ప్రాజెక్ట్**: ఖర్చుల ట్రాకర్ (CLI Expense Tracker with JSON Persistence).

---

## 1. ఫైల్స్ & ఎక్సెప్షన్ హ్యాండ్లింగ్ ఎందుకు అవసరం? (The "Why")

- **కంప్యూటర్ స్విచ్ ఆఫ్ అయితే వేరియబుల్స్ మాయమైపోతాయి:** మనం RAM లో స్టోర్ చేసే డేటా తాత్కాలికం. ఫైల్స్ (లేదా డేటాబేస్) లో సేవ్ చేస్తేనే ఆ డేటా జీవితాంతం పదిలంగా ఉంటుంది.
- **రియల్ వరల్డ్ ఎప్పుడూ పర్ఫెక్ట్‌గా ఉండదు:** రియల్ టైమ్ సర్వర్లలో ఇంటర్నెట్ పోవచ్చు, డిస్క్ నిండిపోవచ్చు లేదా యూజర్ తప్పుడు నెంబర్లు టైప్ చేయవచ్చు. మనం సరైన ఎక్సెప్షన్ హ్యాండ్లింగ్ చేయకపోతే, అర్ధరాత్రి 2 గంటలకి మీ సర్వర్ క్రాష్ అయి కంపెనీకి లక్షల్లో నష్టం వస్తుంది!

---

## 2. ఫైల్ హ్యాండ్లింగ్ & `with` స్టేట్‌మెంట్ (Context Managers)

### తాళం ఉదాహరణ (Lock Analogy):
- `with` లేకుండా ఫైల్ ఓపెన్ చేస్తే, పని అయిపోయాక మనమే గుర్తుపెట్టుకుని `file.close()` చేయాలి. ఒకవేళ మధ్యలో కరెంట్ పోయినా లేదా ఎర్రర్ వచ్చినా ఫైల్ అలాగే లాక్ అయిపోతుంది!
- అదే `with` వాడితే, లోపల ఏం జరిగినా సరే పని పూర్తవగానే పైథాన్ ఆటోమేటిక్‌గా ఫైల్‌ని సురక్షితంగా క్లోజ్ చేస్తుంది.

```python
# టెక్స్ట్ ఫైల్‌లోకి డేటా రాయడం (mode="a" అంటే append - చివర్లో చేరుస్తుంది)
log_entry = "2026-10-15 10:00:00 | సిస్టమ్ ప్రారంభమైంది | Status: HEALTHY\n"

with open("app.log", mode="a", encoding="utf-8") as f:
    f.write(log_entry)

# టెక్స్ట్ ఫైల్ నుండి డేటా చదవడం (mode="r" అంటే read)
with open("app.log", mode="r", encoding="utf-8") as f:
    content = f.read()
    print("లాగ్ ఫైల్ వివరాలు:\n", content)
```

---

## 3. JSON & CSV ఫైల్స్ నిర్వహణ (Working with JSON & CSV)

### A. JSON ఫైల్స్ (వెబ్ APIs మరియు AI కి ప్రాణం)
JSON అనేది వెబ్‌సైట్లు, మొబైల్ యాప్స్ మరియు AI మోడల్స్ మధ్య డేటా మార్పిడికి ఉపయోగించే గ్లోబల్ స్టాండర్డ్.

```python
import json

# పైథాన్ డిక్షనరీని JSON ఫైల్‌గా సేవ్ చేయడం (json.dump)
user_session = {
    "user_id": 1045,
    "username": "satish_g",
    "roles": ["admin", "ai_developer"],
    "preferences": {"theme": "dark", "notifications": True}
}

with open("session.json", "w", encoding="utf-8") as f:
    json.dump(user_session, f, indent=4)  # indent=4 ఇస్తే చూడటానికి అందంగా అమరుస్తుంది

# JSON ఫైల్ నుండి పైథాన్ డిక్షనరీలోకి డేటా లోడ్ చేయడం (json.load)
with open("session.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print("యూజర్‌నేమ్:", loaded_data["username"])
```

### B. CSV ఫైల్స్ (డేటా సైన్స్ మరియు ఎక్సెల్ షీట్లు)

```python
import csv

# CSV లోకి కొత్త రికార్డులు రాయడం
employees = [
    ["EmpID", "Name", "Department", "Salary"],
    [101, "ఆరవ్", "AI Labs", 95000],
    [102, "దివ్య", "Data Platform", 88000]
]

with open("employees.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(employees)

# CSV నుండి రికార్డులు చదవడం
with open("employees.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print("వరుస వివరాలు:", row)
```

---

## 4. ఎర్రర్ హ్యాండ్లింగ్ (`try`, `except`, `else`, `finally`)

### 4 బ్లాక్స్ అర్థం:
- `try`: ఎర్రర్ వచ్చే అవకాశం ఉన్న రిస్కీ కోడ్ ఇక్కడ రాస్తాం.
- `except`: ఒకవేళ ఎర్రర్ వస్తే ప్రోగ్రామ్ ఆగిపోకుండా ప్రత్యామ్నాయంగా ఏం చేయాలో ఇక్కడ చెప్తాం.
- `else`: ఎలాంటి ఎర్రర్ రాకపోతే మాత్రమే ఇది రన్ అవుతుంది.
- `finally`: ఎర్రర్ వచ్చినా రాకపోయినా ఇది **తప్పకుండా రన్ అవుతుంది** (క్లీనప్ పనుల కోసం).

```python
def process_user_payment(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("చెల్లించాల్సిన మొత్తం సున్నా కంటే ఎక్కువ ఉండాలి.")
        print(f"✅ ₹{amount:,.2f} లావాదేవీని ప్రాసెస్ చేస్తున్నాం...")
    except ValueError as err:
        print(f"❌ ఇన్‌పుట్ లోపం (Validation Error): {err}")
    except Exception as general_err:
        print(f"🚨 ఊహించని సిస్టమ్ లోపం: {general_err}")
    else:
        print("🎉 పేమెంట్ విజయవంతమైంది! రసీదు పంపబడింది.")
    finally:
        print("🔒 డేటాబేస్ కనెక్షన్ క్లోజ్ చేయబడింది.\n")

process_user_payment("1500.50")  # సరైన కేస్
process_user_payment("-500")     # మైనస్ వాల్యూ కేస్
process_user_payment("abc")      # అక్షరాలు ఇచ్చిన కేస్
```

---

## 5. ప్రొఫెషనల్ లాగింగ్ (Logging - ప్రింట్‌లు బంద్ చేయండి!)

పెద్ద కంపెనీలలో ఎవరూ `print()` స్టేట్‌మెంట్లను డీబగ్గింగ్ కోసం వాడరు. `logging` లైబ్రరీ ద్వారా సమయం, ఎర్రర్ స్థాయి (INFO, WARNING, ERROR) తో సహా లాగ్స్ రికార్డ్ చేస్తారు:

```python
import logging

# లాగర్ కాన్ఫిగరేషన్
logging.basicConfig(
    filename="production.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("BillingService")

logger.info("బిల్లింగ్ సర్వీస్ విజయవంతంగా ప్రారంభమైంది.")
logger.warning("పేమెంట్ గేట్‌వే స్పందించడానికి 800ms కంటే ఎక్కువ సమయం పడుతోంది.")
try:
    10 / 0
except ZeroDivisionError:
    logger.error("టాక్స్ కాలిక్యులేషన్‌లో జీరో డివిజన్ ఎర్రర్ వచ్చింది!", exc_info=True)
```

---

## 6. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Pitfalls)

1. **కేవలం `except:` అని ఖాళీగా వదిలేయడం (Bare Except):**
   - ఏ రకమైన ఎర్రర్ అని చెప్పకుండా కేవలం `except:` రాస్తే సిస్టమ్ ఎర్రర్లు, కీబోర్డ్ ఇంటరప్ట్‌లు అన్నీ దాగిపోతాయి. కచ్చితంగా `except ValueError as e:` లాంటి స్పెసిఫిక్ ఎర్రర్ టైప్స్ వాడాలి.
2. **`encoding="utf-8"` మర్చిపోవడం:**
   - విండోస్‌లో తెలుగు అక్షరాలు లేదా ఎమోజీలు ఉన్న ఫైల్స్ ఓపెన్ చేసినప్పుడు UTF-8 పెట్టకపోతే క్రాష్ అవుతుంది.
3. **`"w"` కి మరియు `"a"` కి తేడా:**
   - `"w"` (write) మోడ్‌లో ఓపెన్ చేస్తే ఫైల్‌లో ఉన్న పాత డేటా మొత్తం డిలీట్ అయిపోతుంది! పాతది ఉంచి కొత్తది కలపాలంటే `"a"` (append) వాడాలి.

---

## 7. మాడ్యూల్ 01 క్యాప్‌స్టోన్ మినీ ప్రాజెక్ట్: పర్సనల్ ఎక్స్‌పెన్స్ ట్రాకర్ (CLI Tool)

గత 5 రోజుల్లో నేర్చుకున్న అన్ని కాన్సెప్ట్‌లు (వేరియబుల్స్, కండిషన్స్, లూప్స్, కలెక్షన్స్, ఫంక్షన్స్, ఫైల్స్, ఎక్సెప్షన్స్) కలిపి ఈ ప్రాజెక్ట్ రూపొందించబడింది:

```python
# =========================================================
# Module 01 Capstone: ఖర్చుల నిర్వహణ సాఫ్ట్‌వేర్ (CLI App)
# =========================================================
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

def load_expenses() -> list:
    """JSON ఫైల్ నుండి ఖర్చుల డేటాను లోడ్ చేస్తుంది. ఫైల్ లేకపోతే ఖాళీ లిస్ట్ ఇస్తుంది."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ ఫైల్ పాడైపోయింది. కొత్త లెడ్జర్‌తో ప్రారంభిస్తున్నాం.")
        return []

def save_expenses(expenses: list):
    """ఖర్చుల డేటాను సురక్షితంగా JSON ఫైల్‌లో సేవ్ చేస్తుంది."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)

def add_expense(expenses: list):
    """యూజర్ నుండి కొత్త ఖర్చు వివరాలు నమోదు చేసుకుంటుంది."""
    title = input("ఖర్చు దేనికోసం? (ఉదా: కిరాణా, అద్దె): ").strip()
    if not title:
        print("❌ వివరాలు ఖాళీగా ఉండకూడదు.")
        return

    category = input("కేటగిరీ ఎంచుకోండి (Food, Travel, Rent, Misc): ").strip()
    try:
        amount = float(input("మొత్తం రూపాయల్లో ఇవ్వండి: "))
        if amount <= 0:
            print("❌ మొత్తం పాజిటివ్ సంఖ్య అయి ఉండాలి.")
            return
    except ValueError:
        print("❌ సరైన సంఖ్యను నమోదు చేయండి.")
        return

    record = {
        "id": len(expenses) + 1,
        "title": title,
        "category": category.title(),
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    expenses.append(record)
    save_expenses(expenses)
    print(f"✅ '{title}' (₹{amount:,.2f}) విజయవంతంగా నమోదైంది!")

def view_summary(expenses: list):
    """మొత్తం ఖర్చులు మరియు కేటగిరీల వారీగా విభజించి చూపిస్తుంది."""
    if not expenses:
        print("ℹ️ ఇంతవరకు ఎలాంటి ఖర్చులు నమోదు చేయలేదు.")
        return

    total_spend = sum(item["amount"] for item in expenses)
    print("\n" + "="*45)
    print(f"💰 మొత్తం ఖర్చు: ₹{total_spend:,.2f}")
    print("="*45)

    category_totals = {}
    for item in expenses:
        cat = item["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + item["amount"]

    for cat, total in category_totals.items():
        percentage = (total / total_spend) * 100
        print(f"  • {cat:15}: ₹{total:,.2f} ({percentage:.1f}%)")
    print("="*45)

def main():
    expenses = load_expenses()
    while True:
        print("\n--- 📊 పర్సనల్ ఎక్స్‌పెన్స్ మేనేజర్ ---")
        print("1. కొత్త ఖర్చు నమోదు చేయండి")
        print("2. ఖర్చుల సమ్మరీ చూడండి")
        print("3. బయటకు వెళ్లండి (Exit)")
        choice = input("ఒక ఆప్షన్‌ను ఎంచుకోండి (1-3): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            print("ధన్యవాదాలు! మీ బడ్జెట్ జాగ్రత్తగా చూసుకోండి.")
            break
        else:
            print("❌ తప్పుడు ఆప్షన్. దయచేసి 1, 2 లేదా 3 ఎంచుకోండి.")

if __name__ == "__main__":
    main()
```

---

## 8. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: పైథాన్‌లో కాంటెక్స్ట్ మేనేజర్ (Context Manager) అంటే ఏమిటి? `with` స్టేట్‌మెంట్ ఎలా పనిచేస్తుంది?**
   - **సమాధానం:** కాంటెక్స్ట్ మేనేజర్ అనేది రిసోర్స్‌లను (ఫైల్స్, నెట్‌వర్క్ లేదా డేటాబేస్ కనెక్షన్లు) సురక్షితంగా ఓపెన్ చేసి క్లోజ్ చేయడానికి ఉపయోగించే ప్రోటోకాల్. ఇది అంతర్గతంగా `__enter__()` మరియు `__exit__()` మెథడ్స్‌ను అమలు చేస్తుంది. `with` బ్లాక్ లోపల ఏదైనా ఎర్రర్ వచ్చినా సరే `__exit__()` కాల్ అయ్యి రిసోర్స్‌లు సురక్షితంగా క్లోజ్ అవుతాయి.
2. **ప్రశ్న: `json.dump()` కి మరియు `json.dumps()` కి మధ్య తేడా ఏమిటి?**
   - **సమాధానం:** `json.dump()` అనేది డేటాను నేరుగా ఓపెన్ చేసిన ఫైల్‌లోకి రాస్తుంది. `json.dumps()` (dump string) అనేది పైథాన్ ఆబ్జెక్ట్‌ను స్ట్రింగ్ రూపంలోకి (మెమొరీలో) సీరియలైజ్ చేస్తుంది.
3. **ప్రశ్న: `try` బ్లాక్ లోపల `return` చేసినా `finally` బ్లాక్ రన్ అవుతుందా?**
   - **సమాధానం:** ఖచ్చితంగా అవుతుంది! `try` బ్లాక్‌లో `return` లేదా `break` స్టేట్‌మెంట్లు ఉన్నప్పటికీ, ఫంక్షన్ బయటకు వెళ్లకముందే `finally` బ్లాక్‌లోని కోడ్ తప్పనిసరిగా ఎగ్జిక్యూట్ అవుతుంది.
