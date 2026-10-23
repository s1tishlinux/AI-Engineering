# Day 28: LangChain & LlamaIndex Frameworks

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Why enterprise teams use frameworks instead of hardcoding raw SDK API calls.
2. **LangChain Core & LCEL (LangChain Expression Language)**: Composing pipelines with the Unix pipe operator `|`.
3. **LlamaIndex**: The specialist framework for hierarchical document ingestion and retrieval.
4. The Definitive Decision Matrix: **LangChain vs LlamaIndex** (When to choose which).
5. Building modular, production-ready chains in both ecosystems.

---

## 1. The "Why": Why Not Just Use the Raw Python SDK?

Writing raw SDK code (like Day 23–24) works well for simple one-off scripts. But in complex enterprise AI software, you quickly encounter boilerplate nightmares:
- Swapping Gemini for OpenAI requires rewriting your prompt parsing, streaming handlers, and schema formatting.
- Connecting 4 different data sources (PDFs, Confluence, SQL, Slack) requires writing 4 custom ETL chunkers.
- Chaining multi-step logic (e.g. *Summarize document $\rightarrow$ Translate to Telugu $\rightarrow$ Extract action items into JSON*) requires dozens of nested function callbacks.

**LangChain and LlamaIndex provide standardized, plug-and-play abstractions for the entire AI application lifecycle.**

---

## 2. LangChain Expression Language (LCEL)

The modern LangChain standard (v0.2+) is built on **LCEL**, inspired by Unix pipes:
```bash
cat file.txt | grep "ERROR" | wc -l
```

In LangChain, components implement the `Runnable` protocol, allowing them to be piped together seamlessly:

$$\text{Prompt} \;\;|\;\; \text{LLM Model} \;\;|\;\; \text{Output Parser}$$

```python
# To run this lab: pip install langchain-core langchain-google-genai
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# Step 1: Define a Prompt Template with input variables
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Python performance engineer. Respond concisely."),
    ("user", "Explain how {concept} improves application throughput.")
])

# Step 2: Initialize the Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Step 3: Define Output Parser
parser = StrOutputParser()

# Step 4: The LCEL Pipe! (Clean, declarative, and streaming-ready)
chain = prompt_template | llm | parser

# Invoke the Chain
response = chain.invoke({"concept": "Asyncio Event Loops"})
print("--- LCEL CHAIN OUTPUT ---")
print(response)
```

---

## 3. LlamaIndex: The Document Specialist

While LangChain is a general-purpose orchestration framework, **LlamaIndex** was built from the ground up as a specialized **Data Framework for LLMs**.
- It treats documents as **Nodes** with rich hierarchical metadata.
- It provides out-of-the-box connectors for 100+ enterprise repositories (Notion, Google Drive, Jira, S3).
- Setting up a state-of-the-art RAG pipeline requires literally **3 lines of code**:

```python
# To run: pip install llama-index llama-index-llms-gemini llama-index-embeddings-gemini
from llama_index.core import Document, VectorStoreIndex

# 1. Create Documents
docs = [
    Document(text="TechIn Global provides ₹1,50,000 WFH home office equipment allowance.", metadata={"topic": "benefits"}),
    Document(text="Employees can request hardware refreshes every 24 months.", metadata={"topic": "hardware"})
]

# 2. Build the Vector Store Index in memory (Handles chunking & embedding automatically!)
index = VectorStoreIndex.from_documents(docs)

# 3. Create a Query Engine
query_engine = index.as_query_engine()

# 4. Query
response = query_engine.query("What is the home office allowance amount?")
print("\n--- LLAMAINDEX RAG RESPONSE ---")
print(response)
```

---

## 4. The Decision Matrix: LangChain vs LlamaIndex

| Dimension | LangChain | LlamaIndex |
| :--- | :--- | :--- |
| **Core Philosophy** | General-purpose orchestration & multi-agent execution | Deep, specialized document indexing and data retrieval |
| **Best Used For** | Complex agent workflows, tool routing, chatbots with actions | Search-heavy RAG, parsing complex multi-page PDFs, structured tables |
| **Custom Chains** | Outstanding (**LCEL** pipe composability) | Moderate |
| **Agentic Framework** | **LangGraph** (State graphs & cyclic workflows) | LlamaAgents |
| **Industry Practice** | Often combined! Use LlamaIndex for indexing, LangChain/LangGraph for agent logic. |

---

## 5. Common Fresher Pitfalls

1. **Using outdated LangChain syntax (Pre-LCEL)**:
   - ⚠️ Avoid old tutorials using `LLMChain`, `ConversationChain`, or `initialize_agent`. In modern LangChain, everything must be written using **LCEL (`prompt | model | parser`)** and **LangGraph**.
2. **Framework Lock-In**:
   - Don't build unnecessary abstractions. If you only need to call Gemini once, use the raw Google GenAI SDK. Only bring in LangChain/LlamaIndex when you need composability, complex loaders, or vector store integrations.
3. **Overwriting Stream Handlers**:
   - In LCEL, every chain automatically supports `.stream()` and `.batch()` out of the box! You don't need to write manual streaming callbacks.

---

## 6. Daily Hands-On Lab

### 🧪 Exercise: Build a Multi-Stage Data Extraction & Translation Chain
**Scenario**: Ingest customer feedback in any language, extract key complaints, and translate the summary into English using a composable LangChain LCEL pipeline.

```python
# =========================================================
# Day 28 Lab: Multi-Stage LCEL Transformation Chain
# =========================================================
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Step 1: Prompt to Extract Complaints
extract_prompt = ChatPromptTemplate.from_template(
    "Analyze this customer feedback and list the top 2 actionable complaints:\n\n{feedback}"
)

# Step 2: Prompt to Translate into Formal Executive English
translate_prompt = ChatPromptTemplate.from_template(
    "Translate and format the following complaints into a formal executive briefing:\n\n{complaints}"
)

# Build Composable Multi-Stage Pipeline
# Feedback -> Extract -> Complaints -> Translate -> Final Summary
extraction_chain = extract_prompt | llm | StrOutputParser()
full_pipeline = (
    {"complaints": extraction_chain}
    | translate_prompt
    | llm
    | StrOutputParser()
)

sample_raw_feedback = """
ఈ యాప్ నిన్నటి నుండి చాలా స్లోగా ఉంది. నేను పేమెంట్ చేస్తుంటే మధ్యలోనే యాప్ క్లోజ్ అయిపోయింది! 
మళ్లీ ఓపెన్ చేస్తే అమౌంట్ కట్ అయింది కానీ టికెట్ రాలేదు. వెంటనే రీఫండ్ ఇప్పించండి!
"""

print("Executing Multi-Stage Enterprise Chain...")
result = full_pipeline.invoke({"feedback": sample_raw_feedback})

print("\n" + "="*50)
print("EXECUTIVE INCIDENT BRIEFING (ENGLISH)")
print("="*50)
print(result)
print("="*50)
```

---

## 7. Interview Quick-Fire Questions

1. **Q: What is LCEL (LangChain Expression Language) and what advantages does it offer?**
   - **Answer**: LCEL is a declarative, pipe-based syntax for chaining LangChain components (`prompt | model | parser`). It provides automatic out-of-the-box support for synchronous, asynchronous (`ainvoke`), streaming (`astream`), batching (`batch`), parallel execution, and built-in tracing with LangSmith without writing custom boilerplate.
2. **Q: When would you choose LlamaIndex over LangChain?**
   - **Answer**: Choose LlamaIndex when the core engineering bottleneck is **data management and search quality**—such as parsing heterogeneous complex documents (PDFs with tables, spreadsheets, slide decks), creating hierarchical tree indexes, or executing multi-document synthesis queries. Choose LangChain when the challenge is general orchestration, multi-tool agent routing, and complex state management.
3. **Q: How does a LangChain Output Parser work?**
   - **Answer**: An Output Parser takes the raw `AIMessage` produced by the LLM and transforms it into a downstream data structure (e.g., `StrOutputParser` extracts the string text, while `JsonOutputParser` or `PydanticOutputParser` parses and validates the text against a structured schema), handling fallback logic and retries on parse errors.
