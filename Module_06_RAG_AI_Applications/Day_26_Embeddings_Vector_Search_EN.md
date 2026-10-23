# Day 26: Embeddings & Vector Databases (ChromaDB & FAISS)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. What **Text Embeddings** represent: Dense semantic vectors in high-dimensional space.
2. Vector Similarity Metrics: **Cosine Similarity**, **Dot Product**, and **Euclidean Distance ($L2$)**.
3. Why traditional SQL `LIKE '%keyword%'` fails completely on semantic meaning.
4. Working with local Vector Databases: **ChromaDB** and **FAISS** (Facebook AI Similarity Search).
5. Combining vector similarity with **Metadata Filtering** for production searches.

---

## 1. The "Why": Why SQL Cannot Search Like a Human

Suppose a user searches your company HR database for:
> *"How do I take time off for my wedding?"*

- A standard SQL query `SELECT * FROM policies WHERE content LIKE '%wedding%'` returns **0 results** because the HR manual calls it *"Annual Marriage Leave Policy"*!
- Keyword search is brittle because it searches for matching **letters**, not **concepts**.

**Embeddings solve this by converting meaning into geometry**:
- The vector for *"take time off"* is physically close to *"leave entitlement"*.
- The vector for *"wedding"* is physically close to *"marriage"*.

---

## 2. Vector Similarity Metrics: Which One When?

```
         Vector A                     Vector A
           ▲                            ▲
           │ \ θ (Angle)                │
           │  \                         │  Distance (L2)
           │   \                        │ ◄──────────► Vector B
           └────► Vector B              └────────────────────►
        Cosine Similarity                   Euclidean (L2)
```

| Metric | Formula | What It Measures | When to Use |
| :--- | :--- | :--- | :--- |
| **Cosine Similarity** | $\frac{A \cdot B}{\|A\| \|B\|}$ | **Angle** between vectors (ignoring length). Range: $[-1, 1]$. | **Default choice for text & NLP embeddings!** |
| **Dot Product** | $A \cdot B = \sum A_i B_i$ | Angle **AND** Magnitude. | When vectors are already normalized ($\|A\|=1$). (Fastest computation!) |
| **Euclidean Distance ($L2$)** | $\sqrt{\sum (A_i - B_i)^2}$ | Straight-line spatial distance. | Clustering algorithms (K-Means), geometric coordinates. |

---

## 3. High-Performance Vector Databases: ChromaDB

**ChromaDB** is the developer-favorite open-source vector store for prototyping and production RAG.

### Step 1: Install ChromaDB
```bash
pip install chromadb
```

### Step 2: Ingest Documents & Query Semantically
```python
import chromadb
from chromadb.utils import embedding_functions

# 1. Initialize in-memory or persistent client
client = chromadb.Client()

# 2. Create a Collection (equivalent to a SQL Table)
# By default, Chroma uses all-MiniLM-L6-v2 to automatically generate embeddings!
collection = client.create_collection(name="company_hr_policies")

# 3. Add Documents with Metadata and Unique IDs
documents = [
    "Employees are entitled to 20 days of paid annual vacation each calendar year.",
    "The IT department provides MacBook Pros with 32GB RAM for senior engineers.",
    "Special marriage leave of 5 consecutive days is granted upon wedding registration.",
    "Health insurance covers inpatient hospitalization up to ₹5,00,000 per family member."
]

metadatas = [
    {"category": "leave", "author": "HR"},
    {"category": "hardware", "author": "IT"},
    {"category": "leave", "author": "HR"},
    {"category": "benefits", "author": "HR"}
]

ids = ["doc_01", "doc_02", "doc_03", "doc_04"]

collection.add(documents=documents, metadatas=metadatas, ids=ids)
print(f"✅ Ingested {collection.count()} documents into ChromaDB.\n")

# 4. Semantic Search: Query without exact keyword matches!
query = "I am getting married next month, can I take extra days off?"
results = collection.query(
    query_texts=[query],
    n_results=2,  # Top 2 most relevant chunks
    where={"category": "leave"}  # Metadata filtering!
)

print(f"Search Query: '{query}'\n")
for idx, (doc, dist) in enumerate(zip(results["documents"][0], results["distances"][0])):
    print(f"Result #{idx+1} (Distance: {dist:.4f}):")
    print(f"  Content: {doc}\n")
```

---

## 4. Ultra-Fast Large-Scale Search with Meta's FAISS

When scaling to **10 million vectors**, standard Python loops choke. **FAISS** (Facebook AI Similarity Search) compiles down to C++ with AVX-512 and GPU optimizations.

```python
import numpy as np
import faiss

# Vector dimension (e.g. 4 numbers for demo; in reality 768 or 1536)
dimension = 4
num_vectors = 1000

# Generate 1,000 random document vectors
np.random.seed(42)
document_vectors = np.random.random((num_vectors, dimension)).astype("float32")

# 1. Build the FAISS Flat Index (Exact L2 Search)
index = faiss.IndexFlatL2(dimension)
index.add(document_vectors)
print(f"FAISS Index ready with {index.ntotal} vectors.")

# 2. Query with a new vector
query_vector = np.random.random((1, dimension)).astype("float32")
top_k = 3
distances, indices = index.search(query_vector, top_k)

print("\nTop 3 Nearest Document Indices:", indices[0])
print("L2 Distances to Query:", distances[0])
```

---

## 5. Common Fresher Pitfalls

1. **Mixing Embedding Models**:
   - ⚠️ **The Fatal Mistake**: If you embed your documents using OpenAI's `text-embedding-3-small` (1536 dims), you **CANNOT** search them using Google Gemini's embedding model! Vectors from different models inhabit completely different dimensional geometries. Always use the **exact same model** for both ingestion and querying!
2. **Ignoring Metadata**:
   - Searching across an entire company's documents without metadata filtering (e.g. `department: finance`) will return irrelevant engineering docs that happen to share generic words.
3. **Confusing Distance with Similarity**:
   - In Cosine **Similarity**, 1.0 is identical. In Cosine **Distance**, 0.0 is identical! Know what your database returns.

---

## 6. Daily Hands-On Lab

### 🧪 Exercise: Build a Semantic Customer Support FAQ Matcher
**Scenario**: Customers submit vague questions (*"my card was charged twice"*). Match their question against the company's knowledge base using Cosine Similarity, return the best resolution, and reject queries if the distance is too high (preventing false matches).

```python
# =========================================================
# Day 26 Lab: Semantic Support FAQ Matcher with ChromaDB
# =========================================================
import chromadb

client = chromadb.Client()
faq_collection = client.create_collection(
    name="ecommerce_faqs",
    metadata={"hnsw:space": "cosine"}  # Explicitly configure Cosine Space!
)

# Knowledge Base Records
faq_entries = [
    {"id": "faq_01", "q": "How to request a refund for a damaged item?", "ans": "Go to Orders > Return Item and upload photos within 48 hours."},
    {"id": "faq_02", "q": "Why was I billed multiple times for a single order?", "ans": "Duplicate charges are pending authorization holds released in 3-5 business days."},
    {"id": "faq_03", "q": "How do I change my shipping address?", "ans": "Address can be modified in Orders tab if item has not dispatched."},
]

faq_collection.add(
    documents=[entry["q"] for entry in faq_entries],
    metadatas=[{"answer": entry["ans"]} for entry in faq_entries],
    ids=[entry["id"] for entry in faq_entries]
)

def resolve_customer_query(customer_question: str, max_distance_threshold: float = 0.5):
    results = faq_collection.query(
        query_texts=[customer_question],
        n_results=1
    )
    
    distance = results["distances"][0][0]
    matched_q = results["documents"][0][0]
    answer = results["metadatas"][0][0]["answer"]

    print("="*55)
    print(f"Customer Query: '{customer_question}'")
    print(f"Closest FAQ   : '{matched_q}'")
    print(f"Distance Score: {distance:.4f}")

    if distance > max_distance_threshold:
        print("⚠️ ROUTING TO HUMAN: No matching FAQ found with high confidence.")
    else:
        print(f"✅ AUTO-RESOLUTION: {answer}")
    print("="*55)

# Test Match 1: Semantic duplicate billing
resolve_customer_query("I see two identical debit deductions on my bank statement for one purchase.")

# Test Match 2: Irrelevant query (should be rejected)
resolve_customer_query("What is the recipe for chocolate chip cookies?")
```

---

## 7. Interview Quick-Fire Questions

1. **Q: What is the Curse of Dimensionality and how does it relate to Vector Embeddings?**
   - **Answer**: As vector dimensionality increases (e.g. to 1536 or 3072 dimensions), the volume of the space grows exponentially, making data points extremely sparse and causing Euclidean distance to lose its discriminatory power (all points appear almost equidistant). In high dimensions, Cosine Similarity (measuring angle rather than distance) is preferred.
2. **Q: What is HNSW (Hierarchical Navigable Small World) in vector databases?**
   - **Answer**: HNSW is a graph-based indexing algorithm used by modern vector databases (Pinecone, Chroma, Milvus) for Approximate Nearest Neighbor (ANN) search. It organizes vectors into a multi-layered skip-list graph, allowing queries to search millions of vectors in logarithmic $O(\log N)$ time instead of slow linear $O(N)$ brute-force scans.
3. **Q: Why can't you compare embeddings from two different models?**
   - **Answer**: Each embedding model is trained with a distinct neural architecture, tokenizer vocabulary, and loss function, mapping concepts into its own unique coordinate latent space. Comparing vectors across different models is like comparing latitude/longitude GPS coordinates with pixel coordinates on a TV screen—they share no common geometric frame of reference.
