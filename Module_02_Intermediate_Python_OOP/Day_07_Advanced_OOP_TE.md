# డే 07 (Day 07): అడ్వాన్స్‌డ్ OOP (Inheritance, Polymorphism & Abstraction)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను చాలా స్పష్టంగా అర్థం చేసుకుంటారు:
1. **ఇన్‌హెరిటెన్స్ (Inheritance):** ఒక పేరెంట్ క్లాస్ నుండి లక్షణాలను చైల్డ్ క్లాస్‌లోకి తెచ్చుకోవడం ("IS-A" సంబంధం).
2. **పాలిమార్ఫిజం (Polymorphism):** ఒకే రకమైన మెథడ్ పేరుతో వేర్వేరు ఆబ్జెక్టులు వేర్వేరు ఫలితాలు ఇవ్వడం.
3. **అబ్‌స్ట్రాక్షన్ & ఇంటర్‌ఫేస్ (Abstraction):** `abc` మాడ్యూల్ ఉపయోగించి రూల్స్ (Contracts) నిర్దేశించడం.
4. **కంపోజిషన్ vs ఇన్‌హెరిటెన్స్ (Composition):** "HAS-A" రిలేషన్‌షిప్ ద్వారా ఫ్లెక్సిబుల్ కోడ్ నిర్మించడం.
5. **మల్టిపుల్ ఇన్‌హెరిటెన్స్ & MRO (Method Resolution Order):** మరియు `super()` వాడే విధానం.

---

## 1. ఆధునిక AI వ్యవస్థల్లో అడ్వాన్స్‌డ్ OOP ఎందుకు అవసరం? (The "Why")

పెద్ద కంపెనీలలో లేదా LangChain, LlamaIndex లాంటి AI ఫ్రేమ్‌వర్కులలో ఒకే ఒక్క క్లాస్ రాయరు. ఒక స్టాండర్డ్ ఇంటర్‌ఫేస్ తయారు చేస్తారు:
- ఒక అబ్‌స్ట్రాక్ట్ `BaseLLM` క్లాస్ ఉంటుంది. అందులో `.generate(prompt)` అనే మెథడ్ కచ్చితంగా ఉండాలనే రూల్ ఉంటుంది.
- దాని కింద `OpenAILLM`, `GeminiLLM`, `AnthropicLLM` అనే చైల్డ్ క్లాసులు ఉంటాయి.
- రేపు మీ కంపెనీ OpenAI నుండి Google Gemini కి మారాలనుకుంటే, మొత్తం కోడ్ మార్చనవసరం లేదు. కేవలం **ఒకే ఒక్క లైన్ కాన్ఫిగరేషన్** మార్చితే సరిపోతుంది!

---

## 2. అబ్‌స్ట్రాక్షన్: `abc.ABC` మరియు `@abstractmethod`

**అబ్‌స్ట్రాక్ట్ క్లాస్ (Abstract Class)** ని నేరుగా ఆబ్జెక్ట్‌గా మార్చలేము. ఇది ఒక **రూల్ బుక్ (అగ్రిమెంట్)** లాంటిది. ఇందులో ఉన్న మెథడ్స్‌ని దీని కింద వచ్చే చైల్డ్ క్లాసులు తప్పనిసరిగా రాసి తీరాలి!

```python
from abc import ABC, abstractmethod

# ఇది ఒక కాంట్రాక్ట్ (రూల్ బుక్)
class NotificationService(ABC):
    @abstractmethod
    def send_alert(self, recipient: str, message: str) -> bool:
        """దీని కింద వచ్చే ప్రతి క్లాస్ తప్పకుండా ఈ మెథడ్‌ని ఇంప్లిమెంట్ చేయాలి."""
        pass

# ❌ డైరెక్ట్‌గా ఆబ్జెక్ట్ క్రియేట్ చేయలేము (TypeError వస్తుంది):
# service = NotificationService()

# 1వ ఇంప్లిమెంటేషన్: ఈమెయిల్ సర్వీస్
class EmailNotification(NotificationService):
    def send_alert(self, recipient: str, message: str) -> bool:
        print(f"📧 [ఈమెయిల్ పంపబడింది - {recipient}]: {message}")
        return True

# 2వ ఇంప్లిమెంటేషన్: స్లాక్ (Slack) మెసేజ్ సర్వీస్
class SlackNotification(NotificationService):
    def send_alert(self, recipient: str, message: str) -> bool:
        print(f"💬 [స్లాక్ ఛానల్ #{recipient} లో పోస్ట్ చేయబడింది]: {message}")
        return True
```

---

## 3. పాలిమార్ఫిజం (Polymorphism - ఒకే రూపం, బహుళ పనులు)

**పాలిమార్ఫిజం** అంటే ఒకే ఫంక్షన్ వేర్వేరు రకాల ఆబ్జెక్టులతో మాట్లాడగలగడం:

```python
def broadcast_security_breach(services: list[NotificationService], target: str, incident: str):
    """ఈ ఫంక్షన్‌కి పంపేది ఈమెయిలా లేక స్లాకా అనేది అనవసరం, రెండింటినీ ఒకేలా హ్యాండిల్ చేస్తుంది!"""
    for service in services:
        service.send_alert(target, f"🚨 సెక్యూరిటీ అలర్ట్: {incident}")

# టెస్ట్ చేద్దాం:
channels = [EmailNotification(), SlackNotification()]
broadcast_security_breach(channels, "devops-team", "సర్వర్ పోర్ట్ 8080 వద్ద అనుమానాస్పద లాగిన్ గుర్తించబడింది")
```

---

## 4. `super()` మరియు మెథడ్ ఓవర్‌రైడింగ్ (Method Overriding)

పేరెంట్ క్లాస్‌లో ఉన్న ఫంక్షన్‌కి అదనపు ఫీచర్లు జోడించడానికి చైల్డ్ క్లాస్‌లో `super()` ని ఉపయోగిస్తాం.

```python
class CloudResource:
    def __init__(self, resource_id: str, region: str):
        self.resource_id = resource_id
        self.region = region

    def get_info(self) -> str:
        return f"రిసోర్స్ ఐడీ: {self.resource_id} | లొకేషన్: {self.region}"

class VirtualMachine(CloudResource):
    def __init__(self, resource_id: str, region: str, cpu_cores: int, ram_gb: int):
        # super() ద్వారా పేరెంట్ క్లాస్ కన్‌స్ట్రక్టర్‌ని కాల్ చేస్తున్నాం
        super().__init__(resource_id, region)
        self.cpu_cores = cpu_cores
        self.ram_gb = ram_gb

    # మెథడ్ ఓవర్‌రైడింగ్: పేరెంట్ ఇన్ఫోకి మరిన్ని వివరాలు కలపడం
    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info} | కెపాసిటీ: {self.cpu_cores} vCPU, {self.ram_gb} GB RAM"

vm = VirtualMachine("vm-ai-train-01", "ap-south-1 (ముంబై)", cpu_cores=16, ram_gb=64)
print(vm.get_info())
```

---

## 5. కంపోజిషన్ vs ఇన్‌హెరిటెన్స్ (Composition - ఉత్తమ డిజైన్ ప్రిన్సిపల్)

సాఫ్ట్‌వేర్ ఆర్కిటెక్చర్‌లో ప్రముఖ గోల్డెన్ రూల్: **"Favor Composition over Inheritance"**.
- **ఇన్‌హెరిటెన్స్ ("IS-A" - కుక్క ఒక జంతువు):** పేరెంట్ క్లాస్‌లో ఏ చిన్న మార్పు చేసినా కింద ఉన్న అన్ని చైల్డ్ క్లాసులు పాడైపోతాయి (టైట్ కప్లింగ్).
- **కంపోజిషన్ ("HAS-A" - కారుకు ఇంజిన్ ఉంటుంది, కంప్యూటర్‌కు GPU ఉంటుంది):** భాగాలను విడివిడిగా చేసి అసెంబుల్ చేయడం. నచ్చినప్పుడు ఇంజిన్ మార్చుకోవచ్చు!

```python
# ==========================================
# కంపోజిషన్ ఉదాహరణ: ఆధునిక AI ఏజెంట్
# ==========================================

class VectorDatabase:
    def search(self, query: str):
        return f"[మెమొరీ నుండి సమాచారం: '{query}']"

class LLMBrain:
    def think(self, context: str):
        return f"ఈ సమాచారం ఆధారంగా AI ఆలోచించి రాసిన సమాధానం: {context}"

class AutonomousAgent:
    """ఏజెంట్‌కు మెమొరీ ఉంది (HAS-A) మరియు ఆలోచించే బ్రెయిన్ ఉంది (HAS-A)"""
    def __init__(self, memory: VectorDatabase, brain: LLMBrain):
        self.memory = memory  # కంపోజ్డ్ డిపెండెన్సీ
        self.brain = brain    # కంపోజ్డ్ డిపెండెన్సీ

    def execute_task(self, query: str):
        context = self.memory.search(query)
        response = self.brain.think(context)
        return response

# రేపు డేటాబేస్ మార్చాలన్నా, బ్రెయిన్ మార్చాలన్నా ఈ ఏజెంట్ క్లాస్‌ని ముట్టుకోవాల్సిన పనే లేదు!
agent = AutonomousAgent(VectorDatabase(), LLMBrain())
print(agent.execute_task("ట్రాన్స్‌ఫార్మర్ ఆర్కిటెక్చర్ వివరించండి"))
```

---

## 6. మల్టిపుల్ ఇన్‌హెరిటెన్స్ & MRO (Method Resolution Order)

పైథాన్‌లో ఒక క్లాస్ ఒకేసారి రెండు లేదా అంతకంటే ఎక్కువ పేరెంట్ క్లాసుల నుండి ఫీచర్లను తీసుకోవచ్చు. ఏ పేరెంట్ మెథడ్‌ని ముందు పిలవాలో పైథాన్ **MRO (C3 Linearization)** ప్రకారం నిర్ణయిస్తుంది.

```python
class LoggerMixin:
    def log(self, message):
        print(f"[లాగ్ రికార్డ్]: {message}")

class ValidatorMixin:
    def validate(self, data):
        print(f"[ధృవీకరణ]: డేటా స్కీమా సరిచూస్తున్నాం: {data}")

class DataIngestionPipeline(LoggerMixin, ValidatorMixin):
    def run(self, payload):
        self.validate(payload)
        self.log("డేటాను బిగ్‌క్వెరీ (BigQuery) లోకి లోడ్ చేస్తున్నాం...")

pipeline = DataIngestionPipeline()
pipeline.run({"record_count": 500})

# MRO ఆర్డర్ చూడటం
print("MRO ఆర్డర్:", [cls.__name__ for cls in DataIngestionPipeline.mro()])
```

---

## 7. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Pitfalls)

1. **ఇన్‌హెరిటెన్స్‌ని ఎక్కువగా వాడటం (Over-inheritance):** 5-6 లెవెల్స్ వరకూ పేరెంట్-చైల్డ్ రిలేషన్స్ రాస్తే కోడ్ అర్థం కాకుండా పోతుంది. గరిష్టంగా 1 లేదా 2 లెవెల్స్ మాత్రమే వాడండి.
2. **అబ్‌స్ట్రాక్ట్ మెథడ్‌ని చైల్డ్ క్లాస్‌లో రాయడం మర్చిపోవడం:** పేరెంట్‌లో `@abstractmethod` అని రాసి, చైల్డ్ క్లాస్‌లో దాన్ని రాయకపోతే వెంటనే ఎర్రర్ వస్తుంది.
3. **`super().__init__()` కాల్ చేయడం మర్చిపోవడం:** చైల్డ్ క్లాస్ క్రియేట్ చేసినప్పుడు పేరెంట్ క్లాస్ వేరియబుల్స్ సరిగ్గా సెట్ అవ్వవు.

---

## 8. ప్రాక్టీస్ ల్యాబ్ (Daily Hands-On Lab)

### 🧪 టాస్క్: మల్టీ-ప్రొవైడర్ AI గేట్‌వే (Enterprise AI Gateway)
**సన్నివేశం:** మీ కంపెనీకి ఒక కామన్ AI గేట్‌వే కావాలి. అందులో ఒక బేస్ క్లాస్ తయారు చేసి, గూగుల్ జెమిని మరియు ఓపెన్ఏఐ క్లయింట్లను పాలిమార్ఫిజం ద్వారా ఒకే విధంగా నడపాలి.

```python
# ==========================================
# Day 7 Lab: మల్టీ-ప్రొవైడర్ AI గేట్‌వే
# ==========================================
from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    def __init__(self, api_key: str, model_id: str):
        self.api_key = api_key
        self.model_id = model_id

    @abstractmethod
    def generate_completion(self, prompt: str) -> dict:
        """ప్రతి AI ప్రొవైడర్ తప్పకుండా సమాధానం మరియు టోకెన్ల వివరాలు ఇవ్వాలి."""
        pass

class GeminiProvider(BaseAIProvider):
    def generate_completion(self, prompt: str) -> dict:
        response_text = f"✨ [Google Gemini {self.model_id}]: ప్రాంప్ట్ విశ్లేషించబడింది: '{prompt[:30]}...'"
        return {
            "provider": "Google Vertex AI / Gemini",
            "model": self.model_id,
            "response": response_text,
            "tokens_consumed": len(prompt) // 3
        }

class OpenAIProvider(BaseAIProvider):
    def generate_completion(self, prompt: str) -> dict:
        response_text = f"🤖 [OpenAI {self.model_id}]: సమాధానం సిద్ధంగా ఉంది: '{prompt[:30]}...'"
        return {
            "provider": "OpenAI",
            "model": self.model_id,
            "response": response_text,
            "tokens_consumed": len(prompt) // 4
        }

class EnterpriseAIGateway:
    """పాలిమార్ఫిజం ఉపయోగించి ఏ ప్రొవైడర్ ఇచ్చినా ఒకేలా కాల్ చేస్తుంది."""
    def __init__(self, provider: BaseAIProvider):
        self.provider = provider

    def query(self, prompt: str):
        print(f"\n{self.provider.__class__.__name__} ద్వారా రిక్వెస్ట్ పంపుతున్నాం...")
        result = self.provider.generate_completion(prompt)
        print(f"సమాధానం: {result['response']}")
        print(f"టోకెన్లు : {result['tokens_consumed']}")

# ప్రొవైడర్లను సులభంగా మార్చడం చూద్దాం:
gemini_client = GeminiProvider(api_key="AIzaSyDummyKey", model_id="gemini-1.5-pro")
openai_client = OpenAIProvider(api_key="sk-proj-DummyKey", model_id="gpt-4o")

gateway = EnterpriseAIGateway(gemini_client)
gateway.query("ట్రాన్స్‌ఫార్మర్లలో అటెన్షన్ హెడ్స్ ఎలా పనిచేస్తాయి?")

# కోడ్ మార్చకుండా కేవలం ప్రొవైడర్‌ను మార్చడం:
gateway.provider = openai_client
gateway.query("ట్రాన్స్‌ఫార్మర్లలో అటెన్షన్ హెడ్స్ ఎలా పనిచేస్తాయి?")
```

---

## 9. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: పైథాన్‌లో `abc` మాడ్యూల్ యొక్క ముఖ్య ఉద్దేశం ఏమిటి?**
   - **సమాధానం:** `abc` (Abstract Base Class) మాడ్యూల్ అనేది ఇంటర్‌ఫేస్‌లను రూపొందించడానికి ఉపయోగపడుతుంది. ఒక మెథడ్‌పై `@abstractmethod` పెడితే, దాని చైల్డ్ క్లాసులు ఆ మెథడ్‌ను అమలు చేసేంత వరకు వాటి ఆబ్జెక్టులను క్రియేట్ చేయడానికి పైథాన్ అనుమతించదు.
2. **ప్రశ్న: ఇన్‌హెరిటెన్స్ కంటే కంపోజిషన్ ఎందుకు మంచిది?**
   - **సమాధానం:** ఇన్‌హెరిటెన్స్ అనేది పేరెంట్ మరియు చైల్డ్ మధ్య గట్టి సంబంధాన్ని ("IS-A") ఏర్పరుస్తుంది; పేరెంట్ మారితే చైల్డ్ బ్రేక్ అవుతుంది. అదే కంపోజిషన్ ("HAS-A") లో స్వతంత్ర విడిభాగాలను కలపడం వల్ల కోడ్‌ని సులభంగా టెస్ట్ చేయవచ్చు, విడదీయవచ్చు మరియు రన్‌టైమ్‌లో మార్చుకోవచ్చు.
3. **ప్రశ్న: పైథాన్ మల్టిపుల్ ఇన్‌హెరిటెన్స్‌లో మెథడ్స్‌ని ఏ ఆర్డర్‌లో వెతుకుతుంది?**
   - **సమాధానం:** పైథాన్ **C3 లీనియరైజేషన్ అల్గారిథమ్** ఉపయోగించి **MRO (Method Resolution Order)** ని నిర్మిస్తుంది. ఎడమ నుండి కుడికి, బాటమ్ నుండి టాప్‌కి ఏ మెథడ్ కూడా డూప్లికేట్ కాకుండా క్రమపద్ధతిలో వెతుకుతుంది.
