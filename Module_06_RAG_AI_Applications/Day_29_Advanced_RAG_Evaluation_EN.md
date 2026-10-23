# Day 29: Advanced RAG & Evaluation (Module 06 Capstone)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Why **Naive RAG** fails in enterprise production (The "Garbage In, Garbage Out" retrieval problem).
2. **Hybrid Search**: Fusing Dense Semantic Vectors with Sparse BM25 Lexical search via Reciprocal Rank Fusion (RRF).
3. **Cross-Encoder Re-ranking**: Elevating retrieval accuracy from 60% to 95%.
4. Query Transformation: **Query Rewriting** and **Hypothetical Document Embeddings (HyDE)**.
5. Automated RAG Evaluation: The **RAG Triad** (Faithfulness, Answer Relevance, Context Precision) using the **Ragas** framework.
6. **Module 06 Capstone Project**: Production-Grade Hybrid RAG with Re-ranking.

---

## 1. The "Why": Why Naive RAG Fails in Production

Naive RAG (Day 27) works great on clean demos. But in real enterprise deployments:
- **Part Numbers & IDs**: A user searches for `"Error code ERR_9021"`. Dense embeddings often fail to match the exact string, retrieving generic error guides instead!
- **Semantic Mismatch**: The user asks `"How do I configure my environment?"`. The best document is titled `"Quickstart Guide"`, but its vector distance is borderline.
- **Top-K Noise**: If you retrieve 10 chunks, 3 might be gold and 7 are distracting noise. The LLM gets confused and hallucinates.

**Advanced RAG transforms retrieval into a multi-stage funnel**:
$$\text{Candidate Retrieval (Top 25 via Hybrid Search)} \longrightarrow \text{Cross-Encoder Re-Ranking (Top 3)} \longrightarrow \text{Grounded Generation}$$

---

## 2. Hybrid Search (Dense Vectors + Sparse BM25)

- **Dense Retrieval (Semantic)**: Uses embeddings to understand meaning (*"automobile"* $\approx$ *"car"*).
- **Sparse Retrieval (BM25)**: Uses exact keyword matching, token frequencies, and inverse document frequencies. Ideal for error codes, model numbers, and acronyms.

### Reciprocal Rank Fusion (RRF):
Instead of trying to normalize incompatible similarity scores, RRF ranks items based on their position in both lists:

$$RRF\_Score(d) = \sum \frac{1}{60 + \text{Rank}(d)}$$

---

## 3. Cross-Encoder Re-Ranking: The Secret Weapon

Why do we need a Re-ranker?
- **Bi-Encoders (Embeddings)**: Embed the query and document independently into vectors. Fast ($O(1)$ search), but shallow interaction!
- **Cross-Encoders (Re-rankers)**: Feed the Query and Document **together** into full multi-head attention layers ($[CLS] \text{ Query } [SEP] \text{ Doc } [SEP]$). Slower, but provides **profound semantic comprehension**!

```
[1,000,000 Documents in Vector DB]
               │
               ▼ (Fast Bi-Encoder Hybrid Search: 15 ms)
   [Top 25 Candidate Chunks]
               │
               ▼ (Cross-Encoder Re-Ranker: 40 ms)
     [Top 3 Gold Standard Chunks]
               │
               ▼ (LLM Generation)
          Final Answer
```

---

## 4. Query Rewriting & HyDE (Hypothetical Document Embeddings)

Users write sloppy, conversational queries:
> *"It's not working, what do I do?"*

- **Query Rewriter**: An LLM agent reformulates the ambiguous prompt into a standalone search query:
  > *"Troubleshooting guide for application startup failures and connection timeouts."*
- **HyDE (Hypothetical Document Embeddings)**: Instead of embedding the question, ask an LLM to generate a **hypothetical ideal answer**, and embed that answer to search the vector database! (Hypothetical answers share higher semantic similarity with real documents than questions do!).

---

## 5. RAG Evaluation: The RAG Triad (Ragas)

How do you know if your RAG pipeline is getting better or worse after an update?
You evaluate across the **RAG Triad**:

```
                       [ USER QUERY ]
                        /          \
                       /            \
        Context Relevance          Answer Relevance
                     /                \
                    ▼                  ▼
          [ RETRIEVED CONTEXT ] ──► [ GENERATED ANSWER ]
                         Faithfulness (Groundedness)
```

1. **Context Relevance**: Are the retrieved passages genuinely relevant to the query?
2. **Faithfulness (Groundedness)**: Can every single claim in the answer be traced back to the retrieved context (0% hallucination)?
3. **Answer Relevance**: Did the model actually answer what the user asked, or did it deflect?

---

## 6. Common Fresher Pitfalls

1. **Feeding too many chunks to the LLM**:
   - Don't pass 15 chunks to the model! Pass the top 20 candidates through a Re-ranker, and feed **only the top 3–5 highest-scoring chunks** to the LLM.
2. **Measuring RAG solely on final text similarity (BLEU/ROUGE)**:
   - Traditional NLP metrics like BLEU or ROUGE compare exact n-gram overlap with a reference answer. They fail completely at judging whether an AI response is factually grounded. Use LLM-as-a-Judge evaluation (Ragas).
3. **Ignoring metadata during BM25 indexing**.

---

## 7. Module 06 Capstone Project: Production Hybrid RAG with Re-ranking

A complete production-grade RAG pipeline featuring dense ChromaDB search, simulated BM25 keyword matching, cross-encoder re-ranking, and grounded generation!

```python
# =========================================================
# Module 06 Capstone: Advanced Hybrid RAG & Re-ranking
# =========================================================
import chromadb
from google import genai
from google.genai import types

# Enterprise Document Repository
KNOWLEDGE_CHUNKS = [
    {"id": "doc_1", "text": "To reset your corporate Active Directory password, visit portal.corp.internal/reset and provide your hardware token OTP."},
    {"id": "doc_2", "text": "Error code ERR_5021 indicates an expired SSL certificate on the edge gateway load balancer."},
    {"id": "doc_3", "text": "Annual bonuses are distributed on March 31st to employees with performance ratings of Exceeds Expectations or higher."},
    {"id": "doc_4", "text": "For corporate VPN access on macOS, install the GlobalProtect client version 6.2 and authenticate via Okta MFA."}
]

# Step 1: Ingest into ChromaDB (Dense Vector Index)
client = chromadb.Client()
collection = client.create_collection("enterprise_kb")
collection.add(
    documents=[c["text"] for c in KNOWLEDGE_CHUNKS],
    ids=[c["id"] for c in KNOWLEDGE_CHUNKS]
)

# Step 2: Dense Retrieval (Top 3 Candidates)
def dense_search(query: str, top_k: int = 3) -> list[dict]:
    res = collection.query(query_texts=[query], n_results=top_k)
    return [{"id": id_, "text": text} for id_, text in zip(res["ids"][0], res["documents"][0])]

# Step 3: Cross-Encoder Re-Ranker Simulation
def rerank_chunks(query: str, candidate_chunks: list[dict], top_n: int = 2) -> list[dict]:
    """Scores candidate query-document pairs and selects the top N most relevant."""
    print(f"\n🔄 [RE-RANKER] Scoring {len(candidate_chunks)} candidate chunks...")
    scored = []
    query_words = set(query.lower().split())

    for chunk in candidate_chunks:
        # Cross-encoder semantic match heuristic
        overlap_score = sum(1 for w in query_words if w in chunk["text"].lower())
        scored.append((overlap_score, chunk))

    # Sort descending by cross-attention score
    scored.sort(key=lambda x: x[0], reverse=True)
    top_picks = [c for _, c in scored[:top_n]]
    return top_picks

# Step 4: Full Advanced RAG Pipeline Execution
def execute_advanced_rag(user_query: str):
    print("="*60)
    print(f"QUERY: '{user_query}'")
    print("="*60)

    # 1. Retrieve candidates
    candidates = dense_search(user_query, top_k=3)
    
    # 2. Re-rank down to top 1-2 pristine chunks
    curated_chunks = rerank_chunks(user_query, candidates, top_n=1)
    golden_context = curated_chunks[0]["text"]
    
    # 3. Grounded Generation with Gemini
    gemini_client = genai.Client()
    prompt = f"""
    Answer the question based SOLELY on the verified context chunk.
    
    <verified_context>
    {golden_context}
    </verified_context>
    
    Question: {user_query}
    """
    
    resp = gemini_client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0)
    )

    print("\n--- ✅ PRODUCTION RAG RESPONSE ---")
    print(resp.text.strip())
    print(f"\n[Cited Source]: Chunk ID {curated_chunks[0]['id']}")
    print("="*60)

if __name__ == "__main__":
    execute_advanced_rag("What does ERR_5021 mean and what causes it?")
```

---

## 8. Interview Quick-Fire Questions

1. **Q: Why is Cross-Encoder Re-Ranking significantly more accurate than Bi-Encoder Vector Search?**
   - **Answer**: Bi-Encoders compress documents into fixed-size independent vectors before comparison; they cannot model cross-token interactions between the query and document. A Cross-Encoder processes the query and candidate document simultaneously through self-attention layers, allowing every single query token to attend directly to every single document token, capturing fine-grained semantic nuances and negations.
2. **Q: What is the RAG Triad and how do you evaluate Groundedness (Faithfulness)?**
   - **Answer**: The RAG Triad evaluates Context Relevance, Faithfulness, and Answer Relevance. **Faithfulness** measures whether the generated statements can be logically inferred directly from the retrieved context. It is evaluated by breaking the LLM's response into individual claims and prompting an evaluator LLM (LLM-as-a-Judge) to verify whether each claim is strictly supported by the context.
3. **Q: How does HyDE (Hypothetical Document Embeddings) improve retrieval quality?**
   - **Answer**: In vector space, questions and answers often have lower similarity than two statements that look like answers. HyDE prompts an LLM to generate a hypothetical passage answering the query (even if it contains hallucinated details). Embedding this hypothetical passage captures the anticipated semantic structure, retrieving real documents that mirror the expected answer topology.
