# Day 39: Microsoft Azure for AI Developers (Azure AI Foundry & OpenAI Service) 🔷

---

## 1. Day 39 Learning Objectives
- Master the Microsoft enterprise AI ecosystem: **Azure AI Foundry** (formerly Azure AI Studio), **Azure OpenAI Service**, and **Azure Machine Learning**.
- Understand enterprise private networking & compliance: Deploying OpenAI models (GPT-4o, GPT-4o-mini, text-embedding-3) within private virtual networks (VNets) with zero data leaving corporate security perimeters.
- Implement serverless AI microservices using **Azure Functions (Python v2 programming model)** and **Azure Blob Storage**.
- Utilize **Microsoft Entra ID (Azure Active Directory)** authentication via `DefaultAzureCredential` to eliminate hardcoded API keys.
- Implement Content Safety filters: Protected material detection, prompt injection shields, and self-harm filters.

---

## 2. Real-World Analogy

> 💡 **Analogy: Public Internet Cafe vs. High-Security Bank Vault**
>
> - **Public Consumer OpenAI API (`api.openai.com`):**
>   Imagine using an internet cafe. It's fast, convenient, and anyone with a credit card can sit down and browse. But if you work at a bank or hospital, bringing top-secret patient records or banking ledgers into a public cafe breaches every privacy law in existence.
> - **Azure OpenAI Service (The Private Bank Vault):**
>   Microsoft took the exact same GPT-4o engines from OpenAI and installed them inside Microsoft's hardened, enterprise-certified **Swiss Bank Vault (Azure Cloud)**.
>   - Your data **NEVER** trains OpenAI's public models.
>   - All traffic stays inside your company's private fiber network (Azure Private Link / VNet).
>   - Access is audited by enterprise single-sign-on (Microsoft Entra ID).
>   - Full compliance with HIPAA, GDPR, SOC2, and ISO certifications.

---

## 3. Architecture Overview: Enterprise RAG on Microsoft Azure

```
                    ┌──────────────────────────────┐
                    │  Enterprise User / Web App   │
                    └──────────────┬───────────────┘
                                   │ HTTPS Request
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        AZURE VIRTUAL NETWORK (VNET)                    │
│                                                                        │
│   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
│   │      Azure API Mgmt       │─────►│    Azure Functions (v2)     │   │
│   │   (OAuth2 / Entra ID)     │      │   (Microservice Backend)    │   │
│   └───────────────────────────┘      └──────────────┬──────────────┘   │
│                                                     │                  │
│                                                     ▼                  │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                      AZURE AI FOUNDRY                          │   │
│   │                                                                │   │
│   │   ┌──────────────────────────┐    ┌────────────────────────┐   │   │
│   │   │   Azure AI Search        │    │  Azure OpenAI Service  │   │   │
│   │   │ (Hybrid Vector + BM25)   │◄──►│  (GPT-4o Deployment)   │   │   │
│   │   └──────────────────────────┘    └────────────────────────┘   │   │
│   │                 ▲                                              │   │
│   │                 │ Managed Identity                             │   │
│   │   ┌─────────────┴────────────┐                                 │   │
│   │   │    Azure Blob Storage    │                                 │   │
│   │   │  (PDFs & Enterprise Docs)│                                 │   │
│   │   └──────────────────────────┘                                 │   │
│   └────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Key Microsoft Azure AI Services

1. **Azure AI Foundry:**
   - The unified web portal and SDK uniting Azure OpenAI, model evaluation tools, custom fine-tuning, and multi-modal prompt engineering.
2. **Azure OpenAI Service:**
   - Enterprise deployments of GPT-4o, GPT-4o-mini, DALL-E 3, and Whisper with enterprise SLA and data isolation.
3. **Azure AI Search (formerly Cognitive Search):**
   - The premier enterprise RAG retrieval engine: supports hybrid search (combining dense vector search with sparse BM25 keyword matching) and semantic re-ranking.
4. **Microsoft Entra ID & Managed Identity:**
   - Zero-trust authentication allowing Azure Functions to authenticate directly to Azure OpenAI without storing API keys in configuration files.

---

## 5. Coding Walkthrough: Enterprise Python Code with Azure OpenAI & Managed Identity

Here is how production systems call Azure OpenAI using Microsoft's recommended `DefaultAzureCredential` (no hardcoded keys!) and the standard `openai` Python SDK:

```python
# azure_openai_enterprise.py
"""
Production Azure OpenAI with Microsoft Entra ID Authentication
Requirements:
  pip install openai azure-identity
"""
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def run_azure_openai_query(prompt_text: str):
    # 1. Fetch Configuration from Environment Variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://my-enterprise-ai.openai.azure.com/")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-production")

    print(f"Connecting to Azure OpenAI Endpoint: {endpoint}")

    # 2. Keyless Zero-Trust Authentication via Microsoft Entra ID
    # DefaultAzureCredential automatically checks:
    # 1. Environment variables -> 2. Workload Identity -> 3. Azure CLI login
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default"
    )

    # 3. Instantiate Official AzureOpenAI Client
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version=api_version
    )

    print(f"🚀 Invoking Azure Deployment '{deployment_name}'...")

    try:
        # 4. Execute Chat Completion
        response = client.chat.completions.create(
            model=deployment_name,  # In Azure, this must match your Deployment Name!
            messages=[
                {"role": "system", "content": "You are an enterprise Azure cloud advisor."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.2,
            max_tokens=400
        )

        choice = response.choices[0].message
        print("\n--- Response from Azure OpenAI ---")
        print(choice.content)

        print("\n--- Usage & Billing Telemetry ---")
        usage = response.usage
        print(f"Prompt Tokens    : {usage.prompt_tokens}")
        print(f"Completion Tokens: {usage.completion_tokens}")
        print(f"Total Tokens     : {usage.total_tokens}")

        return choice.content

    except Exception as e:
        print(f"❌ Azure OpenAI Execution Error: {str(e)}")
        return None

# Azure Functions v2 Python Model Example
def azure_function_entrypoint():
    """
    Simulates an Azure Functions HTTP trigger (function_app.py in Python v2 model)
    """
    sample_request = "How does Azure OpenAI guarantee enterprise data privacy?"
    return run_azure_openai_query(sample_request)

if __name__ == "__main__":
    # Test execution
    azure_function_entrypoint()
```

---

## 6. Common Fresher Pitfalls

| Pitfall | Root Cause | Best Practice |
| :--- | :--- | :--- |
| **Passing Model Name instead of Deployment Name** | In public OpenAI, `model="gpt-4o"`. In Azure, you must pass the exact name given when creating the deployment in Azure AI Studio (e.g., `model="my-gpt4o-deployment"`). | Double-check the Azure Portal "Deployments" tab and pass the deployment name string. |
| **Hardcoding API Keys in `local.settings.json`** | Committing Azure cognitive keys to source control breaches corporate security policies. | Use `DefaultAzureCredential()` and assign the `Cognitive Services OpenAI User` role to your managed identity. |
| **Exceeding TPM (Tokens Per Minute) Limits** | Azure OpenAI enforces strict Regional Quotas (e.g. 30K TPM). Sudden bursts of requests return HTTP 429 Rate Limit errors. | Implement exponential backoff retry policies or use Azure OpenAI Provisioned Throughput Units (PTU) for guaranteed capacity. |

---

## 7. Hands-on Lab: Azure Function AI Endpoint

### Objective:
Write a clean `function_app.py` using the Azure Functions Python v2 programming model that exposes an HTTP POST route `/api/summarize` to process text.

```python
# function_app.py
import azure.functions as func
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="summarize", methods=["POST"])
def summarize_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing text summarization request.")
    try:
        req_body = req.get_json()
        raw_text = req_body.get("text", "")
        
        if not raw_text:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'text' in JSON body"}),
                status_code=400,
                mimetype="application/json"
            )

        # Mock AI summary
        summary = f"Summary ({len(raw_text)} chars processed): {raw_text[:100]}..."
        
        return func.HttpResponse(
            json.dumps({"status": "SUCCESS", "summary": summary}),
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

## 8. Top 3 Interview Questions & Answers

### Q1: How does Azure OpenAI differ from directly using the OpenAI public API?
**Answer:**
Azure OpenAI provides the exact same GPT-4o models but runs within Microsoft's global enterprise cloud infrastructure. Critical enterprise distinctions include:
1. **Data Privacy:** Customer prompts and completions are never used to train or retrain any models.
2. **Network Isolation:** Access can be completely restricted to private corporate networks via Azure Private Endpoints with zero exposure to the public internet.
3. **Enterprise Compliance:** Backed by Microsoft enterprise SLAs, GDPR, HIPAA, and ISO certifications.
4. **Unified Billing & Governance:** Integrated with Microsoft Entra ID (role-based access control) and unified Azure subscription billing.

### Q2: What is Hybrid Search in Azure AI Search and why is it preferred for enterprise RAG?
**Answer:**
Pure vector search (dense embeddings) excels at understanding conceptual semantics, but can fail on exact keyword lookups, such as part numbers (e.g., `Part-X892-Rev3`), product codes, or legal case citations. Hybrid Search combines:
1. **Dense Vector Retrieval** (capturing meaning and context), and
2. **Sparse Lexical Search (BM25)** (capturing exact keyword and acronym matches),
fused together using Reciprocal Rank Fusion (RRF) and semantic re-ranking to deliver optimal retrieval precision.

### Q3: What is the purpose of `DefaultAzureCredential` in Python?
**Answer:**
`DefaultAzureCredential` from the `azure-identity` library enables seamless zero-trust authentication across development and production environments without changing code. During local development, it automatically picks up credentials from the developer's Azure CLI or VS Code login. In production (Azure Functions, AKS, VMs), it automatically uses the cloud resource's **Managed Identity**, completely eliminating the need to store, rotate, or risk leaking API keys.
