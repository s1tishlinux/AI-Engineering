# Day 39: AI డెవలపర్ల కోసం Microsoft Azure (Azure AI Foundry & OpenAI) 🔷

---

## 1. ఈ రోజు మన గోల్స్ (Day 39 Learning Objectives)
- మైక్రోసాఫ్ట్ ఎంటర్‌ప్రైజ్ AI ఎకోసిస్టమ్: **Azure AI Foundry** (గతంలో Azure AI Studio), **Azure OpenAI Service**, మరియు **Azure Machine Learning**.
- పబ్లిక్ ఇంటర్నెట్ కాకుండా, కార్పొరేట్ డేటా బయటకు వెళ్లకుండా ఉండే **Private Virtual Networks (VNets)** లో మోడల్స్ ని హోస్ట్ చేయడం.
- **Azure Functions (Python v2 Programming Model)** మరియు **Azure Blob Storage** తో సర్వర్‌లెస్ AI మైక్రోసర్వీసులు నిర్మించడం.
- కోడ్ లో API కీలు లేకుండానే సెక్యూరిటీని అందించే **Microsoft Entra ID (Azure AD)** మరియు `DefaultAzureCredential` ను ఉపయోగించడం.
- సెక్యూరిటీ & కంటెంట్ సేఫ్టీ: అసభ్యకరమైన కంటెంట్, కాపీరైట్ ఉల్లంఘనలు మరియు ప్రాంప్ట్ ఇంజెక్షన్ లను అడ్డుకునే **Azure Content Safety**.

---

## 2. రియల్ వరల్డ్ అనలాజీ (Real-World Analogy)

> 💡 **అనలాజీ: పబ్లిక్ ఇంటర్నెట్ కేఫ్ vs స్విస్ బ్యాంక్ లోని ప్రైవేట్ లాకర్**
>
> - **పబ్లిక్ OpenAI API (`api.openai.com`):**
>   ఇది పబ్లిక్ ఇంటర్నెట్ కేఫ్ లాంటిది. వేగంగా ఉంటుంది, క్రెడిట్ కార్డు పెట్టి ఎవరైనా వాడుకోవచ్చు. కానీ మీరు ఒక పెద్ద హాస్పిటల్ లో లేదా బ్యాంకులో పనిచేస్తుంటే, పేషెంట్ల సీక్రెట్ రిపోర్టులను లేదా బ్యాంక్ ఖాతా వివరాలను పబ్లిక్ కేఫ్ లో పెట్టి టైప్ చేయలేరు.. అది తీవ్రమైన నేరం!
> - **Azure OpenAI Service (స్విస్ బ్యాంక్ ప్రైవేట్ లాకర్):**
>   మైక్రోసాఫ్ట్ సంస్థ అదే OpenAI యొక్క GPT-4o మోడల్ ని తీసుకొచ్చి, మైక్రోసాఫ్ట్ యొక్క అత్యంత కట్టుదిట్టమైన **ప్రైవేట్ క్లౌడ్ లాకర్ (Azure)** లో పెట్టింది.
>   - మీ కంపెనీ డేటాను OpenAI తన పబ్లిక్ మోడల్ ట్రైనింగ్ కోసం **ఎట్టి పరిస్థితుల్లోనూ వాడదు**.
>   - ట్రాఫిక్ మొత్తం మీ కంపెనీ ప్రైవేట్ నెట్‌వర్క్ (VNet) లోపలే ఉంటుంది, పబ్లిక్ ఇంటర్నెట్ లోకి వెళ్ళదు.
>   - ఉద్యోగుల సింగిల్-సైన్-ఆన్ (Microsoft Entra ID) తో పూర్తి ఆడిట్ చేయబడుతుంది.
>   - HIPAA, GDPR, SOC2 లాంటి ప్రపంచ స్థాయి డేటా ప్రైవసీ సర్టిఫికేషన్లు ఉంటాయి.

---

## 3. Azure ఎంటర్‌ప్రైజ్ RAG ఆర్కిటెక్చర్

```
                    ┌──────────────────────────────┐
                    │    ఎంటర్‌ప్రైజ్ యూజర్ / యాప్ │
                    └──────────────┬───────────────┘
                                   │ HTTPS Request
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        AZURE VIRTUAL NETWORK (VNET)                    │
│                                                                        │
│   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
│   │      Azure API Mgmt       │─────►│    Azure Functions (v2)     │   │
│   │   (OAuth2 / Entra ID)     │      │   (సర్వర్‌లెస్ బ్యాకెండ్)   │   │
│   └───────────────────────────┘      └──────────────┬──────────────┘   │
│                                                     │                  │
│                                                     ▼                  │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                      AZURE AI FOUNDRY                          │   │
│   │                                                                │   │
│   │   ┌──────────────────────────┐    ┌────────────────────────┐   │   │
│   │   │     Azure AI Search      │    │  Azure OpenAI Service  │   │   │
│   │   │ (హైబ్రిడ్ వెక్టర్ సెర్చ్)│◄──►│  (GPT-4o డిప్లాయ్‌మెంట్) │   │   │
│   │   └──────────────────────────┘    └────────────────────────┘   │   │
│   │                 ▲                                              │   │
│   │                 │ Managed Identity (నో కీస్!)                  │   │
│   │   ┌─────────────┴────────────┐                                 │   │
│   │   │    Azure Blob Storage    │                                 │   │
│   │   │  (కంపెనీ పిడిఎఫ్ ఫైల్స్) │                                 │   │
│   │   └──────────────────────────┘                                 │   │
│   └────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. ముఖ్యమైన Azure AI సర్వీసులు

1. **Azure AI Foundry:**
   - OpenAI మోడల్స్, మోడల్ ఎవాల్యుయేషన్, ప్రాంప్ట్ ఫ్లో మరియు ఫైన్-ట్యూనింగ్ అన్నీ ఒకే చోట లభించే సమగ్ర ప్లాట్‌ఫారమ్.
2. **Azure OpenAI Service:**
   - ఎంటర్‌ప్రైజ్ సెక్యూరిటీతో రన్ అయ్యే GPT-4o, GPT-4o-mini మరియు టెక్స్ట్ ఎంబెడ్డింగ్ మోడల్స్.
3. **Azure AI Search:**
   - RAG అప్లికేషన్ల కోసం ప్రపంచంలోనే అత్యుత్తమ సెర్చ్ ఇంజిన్. ఇది వెక్టర్ సెర్చ్ మరియు కీవర్డ్ సెర్చ్ రెండింటినీ కలిపి (Hybrid Search) అద్భుతమైన ఫలితాలను ఇస్తుంది.
4. **Microsoft Entra ID & Managed Identity:**
   - పాస్‌వర్డ్‌లు లేదా API కీలు లేకుండా సర్వీసులు ఒకదానితో ఒకటి సురక్షితంగా మాట్లాడుకునే జీరో-ట్రస్ట్ ఆథెంటికేషన్.

---

## 5. కోడింగ్ వాక్‌త్రూ: Python లో Azure OpenAI & Managed Identity

కోడ్ లో ఎక్కడా API కీలు రాయకుండా `DefaultAzureCredential` ద్వారా Azure OpenAI ని అధికారిక SDK తో ఎలా కాల్ చేయాలో చూద్దాం:

```python
# azure_openai_demo.py
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def call_azure_gpt4():
    # 1. ఎన్విరాన్మెంట్ కాన్ఫిగరేషన్
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://telangana-enterprise-ai.openai.azure.com/")
    api_version = "2024-06-01"
    deployment_name = "gpt-4o-prod"  # Azure లో మీరు పెట్టిన డిప్లాయ్‌మెంట్ పేరు

    print(f"కనెక్ట్ అవుతున్నాము: {endpoint}")

    # 2. జీరో-ట్రస్ట్ ఆథెంటికేషన్ (API కీలు అవసరం లేదు!)
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default"
    )

    # 3. అధికారిక AzureOpenAI క్లయింట్
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version=api_version
    )

    print(f"🚀 Azure OpenAI డిప్లాయ్‌మెంట్ '{deployment_name}' కి రిక్వెస్ట్ వెళ్తోంది...")

    try:
        # 4. చాట్ కంప్లీషన్ కాల్
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "నువ్వు మైక్రోసాఫ్ట్ Azure ఎంటర్‌ప్రైజ్ AI అసిస్టెంట్‌వి. తెలుగులో సహాయం చెయ్యి."},
                {"role": "user", "content": "Azure OpenAI మరియు పబ్లిక్ OpenAI మధ్య ప్రధాన తేడా ఏమిటి?"}
            ],
            temperature=0.2,
            max_tokens=400
        )

        reply = response.choices[0].message.content
        print("\n--- 📩 Azure నుండి వచ్చిన సమాధానం ---")
        print(reply)

        print("\n--- 📊 టోకెన్ వినియోగం ---")
        print(f"మొత్తం ఖర్చయిన టోకెన్లు: {response.usage.total_tokens}")

        return reply

    except Exception as err:
        print(f"❌ Azure ఎర్రర్: {str(err)}")
        return None

if __name__ == "__main__":
    call_azure_gpt4()
```

---

## 6. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు & నివారణలు

| తప్పు | ఎందుకు జరుగుతుంది? | సరైన పద్ధతి |
| :--- | :--- | :--- |
| **Model Name కి బదులు Deployment Name ఇవ్వకపోవడం** | పబ్లిక్ OpenAI లో `model="gpt-4o"` అంటాం. కానీ Azure లో మీరు AI Studio లో మోడల్ కి ఏ పేరు పెట్టారో (ఉదా: `gpt-4o-prod`), ఆ డిప్లాయ్‌మెంట్ పేరునే ఇవ్వాలి, లేదంటే మోడల్ నాట్ ఫౌండ్ ఎర్రర్ వస్తుంది. | Azure Portal లో డిప్లాయ్‌మెంట్ పేరు చెక్ చేసి ఇవ్వాలి. |
| **కోడ్ లో API కీలను హార్డ్‌కోడ్ చేయడం** | `api_key = "d3b4f..."` అని రాస్తే గిట్‌హబ్ లేదా ఆడిటింగ్ లో సెక్యూరిటీ అలర్ట్ వస్తుంది. | ఎల్లప్పుడూ `DefaultAzureCredential()` మరియు Managed Identity వాడాలి. |
| **TPM (Tokens Per Minute) లిమిట్స్ పట్టించుకోకపోవడం** | Azure లో ప్రతి రీజియన్ కి నిమిషానికి నిర్దిష్ట టోకెన్ కోటా మాత్రమే ఉంటుంది. ట్రాఫిక్ పెరిగితే HTTP 429 Rate Limit వస్తుంది. | కోడ్ లో ఎక్స్‌పోనెన్షియల్ బ్యాక్-ఆఫ్ రీట్రై లాజిక్ రాయాలి లేదా PTU (Provisioned Throughput) తీసుకోవాలి. |

---

## 7. ప్రాక్టికల్ ల్యాబ్ (Hands-on Lab)

### లక్ష్యం:
Azure Functions (Python v2 Model) ఉపయోగించి, యూజర్ పంపిన టెక్స్ట్‌ని సమ్మరైజ్ చేసే ఒక సింపుల్ సర్వర్‌లెస్ API ఎండ్‌పాయింట్ ని రాయండి.

```python
# function_app.py
import azure.functions as func
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="summarize", methods=["POST"])
def summarize_text(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        input_text = body.get("text", "")
        
        if not input_text:
            return func.HttpResponse(
                json.dumps({"error": "దయచేసి 'text' పంపించండి"}),
                status_code=400,
                mimetype="application/json"
            )

        # AI సారాంశం (డెమో)
        summary = f"సారాంశం: {input_text[:80]}... (మొత్తం {len(input_text)} అక్షరాలు పరిశీలించబడ్డాయి)"
        
        return func.HttpResponse(
            json.dumps({"status": "SUCCESS", "result": summary}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
```

---

## 8. టాప్ 3 ఇంటర్వ్యూ ప్రశ్నలు & సమాధానాలు

### Q1: పబ్లిక్ OpenAI కి మరియు Azure OpenAI కి మధ్య ఎంటర్‌ప్రైజ్ తేడాలు ఏమిటి?
**సమాధానం:**
రెండు ఒకే రకమైన GPT-4o ఆర్కిటెక్చర్ ని వాడినప్పటికీ, Azure OpenAI లో:
1. **డేటా ప్రైవసీ:** కస్టమర్ డేటాను మైక్రోసాఫ్ట్ లేదా OpenAI తమ మోడల్స్ ని ట్రైన్ చేయడానికి వాడవు.
2. **ప్రైవేట్ నెట్‌వర్కింగ్:** పబ్లిక్ ఇంటర్నెట్ తో సంబంధం లేకుండా కేవలం కంపెనీ VNet లేదా ప్రైవేట్ ఎండ్‌పాయింట్స్ ద్వారా మాత్రమే కనెక్ట్ కావచ్చు.
3. **రెగ్యులేటరీ కంప్లయన్స్:** HIPAA, GDPR, SOC2 లాంటి కఠినమైన చట్టపరమైన అనుమతులు ఉంటాయి.

### Q2: Azure AI Search లో "Hybrid Search" అంటే ఏమిటి?
**సమాధానం:**
కేవలం వెక్టర్ సెర్చ్ (Vector Search) వాడితే భావం (Semantics) అర్థమవుతుంది కానీ, కొన్ని ప్రత్యేకమైన కోడ్ నంబర్లు (ఉదా: `PART-994-B`) లేదా కంపెనీ పేర్లను కరెక్ట్ గా పట్టుకోలేదు.
హైబ్రిడ్ సెర్చ్ లో **Dense Vector Search** (భావం కోసం) మరియు **Sparse Keyword Search - BM25** (ఖచ్చితమైన పదాల కోసం) రెండింటినీ కలిపి శోధించి, Reciprocal Rank Fusion (RRF) ద్వారా అత్యంత ఖచ్చితమైన సమాచారాన్ని అందిస్తుంది.

### Q3: పైథాన్ లో `DefaultAzureCredential` వల్ల ఉపయోగం ఏమిటి?
**సమాధానం:**
ఇది క్లౌడ్ లో జీరో-ట్రస్ట్ సెక్యూరిటీని సులభతరం చేస్తుంది. లోకల్ కంప్యూటర్ లో కోడింగ్ చేసేటప్పుడు డెవలపర్ యొక్క Azure CLI లాగిన్ ని వాడుకుంటుంది. అదే కోడ్ ని క్లౌడ్ లోని Azure Function లేదా VM లోకి డిప్లాయ్ చేసినప్పుడు, ఆటోమేటిక్ గా అక్కడి **Managed Identity** ని వాడుకుంటుంది. దీనివల్ల కోడ్ లో ఎక్కడా పాస్‌వర్డ్‌లు లేదా API కీలు రాయాల్సిన పనే ఉండదు.
