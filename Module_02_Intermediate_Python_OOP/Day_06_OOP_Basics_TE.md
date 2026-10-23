# డే 06 (Day 06): ఆబ్జెక్ట్ ఓరియెంటెడ్ ప్రోగ్రామింగ్ (OOP Fundamentals)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను చాలా స్పష్టంగా అర్థం చేసుకుంటారు:
1. అసలు OOP అంటే ఏమిటి? డేటా మరియు ఫంక్షన్లను కలిపి భద్రపరచడం.
2. క్లాస్ (Class) రాయడం, ఆబ్జెక్ట్ (Object) క్రియేట్ చేయడం మరియు `__init__`, `self` ల అసలు అర్థం.
3. ఎన్‌క్యాప్సులేషన్ (Encapsulation): డేటా రక్షణ మరియు ఆధునిక `@property` వాడకం.
4. మూడు రకాల మెథడ్స్ మధ్య తేడాలు: Instance Methods, `@classmethod` మరియు `@staticmethod`.

---

## 1. అసలు OOP ఎందుకు వాడాలి? (The "Why")

ఒక చిన్న బ్యాంకింగ్ ప్రోగ్రామ్ రాస్తున్నాం అనుకుందాం. క్లాసులు లేకుండా కేవలం డిక్షనరీలు మాత్రమే వాడితే:
```python
# సాధారణ పద్ధతిలో రాస్తే:
account1 = {"acc_num": "SB-101", "balance": 5000}

# ఎవరైనా పొరపాటున ఎక్కడి నుంచైనా ఇలా చేసేయొచ్చు:
account1["balance"] = -9999999  # డేటా కరప్ట్ అయిపోయింది!
```
ఇలా డేటాని విడిగా వదిలేస్తే ఎవరైనా తప్పులు చేయొచ్చు.
**OOP ఏం చేస్తుందంటే - డేటాని మరియు ఆ డేటాతో పనిచేసే ఫంక్షన్లను కలిపి ఒకే రక్షక కవచంలో ఉంచుతుంది.** దాన్నే **ఆబ్జెక్ట్ (Object)** అంటాం.

### రియల్ వరల్డ్ ఉదాహరణ (Real-World Analogy):
- **క్లాస్ (Class):** ఒక భవనం యొక్క **బ్లూప్రింట్ (ప్లాన్ లేదా పటం)** లాంటిది. ప్లాన్ గీయడానికి సిమెంట్ లేదా ఇటుకలు అవసరం లేదు; అది కేవలం నియమాలు మరియు కొలతలతో కూడిన కాగితం.
- **ఆబ్జెక్ట్ (Object / Instance):** ఆ బ్లూప్రింట్ చూసి **నిజంగా నిర్మించిన ఇల్లు!** ఒకే ప్లాన్‌తో 50 ఇళ్ళు కట్టొచ్చు, ఒక్కో ఇంటికి వేర్వేరు రంగులు, వేర్వేరు వ్యక్తులు ఉంటారు.

---

## 2. క్లాస్ నిర్మాణం: `self` మరియు `__init__`

ఫ్రెషర్స్‌కి `self` అంటే చాలా కన్‌ఫ్యూజన్ ఉంటుంది.
- **`self` అంటే "ప్రస్తుతం మనం మాట్లాడుతున్న నిర్దిష్టమైన ఆబ్జెక్ట్" అని అర్థం.**
- మనం `acc1.deposit(500)` అన్నప్పుడు, పైథాన్ అంతర్గతంగా `BankAccount.deposit(acc1, 500)` గా మారుస్తుంది.

```python
class BankAccount:
    # క్లాస్ అట్రిబ్యూట్ (అన్ని అకౌంట్లకు ఉమ్మడిగా ఉండేది)
    BANK_NAME = "టీచిన్ ఫిన్‌టెక్ బ్యాంక్"
    INTEREST_RATE = 0.04  # 4% వార్షిక వడ్డీ

    # కన్‌స్ట్రక్టర్ / ఇనీషియలైజర్ (కొత్త అకౌంట్ ఓపెన్ చేసిన ప్రతిసారీ ఇది రన్ అవుతుంది)
    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        # ఇన్‌స్టాన్స్ అట్రిబ్యూట్స్ (ఒక్కో అకౌంట్‌కి ప్రత్యేకంగా ఉండేవి)
        self.account_holder = account_holder
        self.balance = initial_balance

    # ఇన్‌స్టాన్స్ మెథడ్ (ఈ నిర్దిష్ట అకౌంట్‌పై మాత్రమే పనిచేస్తుంది)
    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("డిపాజిట్ మొత్తం సున్నా కంటే ఎక్కువ ఉండాలి.")
        self.balance += amount
        print(f"✅ ₹{amount:,.2f} డిపాజిట్ విజయవంతమైంది. ప్రస్తుత బ్యాలెన్స్: ₹{self.balance:,.2f}")

    def withdraw(self, amount: float):
        if amount > self.balance:
            print(f"❌ విత్‌డ్రా విఫలమైంది! ఖాతాలో సరిపడా నిధులు లేవు.")
            return False
        self.balance -= amount
        print(f"💵 ₹{amount:,.2f} విత్‌డ్రా అయింది. మిగిలిన బ్యాలెన్స్: ₹{self.balance:,.2f}")
        return True

# ఆబ్జెక్ట్స్ క్రియేట్ చేయడం (ఇళ్లు కట్టడం లాంటిది)
acc1 = BankAccount("రాహుల్ శర్మ", 15000)
acc2 = BankAccount("ప్రియా పటేల్", 50000)

acc1.deposit(2500)
acc1.withdraw(20000)  # ఫెయిల్ అవుతుంది (సరిపడా బ్యాలెన్స్ లేదు)
acc2.withdraw(10000)  # సక్సెస్ అవుతుంది
```

---

## 3. ఎన్‌క్యాప్సులేషన్ & `@property` (Encapsulation)

పైథాన్‌లో డేటాను రక్షించడానికి మూడు రకాల పద్ధతులు ఉంటాయి:
- `name` : పబ్లిక్ (ఎవరైనా నేరుగా చూడొచ్చు, మార్చొచ్చు).
- `_name` : ప్రొటెక్టెడ్ (సాధారణంగా బయటివారు మార్చకూడదని చెప్పే సూచన).
- `__name` : ప్రైవేట్ (పైథాన్ దీని పేరును లోపల మార్చేస్తుంది - నేమ్ మాంగ్లింగ్).

డేటాను మార్చేముందు రూల్స్ చెక్ చేయడానికి `@property` డెకరేటర్ వాడతాం:

```python
class Employee:
    def __init__(self, name: str, monthly_salary: float):
        self.name = name
        self._monthly_salary = monthly_salary  # ప్రొటెక్టెడ్ అట్రిబ్యూట్

    # Getter: శాలరీని వేరియబుల్‌లా సులభంగా చదవడానికి (emp.salary)
    @property
    def salary(self) -> float:
        return self._monthly_salary

    # Setter: శాలరీని మార్చేముందు రూల్స్ చెక్ చేస్తుంది
    @salary.setter
    def salary(self, new_salary: float):
        if new_salary < 15000:
            raise ValueError("జీతం కనీస వేతనం (₹15,000) కంటే తక్కువ ఉండకూడదు!")
        print(f"{self.name} జీతం ₹{new_salary:,.2f} కి అప్‌డేట్ చేయబడింది.")
        self._monthly_salary = new_salary

emp = Employee("విక్రమ్", 45000)
print(f"ప్రస్తుత జీతం: ₹{emp.salary:,.2f}")

emp.salary = 55000     # ఆటోమేటిక్‌గా @salary.setter ని కాల్ చేస్తుంది!
# emp.salary = 5000    # ❌ రూల్ బ్రేక్ అయి ValueError వస్తుంది!
```

---

## 4. మూడు రకాల మెథడ్స్ (Instance, Class, Static Methods)

| మెథడ్ రకం | డెకరేటర్ | మొదటి పారామీటర్ | ఏం చేయగలదు? | ఎప్పుడు వాడాలి? |
| :--- | :--- | :--- | :--- | :--- |
| **Instance Method** | ఏమీ ఉండదు | `self` | నిర్దిష్ట ఆబ్జెక్ట్ డేటాతో పనిచేస్తుంది | సాధారణంగా ఆబ్జెక్ట్ పనుల కోసం |
| **Class Method** | `@classmethod` | `cls` | మొత్తం క్లాస్ డేటాతో పనిచేస్తుంది | డిక్షనరీ/JSON నుండి ఆబ్జెక్ట్ క్రియేట్ చేయడానికి |
| **Static Method** | `@staticmethod` | ఏమీ ఉండదు | కేవలం ఒక హెల్పర్ లాజిక్ మాత్రమే | క్లాస్‌తో సంబంధం ఉన్న సాధారణ ఫంక్షన్లకు |

```python
class User:
    TOTAL_USERS = 0  # క్లాస్ వేరియబుల్

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        User.TOTAL_USERS += 1

    # ఇన్‌స్టాన్స్ మెథడ్ (యూజర్‌కి ఈమెయిల్ పంపడం)
    def send_welcome_email(self):
        print(f"{self.email} కి వెల్‌కమ్ ఈమెయిల్ పంపుతున్నాం...")

    # క్లాస్ మెథడ్ (డిక్షనరీ నుండి నేరుగా యూజర్‌ని తయారు చేస్తుంది - Factory)
    @classmethod
    def from_dict(cls, data: dict):
        return cls(username=data["username"], email=data["email"])

    # స్టాటిక్ మెథడ్ (ఈమెయిల్ సరైనదేనా అని చూసే ఒక సాధారణ హెల్పర్ ఫంక్షన్)
    @staticmethod
    def is_valid_email(email: str) -> bool:
        return "@" in email and "." in email

# వాడే విధానం:
user_data = {"username": "ananya_ai", "email": "ananya@techin.ai"}

if User.is_valid_email(user_data["email"]):
    user1 = User.from_dict(user_data)  # క్లాస్ మెథడ్ ద్వారా ఆబ్జెక్ట్ సృష్టించాం
    user1.send_welcome_email()

print("మొత్తం నమోదైన యూజర్లు:", User.TOTAL_USERS)
```

---

## 5. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Pitfalls)

1. **`self` రాయడం మర్చిపోవడం:** మెథడ్స్ డిఫైన్ చేసేటప్పుడు `def deposit(amount):` అని రాస్తే `TypeError` వస్తుంది. తప్పకుండా `def deposit(self, amount):` అని రాయాలి.
2. **క్లాస్ వేరియబుల్‌ని ఆబ్జెక్ట్ ద్వారా మార్చడం:** `acc1.BANK_NAME = "New"` అంటే అది కేవలం `acc1` కి మాత్రమే మారుతుంది తప్ప మొత్తం క్లాస్‌కి మారదు.
3. **ప్రతిదానికీ క్లాసులు రాయడం:** కేవలం చిన్న ఫార్ములా కోసం క్లాసులు రాయనవసరం లేదు, సాధారణ ఫంక్షన్ సరిపోతుంది.

---

## 6. ప్రాక్టీస్ ల్యాబ్ (Daily Hands-On Lab)

### 🧪 టాస్క్: AI మోడల్ సర్వింగ్ ఎండ్‌పాయింట్ మేనేజర్ (Model Endpoint System)
**సన్నివేశం:** AI సిస్టమ్స్‌లో జెమిని, జీపీటీ లాంటి మోడల్స్‌కి యూజర్లు పంపే రిక్వెస్టులను ట్రాక్ చేయాలి. గరిష్ట లిమిట్ దాటితే రిక్వెస్ట్ ఆపాలి మరియు టోకెన్ ఖర్చు లెక్కించాలి.

```python
# ==========================================
# Day 6 Lab: AI మోడల్ సర్వర్ ఎండ్‌పాయింట్
# ==========================================

class ModelEndpoint:
    DEPLOYED_REGISTRY = []

    def __init__(self, model_name: str, cost_per_1k_tokens: float, max_concurrency: int = 5):
        self.model_name = model_name
        self.cost_per_1k_tokens = cost_per_1k_tokens
        self.max_concurrency = max_concurrency
        self._active_requests = 0
        self._total_tokens_served = 0
        ModelEndpoint.DEPLOYED_REGISTRY.append(self.model_name)

    @property
    def active_requests(self) -> int:
        return self._active_requests

    def process_inference(self, tokens_used: int) -> bool:
        """సర్వర్‌లో ట్రాఫిక్ లిమిట్ దాటకపోతే ప్రాసెస్ చేస్తుంది."""
        if self._active_requests >= self.max_concurrency:
            print(f"⚠️ [503 ఓవర్‌లోడ్] {self.model_name} వద్ద గరిష్ట రిక్వెస్ట్‌లు ({self.max_concurrency}) నడుస్తున్నాయి. వేచి ఉండండి!")
            return False

        # రిక్వెస్ట్ స్వీకరించబడింది
        self._active_requests += 1
        self._total_tokens_served += tokens_used
        print(f"⚡ [{self.model_name}] ప్రాసెసింగ్ జరుగుతోంది: {tokens_used} టోకెన్లు (ప్రస్తుతం యాక్టివ్: {self._active_requests})")
        
        # పూర్తయింది
        self._active_requests -= 1
        return True

    def calculate_billing_usd(self) -> float:
        return (self._total_tokens_served / 1000) * self.cost_per_1k_tokens

    @classmethod
    def get_deployed_catalog(cls) -> list:
        return cls.DEPLOYED_REGISTRY

# టెస్ట్ చేద్దాం:
gemini_endpoint = ModelEndpoint("gemini-1.5-flash", cost_per_1k_tokens=0.000375, max_concurrency=2)

gemini_endpoint.process_inference(1200)
gemini_endpoint.process_inference(4500)
print(f"{gemini_endpoint.model_name} మొత్తం బిల్లు: ${gemini_endpoint.calculate_billing_usd():.6f}")
print("అందుబాటులో ఉన్న మోడల్స్ లిస్ట్:", ModelEndpoint.get_deployed_catalog())
```

---

## 7. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: పైథాన్ క్లాసులలో `self` అంటే ఏమిటి?**
   - **సమాధానం:** `self` అనేది ప్రస్తుతం పనిచేస్తున్న నిర్దిష్ట ఆబ్జెక్ట్ యొక్క రిఫరెన్స్. ఇన్‌స్టాన్స్ మెథడ్‌ను కాల్ చేసినప్పుడు పైథాన్ ఆ ఆబ్జెక్ట్‌ను `self` ద్వారా స్వయంచాలకంగా పంపుతుంది. దాని ద్వారానే ఆబ్జెక్ట్ యొక్క అట్రిబ్యూట్స్ మరియు మెథడ్స్‌ను యాక్సెస్ చేయగలుగుతాం.
2. **ప్రశ్న: `@classmethod` మరియు `@staticmethod` మధ్య తేడా ఏమిటి?**
   - **సమాధానం:** `@classmethod` మొదటి పారామీటర్‌గా క్లాస్‌ని (`cls`) తీసుకుంటుంది మరియు క్లాస్-లెవల్ స్టేట్‌ను యాక్సెస్ చేయగలదు. `@staticmethod` కి `self` గానీ `cls` గానీ ఉండవు; అది క్లాస్ పరిధిలో ఉండే ఒక సాధారణ హెల్పర్ ఫంక్షన్ మాత్రమే.
3. **ప్రశ్న: పైథాన్‌లో ప్రైవేట్ వేరియబుల్స్ కోసం నేమ్ మాంగ్లింగ్ (Name Mangling) అంటే ఏమిటి?**
   - **సమాధానం:** వేరియబుల్ పేరు ముందు రెండు అండర్‌స్కోర్‌లు (`__variable`) పెట్టినప్పుడు, పైథాన్ అంతర్గతంగా దాని పేరును `_ClassName__variable` గా మారుస్తుంది. దీనివల్ల సబ్‌క్లాస్‌లలో పొరపాటున ఆ వేరియబుల్ ఓవర్‌రైట్ అవ్వకుండా రక్షణ కలుగుతుంది.
