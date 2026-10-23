# డే 23 (Day 23): పైథాన్‌తో LLM ఇంటిగ్రేషన్ (Gemini & OpenAI SDKs)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను చాలా స్పష్టంగా అర్థం చేసుకుంటారు:
1. అధికారిక **Google Gemini SDK** మరియు **OpenAI SDK** సెటప్ మరియు అథెంటికేషన్.
2. సిస్టమ్ ఇన్‌స్ట్రక్షన్స్, టెంపరేచర్ మరియు టోకెన్ బడ్జెట్‌తో ప్రాంప్ట్ పంపడం.
3. లైవ్ స్ట్రీమింగ్ రెస్పాన్స్ (**Streaming Outputs - `stream=True`**) తయారు చేయడం.
4. గత సంభాషణలను గుర్తుంచుకునే **మల్టీ-టర్న్ చాట్ సెషన్లు** నిర్మించడం.
5. టోకెన్ ఖర్చులను లెక్కించడం మరియు రేట్ లిమిట్స్ హ్యాండిల్ చేయడం.

---

## 1. మన సొంత AI అప్లికేషన్లు ఎందుకు నిర్మించాలి? (The "Why")

ChatGPT లేదా Gemini వెబ్‌సైట్లు సాధారణ ప్రజల కోసం తయారు చేసినవి.
కానీ ఒక సాఫ్ట్‌వేర్ ఇంజనీర్‌గా మనం ఆఫీసులలో **ఆటోమేటెడ్ బ్యాకెండ్ AI సిస్టమ్స్** నిర్మిస్తాం:
- కస్టమర్ కేర్ కాల్ ముగియగానే పూర్తి సంభాషణను ఆటోమేటిక్‌గా సమ్మరైజ్ చేసి డేటాబేస్‌లో పెట్టడం.
- జాబ్ పోర్టల్‌కి వచ్చిన వేలాది రెజ్యూమెలను చదివి సరైన అభ్యర్థులను ఫిల్టర్ చేయడం.
- కంపెనీ కోడ్‌ను ఆటోమేటిక్‌గా రివ్యూ చేసి బగ్స్ కనిపెట్టే బాట్ తయారు చేయడం.

వీటన్నింటి కోసం మనం అధికారిక **Python SDKs** ను ఉపయోగిస్తాం.

---

## 2. API కీలు మరియు ఎన్విరాన్‌మెంట్ సెటప్

⚠️ **గోల్డెన్ రూల్:** API కీని ఎప్పుడూ కోడ్ ఫైల్ లోపల డైరెక్ట్‌గా రాయకూడదు! ఎన్విరాన్‌మెంట్ వేరియబుల్స్ ద్వారా మాత్రమే లోడ్ చేయాలి:

```bash
# టెర్మినల్ లో సెట్ చేయడం:
export GEMINI_API_KEY="మీ_ఒరిజినల్_API_కీ_ఇక్కడ_ఇవ్వండి"

# కావాల్సిన లైబ్రరీలు వేసుకోవడం:
pip install google-genai openai python-dotenv
```

---

## 3. గూగుల్ జెమిని (Google Gemini) పైథాన్ SDK వాడే విధానం

గూగుల్ వారి Gemini 1.5 మోడల్స్ 10 లక్షల నుండి 20 లక్షల టోకెన్ల సామర్థ్యంతో పరిశ్రమలోనే అత్యుత్తమ స్థానంలో ఉన్నాయి.

```python
import os
from google import genai
from google.genai import types

# 1. క్లయింట్ ప్రారంభం (ఎన్విరాన్‌మెంట్ నుండి GEMINI_API_KEY ని ఆటోమేటిక్‌గా తీసుకుంటుంది)
client = genai.Client()

# 2. సిస్టమ్ ప్రాంప్ట్ & సెట్టింగ్స్ కాన్ఫిగర్ చేయడం
config = types.GenerateContentConfig(
    system_instruction="నువ్వు ఒక చీఫ్ సాఫ్ట్‌వేర్ ఆర్కిటెక్ట్‌వి. స్పష్టంగా, సూటిగా సమాధానం ఇవ్వు.",
    temperature=0.2,
    max_output_tokens=500
)

# 3. ప్రశ్న పంపడం (Single-Turn Generation)
response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="డేటాబేస్ డిజైన్‌లో కనెక్షన్ పూలింగ్ (Connection Pooling) ఎందుకు అంత ముఖ్యం?",
    config=config
)

print("--- జెమిని సమాధానం ---")
print(response.text)

# ఎన్ని టోకెన్లు ఖర్చయ్యాయో చూడటం:
if response.usage_metadata:
    print(f"\nప్రశ్నకు పట్టిన టోకెన్లు : {response.usage_metadata.prompt_token_count}")
    print(f"సమాధానానికి పట్టినవి    : {response.usage_metadata.candidates_token_count}")
    print(f"మొత్తం టోకెన్లు         : {response.usage_metadata.total_token_count}")
```

---

## 4. లైవ్ స్ట్రీమింగ్ (Streaming Responses - UI వేగం పెంచడం)

ఒక పెద్ద సమాధానం రాయడానికి AI కి 5 సెకన్లు పడుతుందనుకుందాం. 5 సెకన్ల పాటు స్క్రీన్ పై ఏమీ కనబడకుండా యూజర్‌ని వెయిట్ చేయిస్తే యాప్ స్లోగా ఉందని ఫీల్ అవుతారు.
**స్ట్రీమింగ్ వాడితే, అక్షరం తయారైన వెంటనే లైవ్‌గా టైప్ అవుతున్నట్లు స్క్రీన్ పై కనిపిస్తుంది:**

```python
import asyncio
from google import genai

client = genai.Client()

async def stream_ai_response(prompt: str):
    print("AI: ", end="", flush=True)
    
    # generate_content_stream ద్వారా ఒక్కో ముక్క వెంటనే వస్తుంది
    response_stream = client.models.generate_content_stream(
        model="gemini-1.5-flash",
        contents=prompt
    )

    for chunk in response_stream:
        print(chunk.text, end="", flush=True)
    print("\n")

stream_ai_response("మైక్రోసర్వీసెస్ వల్ల కలిగే ముఖ్యమైన 3 లాభాలను బుల్లెట్ పాయింట్లలో రాయి.")
```

---

## 5. మల్టీ-టర్న్ చాట్ సెషన్లు (జ్ఞాపకశక్తిని నిలపడం)

LLM లు సహజంగా గత సంభాషణలను గుర్తుంచుకోలేవు (Stateless). చాట్ జరగాలంటే క్లయింట్ అప్లికేషనే పాత హిస్టరీ మొత్తాన్ని మోడల్‌కి పంపాలి:

```python
from google import genai

client = genai.Client()

# చాట్ సెషన్ ప్రారంభం (ఇది హిస్టరీని ఆటోమేటిక్‌గా దాచుకుంటుంది)
chat = client.chats.create(model="gemini-1.5-flash")

# 1వ మెసేజ్
resp1 = chat.send_message("హలో, నా పేరు అరవింద్. నేను ఒక AI ట్రావెల్ ప్లానర్ యాప్ తయారు చేస్తున్నాను.")
print("అసిస్టెంట్:", resp1.text)

# 2వ మెసేజ్ (మోడల్ అరవింద్ పేరును గుర్తుపెట్టుకుంటుంది!)
resp2 = chat.send_message("నా పేరు ఏమిటి? నేను ఏ ప్రాజెక్ట్ చేస్తున్నాను?")
print("అసిస్టెంట్:", resp2.text)

# హిస్టరీలో ఎన్ని మెసేజ్‌లు ఉన్నాయో చూడటం:
print(f"\nమొత్తం సంభాషణల సంఖ్య: {len(chat.get_history())}")
```

---

## 6. టోకెన్ ట్రాకింగ్ & ఖర్చుల లెక్కింపు (Cost Tracking)

కంపెనీలలో AI API బిల్లులు లక్షల్లో రాకుండా ప్రతి రిక్వెస్ట్‌కి ఎంత ఖర్చవుతుందో ట్రాక్ చేయాలి:

```python
class TokenCostTracker:
    # 10 లక్షల టోకెన్ల రేట్లు (డాలర్లలో)
    PRICE_INPUT_PER_1M_USD = 0.075
    PRICE_OUTPUT_PER_1M_USD = 0.300
    USD_TO_INR = 83.5

    @classmethod
    def calculate_cost(cls, prompt_tokens: int, completion_tokens: int) -> dict:
        cost_input = (prompt_tokens / 1_000_000) * cls.PRICE_INPUT_PER_1M_USD
        cost_output = (completion_tokens / 1_000_000) * cls.PRICE_OUTPUT_PER_1M_USD
        total_usd = cost_input + cost_output
        total_inr = total_usd * cls.USD_TO_INR

        return {
            "మొత్తం టోకెన్లు": prompt_tokens + completion_tokens,
            "ఖర్చు డాలర్లలో": f"${total_usd:.6f}",
            "ఖర్చు రూపాయల్లో": f"₹{total_inr:.4f}"
        }

metrics = TokenCostTracker.calculate_cost(prompt_tokens=1500, completion_tokens=450)
print("ఈ ప్రశ్నకి అయిన ఖర్చు వివరాలు:", metrics)
```

---

## 7. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Pitfalls)

1. **API కీలను కోడ్‌లో రాసి GitHub లోకి పుష్ చేయడం:**
   - కీ దొంగిలించబడితే మీ క్రెడిట్ కార్డు ఖాళీ అయిపోతుంది. ఎల్లప్పుడూ `.env` లోనే ఉంచాలి.
2. **అనంతంగా చాట్ హిస్టరీని పెంచుకుంటూ పోవడం:**
   - 100 ప్రశ్నల తర్వాత ప్రాంప్ట్ సైజు 50,000 టోకెన్లకు చేరి, ఒక్కో ప్రశ్నకు ఎక్కువ డబ్బులు మరియు ఎక్కువ సమయం పడుతుంది. చివరి 5 నుండి 10 సంభాషణలను మాత్రమే ఉంచేలా విండో స్లైసింగ్ చేయాలి.
3. **రేట్ లిమిట్స్ ఎర్రర్ వచ్చినప్పుడు రీ-ట్రై చేయకపోవడం:**
   - ఏకకాలంలో చాలా రిక్వెస్ట్‌లు పంపినప్పుడు సర్వర్ `429` ఇస్తుంది. దాన్ని క్యాచ్ చేసి కొన్ని సెకన్లు ఆగి మళ్లీ ప్రయత్నించేలా కోడ్ రాయాలి.

---

## 8. ప్రాక్టీస్ ల్యాబ్ (Daily Hands-On Lab)

### 🧪 టాస్క్: టెర్మినల్ AI కోపైలట్ (CLI Assistant with Streaming)
**సన్నివేశం:** మీ ల్యాప్‌టాప్ టెర్మినల్ నుండే కోడింగ్ డౌట్లు అడగడానికి ఒక లైవ్ స్ట్రీమింగ్ AI అసిస్టెంట్‌ను తయారు చేయండి.

```python
# =========================================================
# Day 23 Lab: టెర్మినల్ AI కోపైలట్
# =========================================================
import os
import time
from google import genai
from google.genai import types

def start_terminal_copilot():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ దయచేసి GEMINI_API_KEY ఎన్విరాన్‌మెంట్ వేరియబుల్‌ని సెట్ చేయండి!")
        return

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model="gemini-1.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="నువ్వు ఒక తెలివైన పైథాన్ కోడింగ్ అసిస్టెంట్‌వి. సూటిగా మరియు వేగంగా కోడ్ రాయ్.",
            temperature=0.3
        )
    )

    print("="*55)
    print("🤖 టీచిన్ టెర్మినల్ AI కోపైలట్ (బయటకు వెళ్లడానికి 'exit' అని టైప్ చేయండి)")
    print("="*55)

    while True:
        try:
            user_input = input("\nమీరు > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("కోపైలట్ ముగిసింది. ఆల్ ది బెస్ట్!")
                break

            print("\nAI > ", end="", flush=True)
            
            # లైవ్ స్ట్రీమింగ్
            response_stream = chat.send_message_stream(user_input)
            for chunk in response_stream:
                print(chunk.text, end="", flush=True)
            print()

        except KeyboardInterrupt:
            print("\nయూజర్ సెషన్‌ను ఆపేశారు.")
            break
        except Exception as e:
            print(f"\n⚠️ సర్వర్ లోపం: {e}. 2 సెకన్లలో మళ్లీ ప్రయత్నిస్తున్నాం...")
            time.sleep(2)

if __name__ == "__main__":
    start_terminal_copilot()
```

---

## 9. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: LLM లు స్టేట్‌లెస్ (Stateless) అంటారు కదా, మరి చాట్‌బాట్ పాత విషయాలను ఎలా గుర్తుంచుకుంటుంది?**
   - **సమాధానం:** అవును, LLM లకు గత సంభాషణల మెమొరీ ఉండదు. ప్రతి కొత్త ప్రశ్న అడిగినప్పుడు, క్లయింట్ అప్లికేషన్ గతంలో జరిగిన సంభాషణల చరిత్ర మొత్తాన్ని ఒక లిస్ట్‌గా కలిపి కొత్త ప్రాంప్ట్‌తో పాటు సర్వర్‌కి పంపుతుంది. ఆ హిస్టరీ మొత్తాన్ని చదివి మోడల్ సమాధానం ఇస్తుంది.
2. **ప్రశ్న: HTTP స్ట్రీమింగ్ (Server-Sent Events) ఎలా పనిచేస్తుంది?**
   - **సమాధానం:** మోడల్ మొత్తం 500 పదాలు రాసేంతవరకు వేచి చూడకుండా, GPU లో ఒక్కో పదం (టోకెన్) తయారైన వెంటనే HTTP కనెక్షన్ ద్వారా క్లయింట్ బ్రౌజర్‌కి పంపిస్తూ ఉంటుంది. దీనివల్ల యూజర్‌కి సమాధానం వెంటనే టైప్ అవుతున్నట్లు కనిపిస్తుంది (Latency ఫీల్ అవ్వదు).
3. **ప్రశ్న: ఇన్‌పుట్ టోకెన్ల కంటే అవుట్‌పుట్ టోకెన్లకు ప్రొవైడర్లు ఎక్కువ డబ్బులు ఎందుకు వసూలు చేస్తారు?**
   - **సమాధానం:** ఇన్‌పుట్ టోకెన్లను మోడల్ ఒకేసారి సమాంతరంగా (Parallel) చదవగలదు, దీనికి తక్కువ సమయం పడుతుంది. కానీ అవుట్‌పుట్ టోకెన్లను ఒక్కొక్కటిగా మాత్రమే సీక్వెన్షియల్‌గా ఉత్పత్తి చేయాలి (Autoregressive); దీనివల్ల GPU మెమొరీ బ్యాండ్‌విడ్త్ ఎక్కువ సమయం ఆక్యుపై అవుతుంది కాబట్టి అవుట్‌పుట్ టోకెన్లకు 3 నుండి 5 రెట్లు ఎక్కువ ఛార్జ్ చేస్తారు.
