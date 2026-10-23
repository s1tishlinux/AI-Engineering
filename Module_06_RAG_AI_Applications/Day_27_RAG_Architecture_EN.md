# Day 27: Retrieval-Augmented Generation (RAG Architecture)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The end-to-end **RAG Architecture**: Ingest $\rightarrow$ Chunk $\rightarrow$ Embed $\rightarrow$ Store $\rightarrow$ Retrieve $\rightarrow$ Augment $\rightarrow$ Generate.
2. Chunking strategies: Why `RecursiveCharacterTextSplitter` dominates naive splitting.
3. The math behind **Chunk Size vs Chunk Overlap** (preventing split-sentence amnesia).
4. Prompt Augmentation: Structuring retrieved context so the model cites page numbers and facts faithfully.
5. Building a zero-framework, production-grade RAG pipeline in pure Python.

---

## 1. The "Why": The Open-Book Exam Analogy

Imagine taking an advanced medical examination:
- **Base LLM without RAG (Closed-Book Exam)**: The student must answer purely from what they memorized months ago during school. If a new medical protocol was published yesterday, the student will guess, fabricate, or fail!
- **RAG-Powered LLM (Open-Book Exam)**: When asked a question, a librarian immediately dashes into the medical library, grabs the **exact 3 relevant pages**, hands them to the student, and says: *"Answer using ONLY these 3 pages, and cite your sources!"*

The student does not need to memorize the encyclopedia; they just need to read the retrieved cheat sheet!

---

## 2. The 7-Step RAG Pipeline

```
OFFLINE INGESTION PHASE:
[Raw Documents (PDF, MD, HTML)]
               │
               ▼ (Step 1: Document Loader)
        [Extracted Text]
               │
               ▼ (Step 2: Recursive Chunking)
   [Small Text Chunks (e.g. 500 chars)]
               │
               ▼ (Step 3: Embedding Model)
    [Dense Semantic Vectors]
               │
               ▼ (Step 4: Vector Database)
    [(Index & Persist in Chroma/Pinecone)]

ONLINE QUERY PHASE:
          User Question ("What is the refund policy?")
               │
               ▼ (Step 5: Semantic Retrieval)
[Retrieve Top-K Most Similar Chunks from Vector DB]
               │
               ▼ (Step 6: Context Augmentation)
   Construct Grounded Prompt with <context>
               │
               ▼ (Step 7: LLM Generation)
  Grounded Answer with Source Citations!
```

---

## 3. Chunking Strategies: Size vs Overlap

Why can't we just embed an entire 50-page PDF as a single vector?
- If you embed 50 pages into one vector, all the specific details get averaged out into a generic, blurry blur of numbers!
- You must slice documents into bite-sized **chunks** (e.g. 400–800 characters).

### The Overlap Principle:
If a crucial sentence is sliced in half right across a boundary:
- Chunk 1: *"...the annual employee bonus is paid only if..."*
- Chunk 2: *"...the company hits its Q4 EBIT target."*

Neither chunk contains the complete fact!
**Chunk Overlap (e.g. 100 characters)** ensures that the end of Chunk 1 repeats at the beginning of Chunk 2, preserving contextual coherence across borders.

```python
def naive_chunk_with_overlap(text: str, chunk_size: int = 200, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += (chunk_size - overlap)  # Slide window forward
    return chunks
```

---

## 4. Grounding and Context Injection

The prompt structure determines whether your RAG pipeline succeeds or hallucinates:

```python
GROUNDED_RAG_PROMPT_TEMPLATE = """
You are an Enterprise Knowledge Assistant. Answer the user's question using ONLY the facts 
contained within the <context> tags below.

<rules>
1. If the answer cannot be determined strictly from the context, state: "I cannot find this information in the provided documentation."
2. DO NOT speculate, assume, or extrapolate beyond the provided text.
3. Cite the document ID for every claim you make.
</rules>

<context>
{retrieved_chunks_block}
</context>

<user_question>
{user_query}
</user_question>
"""
```

---

## 5. Common Fresher Pitfalls

1. **Chunks Too Small or Too Big**:
   - Too small (50 chars): Loses sentence meaning.
   - Too big (5000 chars): Drowns the specific answer in irrelevant noise, triggering "Lost in the Middle".
   - *Sweet spot for most enterprise RAG*: 500 to 1,000 characters with 10%–20% overlap.
2. **Not Handling Empty Retrievals**:
   - If the vector database returns chunks with very poor similarity distance (e.g. distance > 0.8), passing them anyway forces the model to hallucinate. Always filter out low-confidence chunks!
3. **Omitting Source Metadata**:
   - In production, users always ask: *"Where did you get this answer?"* Always attach `source_url`, `page_number`, or `document_id` to your chunk metadata.

---

## 6. Daily Hands-On Lab

### 🧪 Exercise: Build an End-to-End Grounded RAG Pipeline from Scratch
**Scenario**: Ingest a real-world company policy document into ChromaDB, chunk it with overlap, retrieve the most relevant section for a user query, and feed it into Google Gemini with strict anti-hallucination grounding!

```python
# =========================================================
# Day 27 Lab: End-to-End Grounded RAG Pipeline
# =========================================================
import chromadb
from google import genai
from google.genai import types

# 1. Raw Company Policy Document
COMPANY_POLICY_DOC = """
TECHIN GLOBAL EMPLOYEE HANDBOOK (REVISION 2026)
SECTION 1: EQUIPMENT & HARDWARE
Employees are provided a ₹1,50,000 allowance for home office setups. 
Hardware upgrades are permitted every 24 months upon manager approval.

SECTION 2: HEALTH & WELLNESS BENEFITS
All full-time employees and their dependents receive comprehensive health insurance 
covering up to ₹10,00,000 per family. In addition, an annual mental wellness stipend 
of ₹25,000 is available for certified counseling sessions.

SECTION 3: PARENTAL LEAVE
Primary caregivers are entitled to 26 weeks of fully paid parental leave. 
Secondary caregivers receive 6 weeks of fully paid leave. Both must be utilized 
within the first 12 months of the child's birth or legal adoption.
"""

# 2. Text Chunker with Overlap
def split_document(text: str, chunk_size: int = 250, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start + chunk_size].strip()
        if len(chunk) > 20:
            chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

chunks = split_document(COMPANY_POLICY_DOC)
print(f"Generated {len(chunks)} chunks from policy document.")

# 3. Store into ChromaDB
chroma_client = chromadb.Client()
policy_collection = chroma_client.create_collection("techin_handbook")

policy_collection.add(
    documents=chunks,
    metadatas=[{"source": "Employee_Handbook_2026.pdf", "chunk_id": f"chunk_{i}"} for i in range(len(chunks))],
    ids=[f"id_{i}" for i in range(len(chunks))]
)

# 4. RAG Retrieval & Prompt Assembly
def query_rag_pipeline(user_query: str):
    # Retrieve top 2 most relevant chunks
    results = policy_collection.query(query_texts=[user_query], n_results=2)
    retrieved_texts = results["documents"][0]
    
    context_block = "\n---\n".join(retrieved_texts)
    
    prompt = f"""
    Answer the user question using ONLY the provided context below.
    If not found, reply: "I do not have access to that information in the handbook."

    <context>
    {context_block}
    </context>

    Question: {user_query}
    """
    
    # 5. Generate Grounded Response with Gemini
    gemini_client = genai.Client()
    response = gemini_client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0)
    )

    print("\n" + "="*55)
    print(f"User Query : {user_query}")
    print(f"Retrieved Context Chunks:\n{context_block}")
    print("\nAI Grounded Response:")
    print(response.text.strip())
    print("="*55)

# Test 1: Grounded question from text
query_rag_pipeline("How much mental wellness allowance can I claim annually?")

# Test 2: Unanswerable question (Should safely refuse!)
query_rag_pipeline("Can I bring my pet dog to the Hyderabad office?")
```

---

## 7. Interview Quick-Fire Questions

1. **Q: What is the purpose of Chunk Overlap in RAG pipelines?**
   - **Answer**: Chunk Overlap (typically 10% to 20% of the chunk size) ensures that sentences, semantic thoughts, or entities that span across arbitrary character boundaries are not severed in the middle. It provides contextual continuity so neither adjacent chunk loses the surrounding semantic context needed for accurate retrieval.
2. **Q: How does RAG solve the hallucination problem in LLMs?**
   - **Answer**: Base LLMs hallucinate because they rely on fuzzy parametric memory learned during pretraining. RAG converts the generation task into an **extractive, grounded synthesis task** by retrieving the exact factual text chunks from an external database and explicitly instructing the model in the system prompt to answer strictly based on the provided `<context>` and cite sources.
3. **Q: What is the difference between Dense Retrieval and Sparse Retrieval?**
   - **Answer**: **Dense Retrieval** uses neural embedding models (bi-encoders) to find semantically similar passages in high-dimensional vector space (e.g. "car" matches "automobile"). **Sparse Retrieval** (e.g. BM25 / TF-IDF) relies on exact lexical token matching and term frequency statistics. Modern production RAG combines both via **Hybrid Search**.
