# Day 24: Advanced LLM Capabilities (Function Calling, Structured JSON & Multimodality)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. **Tool / Function Calling**: How an LLM can intelligently decide to call your custom Python functions.
2. Guaranteed Structured Outputs using **Pydantic schemas** and `response_schema`.
3. Native **Multimodal Inference**: Passing images, audio, and documents directly to models.
4. **Context Caching**: Slashing latency and cutting API token costs by 75%+ on large repetitive documents.

---

## 1. The "Why": Giving LLMs Hands and Eyes

A standard LLM is a trapped brain in a jar:
- It cannot check today's stock price or query your SQL database.
- It cannot see an invoice image or listen to an audio voicemail.
- It produces conversational text that breaks backend databases when you expect strict JSON.

**Advanced LLM capabilities give the model:**
1. **Hands (Function Calling)**: The ability to execute database queries, send emails, or run calculations.
2. **Eyes & Ears (Multimodality)**: Direct comprehension of diagrams, charts, audio, and video.
3. **Guaranteed Structure (Pydantic Output)**: Deterministic, parse-safe JSON objects for production databases.

---

## 2. Structured Outputs with Pydantic Schemas

Telling an LLM *"Please output only JSON"* in the prompt still risks broken formatting 5% of the time.
Modern SDKs enforce **Schema-Constrained Decoding** directly at the token sampling level:

```python
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# Step 1: Define the strict target schema using Pydantic
class JobCandidateProfile(BaseModel):
    full_name: str
    years_of_experience: float
    core_technical_skills: list[str]
    current_location: str
    suitable_for_senior_role: bool = Field(description="True if experience >= 5 years")

# Step 2: Configure Gemini to enforce this schema
client = genai.Client()

resume_text = """
Rahul Swaminathan is a Senior DevOps Engineer based in Bengaluru with 7.5 years of 
experience architecting Kubernetes clusters, CI/CD with GitHub Actions, and Terraform on GCP.
"""

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=f"Extract the candidate profile from this resume:\n{resume_text}",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=JobCandidateProfile
    )
)

print("--- GUARANTEED PARSED JSON ---")
print(response.text)

# Guaranteed 100% type-safe deserialization!
candidate = JobCandidateProfile.model_validate_json(response.text)
print(f"Extracted: {candidate.full_name} | Senior? {candidate.suitable_for_senior_role}")
```

---

## 3. Tool / Function Calling: How It Actually Works

⚠️ **The Big Fresher Misconception**:
The LLM does **NOT** run your Python code directly on its servers!
1. You give the LLM a list of Python function declarations (name, parameters, docstrings).
2. The LLM analyzes the user's prompt and replies: *"Hey application, I cannot answer this on my own, but please run `get_stock_price(ticker='GOOG')` and give me the result!"*
3. **Your application** runs the function locally and feeds the output back to the LLM.
4. The LLM formulates the final human response!

```python
from google import genai
from google.genai import types

# 1. Define your real Python tool
def get_order_delivery_status(order_id: int) -> dict:
    """Fetches real-time shipping status for an e-commerce order ID."""
    # Simulated database lookup
    MOCK_DB = {
        1001: {"status": "OUT_FOR_DELIVERY", "location": "Hyderabad Hub", "eta": "Today by 6 PM"},
        1002: {"status": "PROCESSING", "location": "Mumbai Warehouse", "eta": "Tomorrow"}
    }
    return MOCK_DB.get(order_id, {"status": "NOT_FOUND", "message": "Order ID does not exist."})

# 2. Hand the tool to Gemini
client = genai.Client()

chat = client.chats.create(
    model="gemini-1.5-flash",
    config=types.GenerateContentConfig(
        tools=[get_order_delivery_status],  # Gemini automatically reads docstrings & type hints!
        temperature=0.0
    )
)

# 3. User asks about their order
response = chat.send_message("Where is my order #1001 right now?")
print("AI Assistant:", response.text)
# Output: "Your order #1001 is currently Out for Delivery from the Hyderabad Hub and is estimated to arrive today by 6 PM!"
```

---

## 4. Native Multimodality: Images and PDFs

Modern Gemini models process images natively in the same token space as text:

```python
from google import genai
from PIL import Image
import io

client = genai.Client()

# Load a local image using PIL
image = Image.open("sample_chart.png")

prompt = "Analyze this financial chart. What was the quarterly revenue growth between Q2 and Q3?"

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=[prompt, image]
)

print("Vision Analysis:\n", response.text)
```

---

## 5. Context Caching (Slashing Enterprise API Costs)

When repeatedly querying a massive 500-page company policy or a 50,000-line codebase:
- In traditional APIs: You upload the 500-page document on **every single user question**, paying full price every time!
- **Context Caching**: You upload the document **ONCE** to the cloud. Gemini caches the precomputed KV-attention states. Subsequent queries against the cached document are **4x cheaper and 3x faster**!

---

## 6. Common Fresher Pitfalls

1. **Poor or missing function docstrings**:
   - The LLM relies **entirely** on your function's docstring and argument type hints to know when and how to call it. Writing `def query(x):` with no docstring will cause the LLM to guess randomly or fail!
2. **Assuming the LLM executes the code itself**:
   - Remember: The LLM only returns a JSON payload describing which function to invoke. Your application code is the bridge.
3. **Uploading raw 4K uncompressed images**:
   - Excessively massive images burn tokens unnecessarily without improving OCR quality. Resize images to reasonable dimensions (e.g. 1024x1024) before sending.

---

## 7. Daily Hands-On Lab

### 🧪 Exercise: Build an AI SQL Database Assistant with Function Calling
**Scenario**: Users ask questions in plain English (*"Show me the total revenue from customers in India"*). The LLM uses function calling to run a safe read-only SQL query against an in-memory SQLite database and summarize the result.

```python
# =========================================================
# Day 24 Lab: SQL Query Assistant via Function Calling
# =========================================================
import sqlite3
from google import genai
from google.genai import types

# Step 1: Create an in-memory SQLite database with sample transactions
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE sales (id INT, product TEXT, country TEXT, revenue_usd FLOAT)")
cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", [
    (1, "Cloud AI License", "India", 4500.0),
    (2, "Developer Seat", "India", 1200.0),
    (3, "Enterprise Tier", "USA", 15000.0),
    (4, "Support Package", "UK", 3000.0)
])
conn.commit()

# Step 2: The Safe Tool
def execute_sql_query(query: str) -> str:
    """Executes a read-only SQL query against the company sales database."""
    print(f"\n⚡ [TOOL EXECUTION] Running SQL: {query}")
    if not query.strip().upper().startswith("SELECT"):
        return "ERROR: Only read-only SELECT queries are permitted."
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return str(rows)
    except Exception as e:
        return f"SQL Error: {e}"

# Step 3: Run the AI Pipeline with Function Calling
client = genai.Client()
chat = client.chats.create(
    model="gemini-1.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a Business Intelligence Analyst. Use the execute_sql_query tool to query the 'sales' table.",
        tools=[execute_sql_query],
        temperature=0.0
    )
)

response = chat.send_message("What is the total revenue generated from customers in India?")
print("\n--- FINAL AI BUSINESS REPORT ---")
print(response.text)
```

---

## 8. Interview Quick-Fire Questions

1. **Q: How does Tool / Function Calling work in LLM architectures?**
   - **Answer**: The developer supplies a JSON Schema specification of available functions (name, description, parameter types). When processing a prompt, if the LLM recognizes that a tool is needed, it pauses text generation and returns a structured `tool_call` object containing the chosen function name and parsed JSON arguments. The client application executes the tool and returns the result in a `tool_response` message, allowing the model to summarize the final output.
2. **Q: How do guaranteed JSON outputs work under the hood without regex retries?**
   - **Answer**: Modern LLM engines implement **Grammar-Guided or Schema-Constrained Decoding**. During token sampling at each step, the sampling logits are masked using a Finite State Machine (FSM) compiled from the Pydantic JSON schema, making it mathematically impossible for the model to emit a token that violates the JSON grammar.
3. **Q: What is Context Caching and when should you use it?**
   - **Answer**: Context Caching precomputes and stores the Key-Value (KV) attention activations for a large, static prefix of tokens (e.g. documentation, books, codebases) in GPU memory. When multiple subsequent queries reference that same context, the model skips the computationally expensive prefill phase, reducing time-to-first-token (TTFT) by up to 80% and input token costs by up to 75%.
