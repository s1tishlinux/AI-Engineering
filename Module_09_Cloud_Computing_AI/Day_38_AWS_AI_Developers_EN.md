# Day 38: AWS for AI Developers (Amazon Bedrock, SageMaker & Serverless AI) 🟧

---

## 1. Day 38 Learning Objectives
- Master the AWS Generative AI ecosystem: **Amazon Bedrock** (serverless foundation models) vs. **Amazon SageMaker** (custom model training, hosting, and fine-tuning).
- Build a serverless AI API using the AWS Serverless stack: **API Gateway -> AWS Lambda -> Amazon Bedrock -> Amazon S3**.
- Write idiomatic Python code using the official AWS SDK: **`boto3`** (client creation, authentication, Converse API, streaming responses).
- Understand enterprise GenAI guardrails in Bedrock: PII redaction, toxic content filtering, and prompt injection defense.
- Implement cost optimization using Bedrock **Prompt Caching**, Batch Inference, and Provisioned Throughput vs. On-Demand pricing.

---

## 2. Real-World Analogy

> 💡 **Analogy: Custom Factory Machine vs. Universal Power Outlet**
>
> - **Amazon SageMaker (Custom Factory Machine):**
>   Imagine building a specialized industrial loom to weave custom silk fabrics. You select the exact machine size, install the motor, wire the gears, calibrate the spindles, and maintain it constantly. This is SageMaker: you configure EC2 GPU instances (`ml.g5.2xlarge`), build custom Docker containers, and tune PyTorch hyperparameters. Incredible control, but requires continuous engineering maintenance.
> - **Amazon Bedrock (Universal Power Outlet):**
>   Imagine you just want electricity to run your office lights. You don't build a power generator or lay coal in a furnace; you just plug an appliance into the wall socket and flip the switch.
>   In Bedrock, state-of-the-art foundation models (Anthropic Claude 3.5 Sonnet, Meta Llama 3, Amazon Titan, Mistral Large) are available through a single, unified `boto3` API call. Zero infrastructure to provision, zero GPUs to manage, 100% serverless!

---

## 3. Architecture Overview: Production Serverless AI on AWS

```
                    ┌──────────────────────────────┐
                    │      Client App (Mobile/Web) │
                    └──────────────┬───────────────┘
                                   │ HTTPS POST /generate
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        AWS CLOUD INFRASTRUCTURE                        │
│                                                                        │
│   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
│   │    Amazon API Gateway     │─────►│     AWS Lambda Function     │   │
│   │   (Rate Limiting & Auth)  │      │  (Python 3.11 + Boto3 SDK)  │   │
│   └───────────────────────────┘      └──────────────┬──────────────┘   │
│                                                     │                  │
│                                                     ▼                  │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                       AMAZON BEDROCK                           │   │
│   │                                                                │   │
│   │   ┌──────────────────────────┐    ┌────────────────────────┐   │   │
│   │   │    Bedrock Guardrails    │    │    Foundation Model    │   │   │
│   │   │ (PII Redaction, Safety)  │───►│ (Claude 3.5 / Llama 3) │   │   │
│   │   └──────────────────────────┘    └────────────────────────┘   │   │
│   └─────────────────────────────────────────────────┬──────────────┘   │
│                                                     │                  │
│                                                     ▼                  │
│                                      ┌─────────────────────────────┐   │
│                                      │          Amazon S3          │   │
│                                      │ (Audit Logs & Transcripts)  │   │
│                                      └─────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Key AWS AI Services Compared

1. **Amazon Bedrock:**
   - Serverless access to proprietary and open-source models via a unified API.
   - Built-in Knowledge Bases (Managed RAG using OpenSearch Serverless / Pinecone).
   - Built-in Agents (Multi-step tool calling and code interpretation).
2. **Amazon SageMaker:**
   - Full ML lifecycle: Data labeling (Ground Truth), notebook environments (Studio), distributed training, hyperparameter optimization, and real-time/asynchronous inference endpoints.
3. **AWS Lambda:**
   - Event-driven compute that executes Python code in milliseconds without managing servers.
4. **Amazon S3:**
   - The default storage layer for training datasets, prompt templates, and audit logs.

---

## 5. Coding Walkthrough: Calling Amazon Bedrock with Boto3 & Converse API

The modern standard for invoking any model on Amazon Bedrock is the **Converse API**, which provides a single consistent message schema across Claude, Llama, Titan, and Mistral:

```python
# bedrock_converse_demo.py
"""
Production Amazon Bedrock Integration with Boto3 Converse API
Requirements:
  pip install boto3
Ensure AWS credentials are configured via ~/.aws/credentials or environment variables.
"""
import json
import boto3
from botocore.exceptions import ClientError

def call_bedrock_converse(prompt_text: str, model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"):
    # 1. Initialize Bedrock Runtime Client
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )

    # 2. Format Messages payload using the unified Converse standard
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt_text}]
        }
    ]

    # 3. Configure Inference Parameters
    inference_config = {
        "maxTokens": 500,
        "temperature": 0.3,
        "topP": 0.9
    }

    system_prompts = [
        {"text": "You are a senior enterprise cloud architect. Provide concise, bulleted responses."}
    ]

    print(f"🚀 Sending request to Amazon Bedrock [Model: {model_id}]...")

    try:
        # 4. Invoke Converse API
        response = bedrock.converse(
            modelId=model_id,
            messages=messages,
            system=system_prompts,
            inferenceConfig=inference_config
        )

        # 5. Extract Text & Usage Metrics
        output_message = response["output"]["message"]
        text_content = output_message["content"][0]["text"]
        usage = response["usage"]

        print("\n--- Response Received ---")
        print(text_content)
        
        print("\n--- Telemetry & Token Usage ---")
        print(f"Input Tokens : {usage['inputTokens']}")
        print(f"Output Tokens: {usage['outputTokens']}")
        print(f"Total Tokens : {usage['totalTokens']}")
        print(f"Stop Reason  : {response['stopReason']}")
        
        return text_content

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        print(f"❌ AWS Client Error [{error_code}]: {error_msg}")
        return None

# AWS Lambda Handler Implementation
def lambda_handler(event, context):
    """
    Standard AWS Lambda entrypoint when triggered by API Gateway.
    """
    try:
        body = json.loads(event.get("body", "{}"))
        user_prompt = body.get("prompt", "What are the benefits of AWS Bedrock?")
        
        result = call_bedrock_converse(user_prompt)
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "SUCCESS", "response": result})
        }
    except Exception as err:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "ERROR", "message": str(err)})
        }

if __name__ == "__main__":
    # Test local invocation
    test_query = "Explain why serverless AI with AWS Bedrock reduces operational overhead."
    call_bedrock_converse(test_query)
```

---

## 6. Common Fresher Pitfalls

| Pitfall | Root Cause | Best Practice |
| :--- | :--- | :--- |
| **Model Access Not Enabled in AWS Console** | In Amazon Bedrock, models like Claude 3.5 Sonnet or Llama 3 are disabled by default. Calling them without requesting access results in `AccessDeniedException`. | Log into AWS Console -> Bedrock -> "Model access" -> Check the boxes and click "Request model access" before running code. |
| **Using Deprecated `invoke_model` with raw JSON strings** | Hardcoding custom JSON payloads for every different model family (`{"prompt": "..."}` for Llama vs `{"messages": [...]}` for Claude). | Always use `bedrock.converse()` or `converse_stream()`, which provides a single standardized payload for all models. |
| **AWS Lambda Timeout (Default 3 seconds)** | LLM inferences can take 5 to 15 seconds. The default AWS Lambda timeout is 3 seconds, causing Lambda to kill the process prematurely. | Increase Lambda timeout to at least 60 seconds and memory to 512MB in the Lambda configuration. |

---

## 7. Hands-on Lab: Streaming Bedrock Responses with Python

### Objective:
Implement streaming output from Amazon Bedrock using `converse_stream()` so that tokens render to the terminal in real time as they are generated.

```python
# lab_day38_streaming.py
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

messages = [{"role": "user", "content": [{"text": "Write a 4-line poem about cloud architecture."}]}]

response = bedrock.converse_stream(
    modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
    messages=messages
)

stream = response.get("stream")
if stream:
    print("Streaming output:")
    for event in stream:
        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"]["delta"]
            if "text" in delta:
                print(delta["text"], end="", flush=True)
    print("\nStream finished.")
```

---

## 8. Top 3 Interview Questions & Answers

### Q1: When should you choose Amazon Bedrock over Amazon SageMaker?
**Answer:**
- Choose **Amazon Bedrock** when you want to build GenAI applications using leading foundation models (Claude, Llama, Titan) without provisioning or managing infrastructure, paying strictly per token consumed.
- Choose **Amazon SageMaker** when you need to train custom deep learning models from scratch, deeply fine-tune large open-source weights with distributed GPUs, or deploy specialized proprietary architectures requiring custom CUDA extensions and dedicated container hosting.

### Q2: What is the AWS Bedrock Converse API and why is it significant?
**Answer:**
Previously, Bedrock required developers to write different raw JSON request structures for each model provider (`anthropic.*`, `meta.*`, `cohere.*`). The **Converse API** (`converse` and `converse_stream`) standardizes the conversation request and response schemas across all model families, while natively supporting multi-turn conversations, tool calling, and multimodal inputs without changing application code.

### Q3: How do Bedrock Guardrails protect enterprise AI applications?
**Answer:**
Bedrock Guardrails sit between the client and the foundation model, evaluating both user inputs and model outputs against customizable safety policies:
1. **Content Filtering:** Blocking hate speech, insults, and sexual content.
2. **Denied Topics:** Blocking inquiries outside approved corporate domains (e.g., blocking investment advice in a retail banking assistant).
3. **Sensitive Information Filters (PII):** Automatically detecting and masking credit card numbers, social security numbers, and emails.
4. **Contextual Grounding:** Blocking hallucinations by checking if the output is grounded in source context.
