# Day 37: AI డెవలపర్ల కోసం క్లౌడ్ కంప్యూటింగ్ బేసిక్స్ & మల్టీ-క్లౌడ్ వ్యూహం ☁️

---

## 1. ఈ రోజు మన గోల్స్ (Day 37 Learning Objectives)
- క్లౌడ్ లోని 3 ప్రధాన సర్వీస్ మోడల్స్: **IaaS (Infrastructure as a Service)**, **PaaS (Platform as a Service)**, మరియు **SaaS (Software as a Service)**.
- AI డెవలపర్ కి తప్పనిసరిగా తెలియాల్సిన క్లౌడ్ కాంపోనెంట్స్: **IAM (సెక్యూరిటీ/రోల్స్)**, **Object Storage (S3/GCS/Blob)**, **Compute (CPUs vs GPUs)**, మరియు **Containers**.
- ప్రపంచ ప్రసిద్ధ క్లౌడ్ దిగ్గజాలు: **AWS**, **Microsoft Azure**, మరియు **Google Cloud (GCP)** ల మధ్య AI సర్వీసుల పోలిక.
- **Shared Responsibility Model** (క్లౌడ్ ప్రొవైడర్ బాధ్యత ఎంత? మన బాధ్యత ఎంత?).
- బిల్లులు పెరగకుండా సర్వర్‌లెస్ (Serverless Inference) మరియు ఆటో-స్కేలింగ్ టెక్నిక్స్ ను ఎలా ఉపయోగించాలో నేర్చుకోవడం.

---

## 2. రియల్ వరల్డ్ అనలాజీ (Real-World Analogy)

> 💡 **అనలాజీ: సొంత కారు కొనుగోలు vs అద్దె కారు vs బస్సు vs ఊబర్ టాక్సీ**
>
> - **ఆన్-ప్రిమైసెస్ (సొంత కారు కొనడం):**
>   మీరే కారు కొంటారు, పార్కింగ్ గ్యారేజ్ కట్టాలి, సర్వీసింగ్ చేయించాలి, బ్రేక్ డౌన్ అయితే రిపేర్ చేయించాలి. రేపు 10 మంది ఫ్రెండ్స్ వస్తే 4 సీట్ల కారు సరిపోదు. (కంపెనీలోనే ఫిజికల్ సర్వర్లు కొనడం లాంటిది).
> - **IaaS (కారు అద్దెకు తీసుకోవడం - Zoomcar/Hertz):**
>   మీరు కారును రోజువారీ అద్దెకు తీసుకుంటారు. ఏ కారు కావాలో మీరే ఎంచుకుంటారు (GPU సర్వర్ లాగా). కానీ డ్రైవింగ్ మీరే చేయాలి, పెట్రోల్ మీరే కొట్టించాలి. (ఉదా: AWS EC2, Azure VM, GCP Compute Engine).
> - **PaaS (ట్రావెల్ బస్సు / విమాన ప్రయాణం):**
>   మీరు టికెట్ కొని లగేజ్ తో వెళ్లి కూర్చుంటారు. డ్రైవర్, ఇంజిన్, డీజిల్, ఏసీ అన్నీ వాళ్ళే చూసుకుంటారు. మీరైతే మీ గమ్యస్థానానికి వెళ్తారు. (ఉదా: AWS SageMaker, GCP Vertex AI, Azure Container Apps).
> - **SaaS (ఊబర్ టాక్సీ బుక్ చేయడం):**
>   యాప్ లో లొకేషన్ క్లిక్ చేస్తారు. కారు వస్తుంది, గమ్యం చేర్చగానే కిలోమీటర్ కు ఇంత అని డబ్బులు కడతారు. ఇంజిన్ ఎలా పనిచేస్తుంది, టైర్లలో గాలి ఉందా లేదా మీకు అనవసరం! (ఉదా: OpenAI API, Google Gemini API, Claude API).

---

## 3. AI కోసం క్లౌడ్ సర్వీస్ పిరమిడ్

```
┌────────────────────────────────────────────────────────────────────────┐
│                        క్లౌడ్ సర్వీస్ పిరమిడ్                          │
├────────────────────────────────────────────────────────────────────────┤
│ SaaS: మోడల్-యాజ్-ఎ-సర్వీస్ (MaaS)                                      │
│ - మీరు మేనేజ్ చేసేది: ఏమీ లేదు, కేవలం API ప్రాంప్ట్ పంపిస్తారు.         │
│ - ఉదాహరణలు: OpenAI API, Gemini API, Anthropic Claude API               │
├────────────────────────────────────────────────────────────────────────┤
│ PaaS: మేనేజ్డ్ AI ప్లాట్‌ఫారమ్‌లు                                       │
│ - మీరు మేనేజ్ చేసేది: మీ పైథాన్ కోడ్, ఫైన్-ట్యూనింగ్ డేటా, ప్రాంప్ట్స్. │
│ - ఉదాహరణలు: AWS SageMaker, GCP Vertex AI, Azure AI Foundry            │
├────────────────────────────────────────────────────────────────────────┤
│ IaaS: ముడి వర్చువల్ సర్వర్లు (Raw Infrastructure)                      │
│ - మీరు మేనేజ్ చేసేది: Linux OS అప్‌డేట్స్, CUDA డ్రైవర్లు, నెట్‌వర్కింగ్.│
│ - ఉదాహరణలు: AWS EC2 (GPU p4de), Azure NDv4, GCP G2 Instances           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. బిగ్ 3 క్లౌడ్స్ మధ్య సేవల పోలిక (AWS vs Azure vs GCP)

| కేటగిరీ | AWS (Amazon Web Services) | Microsoft Azure | Google Cloud (GCP) |
| :--- | :--- | :--- | :--- |
| **ఫౌండేషన్ మోడల్ API** | Amazon Bedrock (Claude, Llama) | Azure OpenAI (GPT-4o) | Vertex AI Gemini API (Gemini 1.5/2.0) |
| **పూర్తి AI/ML ప్లాట్‌ఫారమ్** | AWS SageMaker | Azure Machine Learning | Vertex AI Pipelines & Model Garden |
| **ఆబ్జెక్ట్ స్టోరేజ్ (డేటా/మోడల్స్)** | Amazon S3 | Azure Blob Storage | Google Cloud Storage (GCS) |
| **సర్వర్‌లెస్ కంప్యూట్** | AWS Lambda | Azure Functions | Cloud Run / Cloud Functions |
| **కంటైనర్ ఇంజిన్** | AWS EKS / ECS | Azure AKS / Container Apps | Google Kubernetes Engine (GKE) / Cloud Run |
| **ఐడెంటిటీ & సెక్యూరిటీ** | AWS IAM & KMS | Entra ID (Azure AD) | Cloud IAM & Secret Manager |
| **డేటా వేర్‌హౌస్** | Amazon Redshift | Azure Synapse / Fabric | Google BigQuery |

---

## 5. సెక్యూరిటీ: ప్రిన్సిపల్ ఆఫ్ లీస్ట్ ప్రివిలేజ్ (Least Privilege)

ఫ్రెషర్స్ చేసే అతిపెద్ద తప్పు: `root` క్రెడెన్షియల్స్ లేదా మాస్టర్ API కీలను కోడ్ లో హార్డ్‌కోడ్ చేయడం.
ఎంటర్‌ప్రైజ్ క్లౌడ్ సిస్టమ్స్ లో సర్వీసులకు తాత్కాలిక అనుమతులు ఇచ్చేందుకు **IAM Roles (Role-Based Access Control)** ఉపయోగిస్తారు:

```
┌──────────────────┐               ┌──────────────────┐               ┌──────────────────┐
│   క్లౌడ్ సర్వీస్   │  రోల్ తీసుకుంటుంది │     IAM Role     │   పాలసీ రూల్స్   │  S3 బకెట్        │
│ (FastAPI సర్వర్) ├──────────────►│(కీలు అవసరం లేదు!)├──────────────►│ (AI మోడల్ ఫైల్స్)│
└──────────────────┘               └──────────────────┘               └──────────────────┘
```

### క్లీన్ పైథాన్ కోడ్: మల్టీ-క్లౌడ్ స్టోరేజ్ అబ్‌స్ట్రాక్షన్

క్లౌడ్ మారినా మీ కోడ్ మారకుండా ఉండటానికి ఒక యూనిఫైడ్ ఇంటర్‌ఫేస్ ను ఎలా డిజైన్ చేయవచ్చో చూద్దాం:

```python
# cloud_storage.py
import os
from typing import Protocol, List

class CloudStorageInterface(Protocol):
    def upload(self, local_path: str, remote_name: str) -> str:
        ...
    def download(self, remote_name: str, local_path: str) -> bool:
        ...

# 1. AWS S3 ఇంప్లిమెంటేషన్
class AWSS3Storage:
    def __init__(self, bucket: str):
        self.bucket = bucket
        print(f"AWS S3 బకెట్ కనెక్ట్ అయింది: s3://{self.bucket}")

    def upload(self, local_path: str, remote_name: str) -> str:
        # వాస్తవంలో: boto3.client('s3').upload_file(...)
        print(f"[AWS S3] అప్‌లోడ్ అవుతోంది: {local_path} -> s3://{self.bucket}/{remote_name}")
        return f"s3://{self.bucket}/{remote_name}"

    def download(self, remote_name: str, local_path: str) -> bool:
        print(f"[AWS S3] డౌన్‌లోడ్ పూర్తయింది: {remote_name}")
        return True

# 2. Google Cloud Storage (GCS) ఇంప్లిమెంటేషన్
class GoogleGCSStorage:
    def __init__(self, bucket: str):
        self.bucket = bucket
        print(f"Google Cloud బకెట్ కనెక్ట్ అయింది: gs://{self.bucket}")

    def upload(self, local_path: str, remote_name: str) -> str:
        # వాస్తవంలో: google.cloud.storage.Client()...
        print(f"[GCP GCS] అప్‌లోడ్ అవుతోంది: {local_path} -> gs://{self.bucket}/{remote_name}")
        return f"gs://{self.bucket}/{remote_name}"

    def download(self, remote_name: str, local_path: str) -> bool:
        print(f"[GCP GCS] డౌన్‌లోడ్ పూర్తయింది: {remote_name}")
        return True

# 3. ఫ్యాక్టరీ మెథడ్ (ఏ క్లౌడ్ కావాలంటే దాన్ని క్షణాల్లో ఎంచుకోవచ్చు)
def get_storage_engine(provider: str, bucket_name: str) -> CloudStorageInterface:
    if provider.upper() == "AWS":
        return AWSS3Storage(bucket_name)
    elif provider.upper() == "GCP":
        return GoogleGCSStorage(bucket_name)
    raise ValueError(f"తెలియని క్లౌడ్ ప్రొవైడర్: {provider}")

if __name__ == "__main__":
    env_cloud = os.getenv("TARGET_CLOUD", "GCP")
    storage = get_storage_engine(env_cloud, "ai-models-backup-2026")
    
    saved_url = storage.upload("model_weights.bin", "checkpoints/v1.bin")
    print(f"✅ ఫైల్ భద్రపరచబడిన లొకేషన్: {saved_url}")
```

---

## 6. ఫ్రెషర్స్ చేసే తీవ్రమైన తప్పులు & జాగ్రత్తలు

| తప్పు | ఎందుకు ప్రమాదకరం? | సరైన పద్ధతి |
| :--- | :--- | :--- |
| **GitHub లో క్లౌడ్ సీక్రెట్ కీలను పుష్ చేయడం** | పబ్లిక్ రెపోలో పెట్టిన 60 సెకన్లలో ఆటోమేటెడ్ బాట్స్ కీలను దొంగిలించి గంటల వ్యవధిలో ₹20 లక్షల క్రిప్టో-మైనింగ్ బిల్లు తెస్తాయి. | ఎట్టి పరిస్థితుల్లోనూ కీలను గిట్ లో పెట్టకూడదు. `.gitignore` లో `.env` పెట్టాలి, లేదా IAM Roles వాడాలి. |
| **GPU సర్వర్లను ఆఫ్ చేయడం మర్చిపోవడం** | A100 GPU సర్వర్ గంటకు దాదాపు ₹2,500 అవుతుంది. శుక్రవారం రాత్రి ఆఫ్ చేయడం మర్చిపోతే సోమవారం ఉదయానికి లక్షల్లో బిల్లు వస్తుంది. | తప్పకుండా బడ్జెట్ అలర్ట్స్ (AWS CloudWatch / GCP Budget) మరియు ఆటో-షట్‌డౌన్ స్క్రిప్ట్స్ సెటప్ చేసుకోవాలి. |
| **చిన్న యాప్‌లకు కూడా భారీ Kubernetes క్లస్టర్లు వాడటం** | రోజుకు 20 రిక్వెస్ట్‌లు వచ్చే సర్వీస్ కోసం నెలకు ₹15,000 కట్టి క్లస్టర్ మెయింటైన్ చేయడం దండగ. | ప్రారంభంలో ఎప్పుడూ సర్వర్‌లెస్ (Cloud Run లేదా AWS Lambda) వాడాలి. ట్రాఫిక్ పెరిగినప్పుడు మాత్రమే కంటైనర్ క్లస్టర్లకు మారాలి. |

---

## 7. ప్రాక్టికల్ ల్యాబ్ (Hands-on Lab)

### లక్ష్యం:
కేవలం మోడల్స్ డౌన్‌లోడ్ చేసుకోవడానికి మాత్రమే అనుమతి ఇచ్చే ఒక సురక్షితమైన AWS IAM Policy (JSON) ని తయారుచేయండి (మోడల్స్ ని డిలీట్ చేసే హక్కును ఖచ్చితంగా నిరోధించాలి).

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowDownloadModelsOnly",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::company-ai-models",
        "arn:aws:s3:::company-ai-models/*"
      ]
    },
    {
      "Sid": "DenyModelDeletion",
      "Effect": "Deny",
      "Action": [
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::company-ai-models/*"
    }
  ]
}
```

---

## 8. టాప్ 3 ఇంటర్వ్యూ ప్రశ్నలు & సమాధానాలు

### Q1: క్లౌడ్ కంప్యూటింగ్ లో Shared Responsibility Model అంటే ఏమిటి?
**సమాధానం:**
- **Security OF the Cloud (క్లౌడ్ ప్రొవైడర్ బాధ్యత):** ఫిజికల్ డేటా సెంటర్ భద్రత, కేబుల్స్, హార్డ్‌వేర్ రీప్లేస్‌మెంట్, పవర్ సప్లై మరియు సర్వర్ హార్డ్‌వేర్ కూలింగ్.
- **Security IN the Cloud (కస్టమర్/మన బాధ్యత):** మనం స్టోర్ చేసే డేటా ఎన్‌క్రిప్షన్, IAM యూజర్ పాస్‌వర్డ్‌లు, ఫైర్‌వాల్ రూల్స్, మరియు మనం రాసే అప్లికేషన్ కోడ్ సెక్యూరిటీ.

### Q2: Serverless Inference ఎప్పుడు వాడాలి? Dedicated GPU సర్వర్లు ఎప్పుడు వాడాలి?
**సమాధానం:**
- **Serverless (Cloud Run / Bedrock):** ఎప్పుడు రిక్వెస్ట్‌లు వస్తాయో తెలియనప్పుడు (ఉదా: ఆఫీస్ వేళల్లో మాత్రమే వాడే ఇంటర్నల్ టూల్స్). ఇక్కడ కేవలం రిక్వెస్ట్ వచ్చినప్పుడు మాత్రమే బిల్లు పడుతుంది, ఐడిల్ గా ఉన్నప్పుడు జీరో ఖర్చు.
- **Dedicated GPU (EC2 G5/P4):** నిరంతరం లక్షలాది మంది కస్టమర్లు వాడే 24/7 లైవ్ చాట్ యాప్‌లు లేదా భారీ మోడల్ ట్రైనింగ్ ఉన్నప్పుడు డెడికేటెడ్ సర్వర్లు చౌకగా మరియు అత్యంత వేగంగా పనిచేస్తాయి.

### Q3: AI ట్రైనింగ్ డేటా కోసం Object Storage (S3 / GCS) ఎందుకు అత్యుత్తమం?
**సమాధానం:**
ఆబ్జెక్ట్ స్టోరేజ్ అపరిమితమైన సామర్థ్యం (Unlimited Scaling), 99.999999999% (11 నైన్స్) డేటా సేఫ్టీని అందిస్తుంది. సాధారణ హార్డ్ డిస్క్‌లతో (EBS) పోలిస్తే దీని ఖర్చు చాలా తక్కువ. పైగా REST API ల ద్వారా ప్రపంచంలో ఎక్కడినుండైనా డేటాను వేగంగా డౌన్‌లోడ్ చేసుకునే సదుపాయం ఉంటుంది.
