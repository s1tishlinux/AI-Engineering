# Day 12: Concurrency (Asyncio) & Data Validation (Pydantic)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Concurrency Models: **Multithreading** vs **Multiprocessing** vs **Asyncio** (and the Global Interpreter Lock - GIL).
2. The Async Mental Model: Event Loop, Coroutines, `async` and `await`.
3. Running concurrent tasks in parallel using `asyncio.gather()`.
4. Modern Data Modeling: Standard `@dataclass` vs Production **Pydantic (`BaseModel`)**.
5. Schema validation, type coercion, and custom field validators.

---

## 1. The "Why": Building High-Throughput AI Microservices

Modern AI applications do **not** do heavy CPU calculations in Python—the GPU does that.
Instead, your Python backend spends **95% of its time waiting**:
- Waiting for the OpenAI or Gemini API to stream tokens (1,500 ms).
- Waiting for ChromaDB / Pinecone to return vector chunks (200 ms).
- Waiting for PostgreSQL to fetch user metadata (50 ms).

If your server runs synchronously, 1 user waiting 2 seconds blocks all other users!
**With `asyncio`, your single-threaded Python server can handle 10,000 concurrent user requests effortlessly while waiting for I/O.**

---

## 2. Choosing Concurrency: Threads vs Processes vs Asyncio

| Model | Mechanism | Best For | GIL Impact? |
| :--- | :--- | :--- | :--- |
| **Multiprocessing** | Multiple separate OS processes (separate memory) | **CPU-bound tasks**: Video rendering, model training, heavy matrix math | Bypasses the GIL entirely |
| **Multithreading** | Multiple threads sharing one process memory | **Legacy I/O-bound tasks**: File downloads, disk reads | Limited by GIL (1 thread at a time) |
| **Asyncio** | Single thread with cooperative Event Loop | **Modern High-Concurreny I/O**: Web servers, API calls, chat streams | No GIL contention; ultra-lightweight |

### The Restaurant Analogy:
- **Synchronous**: 1 waiter takes Order 1, goes to the kitchen, stands staring at the oven until the pizza is baked, serves Order 1, and only then talks to Customer 2!
- **Asyncio (Event Loop)**: 1 waiter takes Order 1, submits the ticket to the kitchen, immediately attends Customer 2 (`await`), and serves Customer 1 whenever the kitchen bell rings!

---

## 3. Asyncio, `async` and `await`

- `async def`: Defines a **Coroutine** (a pause-able function).
- `await`: Pauses execution of the current coroutine until the awaited task completes, yielding control back to the Event Loop to do other work in the meantime.

```python
import asyncio
import time

# Simulated asynchronous API call
async def fetch_ai_summary(document_id: int) -> str:
    print(f"⏳ [Doc #{document_id}] Sent request to Gemini API...")
    await asyncio.sleep(1.0)  # Non-blocking pause (unlike time.sleep!)
    print(f"✅ [Doc #{document_id}] Received summary response.")
    return f"Summary of Document #{document_id}"

async def main():
    start = time.perf_counter()
    
    # Run 3 API calls concurrently using asyncio.gather()
    results = await asyncio.gather(
        fetch_ai_summary(101),
        fetch_ai_summary(102),
        fetch_ai_summary(103)
    )
    
    elapsed = time.perf_counter() - start
    print("\nResults:", results)
    print(f"Total time elapsed: {elapsed:.2f}s (Synchronous would have taken 3.0s!)")

# Run the event loop
asyncio.run(main())
```

---

## 4. Modern Data Validation: Pydantic vs Dataclasses

Python provides `@dataclass` for lightweight internal data containers, but **Pydantic** is the gold standard for external data validation (FastAPI, LangChain, and OpenAI Structured Outputs are built on Pydantic!).

### Why Pydantic?
Pydantic does **not just annotate types—it strictly parses, coerces, and validates incoming data**:

```python
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class UserRegistrationSchema(BaseModel):
    user_id: int
    username: str = Field(min_length=3, max_length=20, description="Unique handle")
    email: str
    age: int = Field(ge=18, le=100, description="User must be an adult")
    is_premium: bool = False
    registered_at: datetime = Field(default_factory=datetime.now)

    # Custom Business Logic Validator
    @field_validator("username")
    @classmethod
    def no_special_characters(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must contain only letters and numbers.")
        return v.lower()

# Test 1: Valid input with automatic string-to-int coercion
valid_payload = {
    "user_id": 901,
    "username": "KiranKumar26",
    "email": "kiran@company.com",
    "age": "24",  # String "24" automatically converted to integer 24!
    "is_premium": True
}

user = UserRegistrationSchema(**valid_payload)
print("Validated User Object:\n", user.model_dump_json(indent=2))

# Test 2: Invalid input (catches underage violation)
try:
    invalid_payload = {"user_id": 902, "username": "bad", "email": "x@y.com", "age": 16}
    UserRegistrationSchema(**invalid_payload)
except Exception as e:
    print("\n❌ Pydantic Caught Validation Error:\n", e)
```

---

## 5. Common Fresher Pitfalls

1. **Using `time.sleep()` inside an `async def` function**:
   - ⚠️ **The Server Freeze**: `time.sleep(5)` blocks the entire OS thread, completely freezing your event loop! Always use `await asyncio.sleep(5)`.
2. **Forgetting to `await` a coroutine**:
   - Calling `fetch_ai_summary(101)` without `await` does not run the code! It merely returns an unexecuted `<coroutine object>`.
3. **Confusing Python `@dataclass` with Pydantic `BaseModel`**:
   - Dataclasses do NOT validate data at runtime (`User(age="hello")` will happily create an object). Pydantic strictly validates and raises `ValidationError`.

---

## 6. Daily Hands-On Lab

### 🧪 Exercise: Build a Concurrent AI Batch Processor with Pydantic
**Scenario**: An enterprise uploads a batch of text chunks for AI embedding and sentiment analysis. Validate each incoming record schema using Pydantic, and process valid chunks concurrently with `asyncio`.

```python
# =========================================================
# Day 12 Lab: Concurrent AI Ingestion Pipeline with Pydantic
# =========================================================
import asyncio
from pydantic import BaseModel, Field, ValidationError

class DocumentChunk(BaseModel):
    chunk_id: str
    text: str = Field(min_length=10, max_length=500)
    source: str
    priority: int = Field(default=1, ge=1, le=5)

async def simulate_ai_embedding(chunk: DocumentChunk) -> dict:
    """Asynchronously calls an embedding model."""
    print(f"🚀 [EMBEDDING] Processing chunk {chunk.chunk_id} (Priority: {chunk.priority})...")
    await asyncio.sleep(0.5)  # Simulate API latency
    return {
        "chunk_id": chunk.chunk_id,
        "vector_dimensions": 1536,
        "status": "EMBEDDED_SUCCESS"
    }

async def process_batch(raw_items: list[dict]):
    valid_chunks: list[DocumentChunk] = []

    # Step 1: Validate all items using Pydantic
    for raw in raw_items:
        try:
            chunk = DocumentChunk(**raw)
            valid_chunks.append(chunk)
        except ValidationError as err:
            print(f"❌ [VALIDATION FAILED] Dropping bad chunk: {err.errors()[0]['msg']}")

    # Step 2: Concurrently process valid items
    print(f"\nProcessing {len(valid_chunks)} valid chunks concurrently...")
    tasks = [simulate_ai_embedding(c) for c in valid_chunks]
    results = await asyncio.gather(*tasks)

    print("\n--- ✅ BATCH PROCESSING COMPLETED ---")
    for r in results:
        print(f"  • {r['chunk_id']} -> {r['status']}")

# Test the Pipeline
sample_batch = [
    {"chunk_id": "CHK-001", "text": "LangChain provides modular abstraction for LLMs.", "source": "docs.pdf", "priority": 1},
    {"chunk_id": "CHK-002", "text": "Too short", "source": "chat.txt"},  # Validation error (< 10 chars)
    {"chunk_id": "CHK-003", "text": "Retrieval Augmented Generation enhances accuracy.", "source": "kb.md", "priority": 3}
]

asyncio.run(process_batch(sample_batch))
```

---

## 7. Interview Quick-Fire Questions

1. **Q: What is the Python GIL (Global Interpreter Lock)?**
   - **Answer**: The GIL is a mutex lock used by the standard CPython implementation to prevent multiple native OS threads from executing Python bytecodes simultaneously. It exists to simplify memory management and thread safety in C extensions, but it means multi-threaded CPU-bound programs will not utilize multiple CPU cores in Python.
2. **Q: How does `asyncio` achieve concurrency on a single thread?**
   - **Answer**: Through **Cooperative Multitasking** managed by an **Event Loop**. When an asynchronous task encounters an I/O operation (like a network request), it yields control back to the event loop using `await`. The event loop then runs other pending tasks while the operating system waits for the network socket, achieving high throughput without multiple threads.
3. **Q: What is the primary difference between Pydantic and standard Python `dataclasses`?**
   - **Answer**: Python `@dataclass` is primarily a code generator for boilerplate (`__init__`, `__repr__`, `__eq__`) without performing runtime validation. Pydantic is a data parsing and validation library that enforces strict type checking, automatic type coercion, and complex business logic validation at runtime.
