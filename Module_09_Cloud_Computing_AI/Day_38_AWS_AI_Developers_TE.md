# Day 38: AI డెవలపర్ల కోసం AWS క్లౌడ్ (Amazon Bedrock & SageMaker) 🟧

---

## 1. ఈ రోజు మన గోల్స్ (Day 38 Learning Objectives)
- AWS లోని జనరేటివ్ AI ఎకోసిస్టమ్: **Amazon Bedrock** (సర్వర్‌లెస్ ఫౌండేషన్ మోడల్స్) మరియు **Amazon SageMaker** (కస్టమ్ మోడల్ ట్రైనింగ్ & హోస్టింగ్) మధ్య తేడాను అర్థం చేసుకోవడం.
- సర్వర్‌లెస్ AI ఆర్కిటెక్చర్ నిర్మించడం: **API Gateway -> AWS Lambda -> Amazon Bedrock -> Amazon S3**.
- అధికారిక AWS పైథాన్ SDK అయిన **`boto3`** ఉపయోగించి Bedrock **Converse API** ద్వారా కోడ్ రాయడం.
- డేటా భద్రత కోసం **Bedrock Guardrails**: యూజర్ల ఫోన్ నంబర్లు, క్రెడిట్ కార్డులను (PII Redaction) మాస్క్ చేయడం మరియు హానికరమైన కంటెంట్‌ను నిరోధించడం.
- రెస్పాన్స్ లు లైవ్ లో టైప్ అవుతున్నట్లు రావడానికి **Streaming Responses (`converse_stream`)** ఇంప్లిమెంట్ చేయడం.

---

## 2. రియల్ వరల్డ్ అనలాజీ (Real-World Analogy)

> 💡 **అనలాజీ: కస్టమ్ ఫ్యాక్టరీ మెషిన్ vs ఇంట్లోని కరెంట్ స్విచ్ బోర్డు**
>
> - **Amazon SageMaker (సొంతంగా ఫ్యాక్టరీ మెషిన్ తయారుచేయడం):**
>   మీరు ప్రత్యేకమైన బట్టలు నేయడానికి ఒక పెద్ద మగ్గాన్ని డిజైన్ చేసి, మోటార్లు బిగించి, గ్రీజు పెట్టి నిరంతరం నడిపించడం లాంటిది. SageMaker లో మీరే GPU సర్వర్ సైజు ఎంచుకోవాలి (`ml.g5.2xlarge`), డాకర్ కంటైనర్లు రాయాలి, మెమొరీని మేనేజ్ చేయాలి. పూర్తి కంట్రోల్ ఉంటుంది కానీ చాలా ఇంజనీరింగ్ వర్క్ అవసరం.
> - **Amazon Bedrock (గోడకున్న కరెంట్ స్విచ్ బోర్డు):**
>   మీకు గదిలో ఫ్యాన్, లైట్ వేసుకోవడానికి పవర్ స్టేషన్ నిర్మించాల్సిన అవసరం లేదు. కేవలం గోడకున్న ప్లగ్ లో పిన్ పెట్టి స్విచ్ ఆన్ చేస్తే కరెంట్ వస్తుంది.
>   Bedrock లో కూడా ప్రపంచ ప్రసిద్ధ మోడల్స్ (Claude 3.5 Sonnet, Meta Llama 3, Amazon Titan, Mistral) అన్నీ ముందే సిద్ధంగా ఉంటాయి. ఒక్క సర్వర్ కూడా ఆన్ చేయకుండా, కేవలం పైథాన్ లో `boto3` లైబ్రరీతో ఒక్క API కాల్ కొడితే చాలు.. ఫలితం వచ్చేస్తుంది! 100% సర్వర్‌లెస్!

---

## 3. AWS సర్వర్‌లెస్ AI ఆర్కిటెక్చర్

```
                    ┌──────────────────────────────┐
                    │    మొబైల్ యాప్ / వెబ్‌సైట్   │
                    └──────────────┬───────────────┘
                                   │ HTTPS POST /chat
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        AWS క్లౌడ్ ఇన్ఫ్రాస్ట్రక్చర్                   │
│                                                                        │
│   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
│   │    Amazon API Gateway     │─────►│     AWS Lambda ఫంక్షన్      │   │
│   │ (ట్రాఫిక్ కంట్రోల్ & Auth)│      │  (Python 3.11 + Boto3 SDK)  │   │
│   └───────────────────────────┘      └──────────────┬──────────────┘   │
│                                                     │                  │
│                                                     ▼                  │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                       AMAZON BEDROCK                           │   │
│   │                                                                │   │
│   │   ┌──────────────────────────┐    ┌────────────────────────┐   │   │
│   │   │    Bedrock Guardrails    │    │    ఫౌండేషన్ మోడల్      │   │   │
│   │   │ (వ్యక్తిగత డేటా భద్రత)   │───►│ (Claude 3.5 / Llama 3) │   │   │
│   │   └──────────────────────────┘    └────────────────────────┘   │   │
│   └─────────────────────────────────────────────────┬──────────────┘   │
│                                                     │                  │
│                                                     ▼                  │
│                                      ┌─────────────────────────────┐   │
│                                      │          Amazon S3          │   │
│                                      │ (చాట్ లాగ్స్ & ఆడిట్ డేటా) │   │
│                                      └─────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. ముఖ్యమైన AWS AI సర్వీసులు

1. **Amazon Bedrock:**
   - సర్వర్లు లేకుండానే ప్రముఖ AI మోడల్స్ ని ఉపయోగించుకునే సర్వీస్.
   - దీనిలోనే RAG కోసం **Knowledge Bases** మరియు ఏజెంట్ల కోసం **Agents for Bedrock** ఉంటాయి.
2. **Amazon SageMaker:**
   - మొదటి నుండి సొంతంగా డీప్ లెర్నింగ్ మోడల్స్ ట్రైన్ చేయడానికి, భారీ ఓపెన్-సోర్స్ మోడల్స్ ని ఫైన్-ట్యూన్ చేయడానికి వాడే ప్లాట్‌ఫారమ్.
3. **AWS Lambda:**
   - సర్వర్ల నిర్వహణ అవసరం లేకుండా ఈవెంట్ ఆధారంగా పైథాన్ కోడ్ ని రన్ చేసే సర్వర్‌లెస్ కంప్యూట్.
4. **Amazon S3:**
   - డేటాసెట్లు, మోడల్ వెయిట్స్, ప్రాంప్ట్ టెంప్లేట్లను భద్రపరిచే క్లౌడ్ స్టోరేజ్.

---

## 5. కోడింగ్ వాక్‌త్రూ: Python & Boto3 తో Amazon Bedrock ని కాల్ చేయడం

ప్రస్తుతం Bedrock లో మోడల్స్ ని కాల్ చేయడానికి ప్రామాణికమైన మార్గం **Converse API**. ఇది Claude, Llama, Titan వంటి అన్ని మోడల్స్ కీ ఒకే యూనిఫైడ్ ఫార్మాట్ ని అందిస్తుంది:

```python
# bedrock_demo.py
import json
import boto3
from botocore.exceptions import ClientError

def ask_bedrock(prompt_question: str):
    # 1. Bedrock Runtime క్లయింట్ ప్రారంభం
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )

    # 2. యూజర్ మెసేజ్ ఫార్మాట్
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt_question}]
        }
    ]

    # 3. ఇన్ఫరెన్స్ కాన్ఫిగరేషన్
    inference_config = {
        "maxTokens": 400,
        "temperature": 0.2
    }

    system_instructions = [
        {"text": "నువ్వు ఒక ప్రొఫెషనల్ AI అసిస్టెంట్‌వి. తెలుగులోనే చాలా స్పష్టంగా, మర్యాదగా సమాధానం ఇవ్వు."}
    ]

    # Claude 3.5 Sonnet మోడల్ ఐడీ
    target_model = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    print(f"🚀 Amazon Bedrock కి రిక్వెస్ట్ వెళ్తోంది [Model: {target_model}]...")

    try:
        # 4. Converse API ని కాల్ చేయడం
        response = bedrock.converse(
            modelId=target_model,
            messages=messages,
            system=system_instructions,
            inferenceConfig=inference_config
        )

        # 5. అవుట్‌పుట్ మరియు టోకెన్ వివరాలు వెలికితీయడం
        message_output = response["output"]["message"]
        reply_text = message_output["content"][0]["text"]
        token_usage = response["usage"]

        print("\n--- 📩 Bedrock నుండి వచ్చిన సమాధానం ---")
        print(reply_text)

        print("\n--- 📊 టోకెన్ వివరాలు ---")
        print(f"ఇన్‌పుట్ టోకెన్లు : {token_usage['inputTokens']}")
        print(f"అవుట్‌పుట్ టోకెన్లు: {token_usage['outputTokens']}")
        print(f"మొత్తం టోకెన్లు  : {token_usage['totalTokens']}")

        return reply_text

    except ClientError as err:
        print(f"❌ AWS ఎర్రర్: {err.response['Error']['Message']}")
        return None

# AWS Lambda ఫంక్షన్ హ్యాండ్లర్
def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        user_text = body.get("message", "క్లౌడ్ కంప్యూటింగ్ వల్ల లాభాలు ఏమిటి?")
        
        ai_reply = ask_bedrock(user_text)
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "SUCCESS", "reply": ai_reply})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "ERROR", "error": str(e)})
        }

if __name__ == "__main__":
    ask_bedrock("Amazon Bedrock ను డెవలపర్లు ఎందుకు ఇష్టపడతారు?")
```

---

## 6. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు & పరిష్కారాలు

| తప్పు | ఎందుకు జరుగుతుంది? | సరైన మార్గం |
| :--- | :--- | :--- |
| **AWS కన్సోల్ లో మోడల్ యాక్సెస్ ఎనేబుల్ చేయకపోవడం** | Bedrock లో Claude 3.5 లేదా Llama 3 డీఫాల్ట్ గా ఆన్ లో ఉండవు. రిక్వెస్ట్ పంపితే వెంటనే `AccessDeniedException` వస్తుంది. | AWS Console -> Bedrock -> "Model access" లోకి వెళ్లి కావాల్సిన మోడల్స్ ని టిక్ చేసి "Request model access" క్లిక్ చేయాలి. |
| **AWS Lambda Timeout (డీఫాల్ట్ 3 సెకన్లు)** | LLM సమాధానం ఇవ్వడానికి 5 నుండి 10 సెకన్లు పడుతుంది. లాంబ్డా డీఫాల్ట్ గా 3 సెకన్లలో ఆగిపోయి ఎర్రర్ ఇస్తుంది. | Lambda Configuration లో టైమౌట్ ను కనీసం 30 లేదా 60 సెకన్లకు పెంచాలి. |
| **పాత `invoke_model` మెథడ్ వాడటం** | పాత విధానంలో ఒక్కో మోడల్ కి ఒక్కో రకమైన JSON రాయాల్సి వచ్చేది. | కొత్త ప్రామాణికమైన `bedrock.converse()` మెథడ్ మాత్రమే వాడాలి. |

---

## 7. ప్రాక్టికల్ ల్యాబ్ (Hands-on Lab)

### లక్ష్యం:
Bedrock నుండి సమాధానం వచ్చేటప్పుడు ఒక్కో పదం స్క్రీన్ పై టైప్ అవుతున్నట్లు కనిపించేలా **Streaming API (`converse_stream`)** ని రన్ చేయండి.

```python
# lab_day38_stream.py
import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

messages = [{"role": "user", "content": [{"text": "క్లౌడ్ మరియు AI గురించి 2 మంచి సూక్తులు చెప్పు."}]}]

response = client.converse_stream(
    modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
    messages=messages
)

print("లైవ్ స్ట్రీమింగ్ సమాధానం:\n")
for event in response.get("stream", []):
    if "contentBlockDelta" in event:
        chunk = event["contentBlockDelta"]["delta"].get("text", "")
        print(chunk, end="", flush=True)
print("\n\nస్ట్రీమింగ్ పూర్తయింది.")
```

---

## 8. టాప్ 3 ఇంటర్వ్యూ ప్రశ్నలు & సమాధానాలు

### Q1: Amazon Bedrock కి మరియు Amazon SageMaker కి తేడా ఏమిటి?
**సమాధానం:**
- **Amazon Bedrock:** సర్వర్‌లెస్ జనరేటివ్ AI సర్వీస్. ఇందులో క్లౌడ్ లో ముందే సిద్ధంగా ఉన్న అగ్రశ్రేణి మోడల్స్ ని (Claude, Llama) ఎలాంటి సర్వర్లు మెయింటైన్ చేయకుండా కేవలం API ద్వారా టోకెన్ ఖర్చుతో వాడుకోవచ్చు.
- **Amazon SageMaker:** సంపూర్ణ మెషిన్ లెర్నింగ్ ప్లాట్‌ఫారమ్. ఇందులో GPU సర్వర్లను మనమే ఎంచుకుని, మొదటి నుండి మోడల్స్ ని ట్రైన్ చేయడం, ఫైన్-ట్యూన్ చేయడం మరియు డెడికేటెడ్ కంటైనర్లను హోస్ట్ చేయడం జరుగుతుంది.

### Q2: Bedrock లో Converse API ఎందుకు అంత ముఖ్యమైనది?
**సమాధానం:**
గతంలో Bedrock లో ఆంత్రోపిక్ క్లాడ్ కి వేరే JSON, మెటా లామా కి వేరే రకమైన JSON ఫార్మాట్ రాయాల్సి వచ్చేది. కానీ **Converse API** ఒకే కామన్ మెసేజ్ స్కీమాను తీసుకొచ్చింది. దీనివల్ల రేపు మోడల్ ని Claude నుండి Llama కి మార్చినా అప్లికేషన్ పైథాన్ కోడ్ లో ఒక్క లైన్ కూడా మార్చాల్సిన అవసరం ఉండదు.

### Q3: Bedrock Guardrails అంటే ఏమిటి?
**సమాధానం:**
యూజర్ అడిగే ప్రశ్నలు మరియు మోడల్ ఇచ్చే సమాధానాలను స్కాన్ చేసి సెక్యూరిటీని కాపాడే రక్షణ కవచం. ఇందులో 3 ప్రధాన పనులు జరుగుతాయి:
1. **PII Masking:** కస్టమర్ల ఆధార్, ఫోన్ నంబర్లు, బ్యాంక్ కార్డు నంబర్లను మోడల్ చూడకుండా మాస్క్ చేస్తుంది.
2. **Toxic Content Block:** అసభ్యకరమైన పదాలను, వివక్షను అడ్డుకుంటుంది.
3. **Contextual Grounding:** RAG డాక్యుమెంట్లలో లేని కల్పిత అబద్ధాలను (Hallucinations) గుర్తించి బ్లాక్ చేస్తుంది.
