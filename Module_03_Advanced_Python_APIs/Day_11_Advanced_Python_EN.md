# Day 11: Advanced Python Concepts (Context Managers, Regex & Memory)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Building custom Context Managers with the `__enter__` and `__exit__` protocol, and `@contextlib.contextmanager`.
2. Mastering **Regular Expressions (`re`)** for parsing logs, emails, and sanitizing LLM outputs.
3. How Python manages memory under the hood: **Reference Counting** and the **Cyclic Garbage Collector (gc)**.
4. Clean code standards: **PEP 8**, modern type hinting (`typing` module), and linters.

---

## 1. The "Why": Professional Production Hygiene

Anyone can write code that works on their own machine once. But senior engineers write code that:
- Never leaks database connections or file handles (**Custom Context Managers**).
- Parses semi-structured text without writing 50 clumsy `if-elif` string checks (**Regex**).
- Avoids memory leaks during long-running background AI processes (**Memory Management**).
- Can be read and maintained by teammates 2 years later (**PEP 8 & Type Hints**).

---

## 2. Custom Context Managers (`contextlib`)

You already know `with open(...) as f:`. But what if you want to create your own automatic cleanup mechanism (e.g., measuring execution time, acquiring a database lock, or temporarily overriding settings)?

### Approach A: The Class-Based Protocol (`__enter__` & `__exit__`)
```python
class DatabaseTransaction:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def __enter__(self):
        print(f"🔒 [TRANSACTION START] Locking table in '{self.db_name}'...")
        return self  # The object bound to the 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"❌ [ROLLBACK] Transaction failed due to: {exc_val}. Rolling back state!")
        else:
            print("✅ [COMMIT] Transaction committed successfully to disk.")
        print("🔓 [TRANSACTION END] Table lock released.\n")
        return False  # Propagate exceptions if any

# Usage:
with DatabaseTransaction("ProductionPostgres") as tx:
    print("  Writing customer order #9821...")
```

### Approach B: The Elegant Generator Method (`@contextmanager`)
```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield  # Code inside the 'with' block executes here!
    finally:
        elapsed = time.perf_counter() - start
        print(f"⏱️ [{label}] Elapsed time: {elapsed:.4f} seconds")

with timer("Vector Embedding Generation"):
    time.sleep(0.3)  # Simulating task
```

---

## 3. Regular Expressions (`re`) for Data Extraction

In AI and data pipelines, models and external APIs return messy strings containing dates, emails, and JSON fragments. Regex is your precision scalpel.

```python
import re

log_payload = """
2026-10-15 14:32:01 [ALERT] User id=usr_9812 email=rahul.tech@company.in failed MFA from IP 192.168.1.45.
2026-10-15 14:33:10 [INFO] User id=usr_4402 email=priya_ai@startup.org logged in from IP 10.0.0.99.
"""

# 1. re.findall(): Extract all email addresses
# Pattern: non-whitespace characters followed by @ and a domain
email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
emails = re.findall(email_pattern, log_payload)
print("Extracted Emails:", emails)

# 2. re.search() with Named Groups (?P<name>...)
ip_pattern = r"IP\s+(?P<ip_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
match = re.search(ip_pattern, log_payload)
if match:
    print("First Suspicious IP:", match.group("ip_address"))

# 3. re.sub(): Redacting sensitive data
sanitized_log = re.sub(r"usr_\d+", "usr_[MASKED]", log_payload)
print("Sanitized Log Preview:\n", sanitized_log.strip())
```

---

## 4. How Python Manages Memory (Reference Counting & GC)

Unlike C++, you don't call `free()` or `malloc()`. Unlike Java, Python primarily uses **Reference Counting**, backed up by a cyclic Garbage Collector.

1. **Reference Count**: Every object in Python tracks how many variables point to it.
2. When an object's reference count drops to **0**, Python frees the memory **immediately**!
3. **Circular Reference Problem**: If Object A points to Object B, and Object B points to Object A, their counts never reach zero. Python's cyclic `gc` module periodically scans for these reference cycles and sweeps them away.

```python
import sys
import gc

# Creating an object in memory
x = ["AI Model Weights", 4096]
print("Initial Refcount:", sys.getrefcount(x))  # Typically 2 (x + internal getrefcount arg)

y = x  # Creating a second reference
print("Refcount after assigning y:", sys.getrefcount(x))  # 3

del y  # Removing reference
print("Refcount after deleting y:", sys.getrefcount(x))   # 2

# Manually triggering garbage collection if dealing with huge tensors
gc.collect()
```

---

## 5. Modern Type Hints & Clean Code (PEP 8)

Starting with Python 3.9+, you can use native collection types for type hinting without importing `List`, `Dict`, `Tuple` from `typing`:

```python
from typing import Optional, Union

# Clean modern function signature
def generate_rag_response(
    query: str,
    top_k: int = 5,
    filters: Optional[dict[str, str]] = None
) -> dict[str, Union[str, float]]:
    """Type annotations communicate developer intent and enable IDE autocompletion!"""
    return {
        "query": query,
        "confidence_score": 0.94
    }
```

---

## 6. Common Fresher Pitfalls

1. **The ReDoS Trap (Regular Expression Denial of Service)**:
   - Writing catastrophic backtracking regexes (like `(a+)+$`) on untrusted user input can lock the CPU at 100% indefinitely. Keep regexes simple and bounded.
2. **Supplying exceptions incorrectly in `__exit__`**:
   - If your `__exit__` method returns `True`, it **suppresses** any exception that occurred inside the `with` block. If it returns `False` (or `None`), the exception bubbles up properly.
3. **Relying on `del` to immediately free memory**:
   - `del variable` only removes the variable name and decrements the reference count. It only frees the memory if no other references exist!

---

## 7. Daily Hands-On Lab

### 🧪 Exercise: Build a "Safe File Lock & PII Redaction Pipeline"
**Scenario**: In AI training pipelines, raw datasets often contain Personally Identifiable Information (PII: emails, phone numbers, credit card numbers). Build a custom context manager that locks a file, extracts and redacts PII using regex, and safely writes the sanitized file.

```python
# ==========================================
# Day 11 Lab: PII Redactor with Context Manager
# ==========================================
import re
from contextlib import contextmanager

RAW_DOC = """
CONFIDENTIAL CUSTOMER RECORD
Customer Name: Arvind Swaminathan
Email Address: arvind.s@techinnovate.com
Phone Number: +91-9845012345
Credit Card: 4532-8921-9031-4122
Note: Requested credit limit hike of INR 2,00,000.
"""

@contextmanager
def file_audit_context(pipeline_name: str):
    print(f"--- 🛡️ Starting Secure Pipeline: '{pipeline_name}' ---")
    metrics = {"pii_scrubbed": 0}
    try:
        yield metrics
    finally:
        print(f"--- 🏁 Pipeline '{pipeline_name}' Completed. Total Scrubbed: {metrics['pii_scrubbed']} ---\n")

def scrub_pii(text: str, metrics: dict) -> str:
    # 1. Scrub Credit Cards (\d{4}-\d{4}-\d{4}-\d{4})
    cc_pattern = r"\b\d{4}-\d{4}-\d{4}-\d{4}\b"
    text, cc_count = re.subn(cc_pattern, "[CARD-REDACTED]", text)
    
    # 2. Scrub Indian Phone Numbers (+91-XXXXX or 10 digits)
    phone_pattern = r"(\+91[-\s]?)?[6-9]\d{9}|\+91-\d{10}"
    text, phone_count = re.subn(phone_pattern, "[PHONE-REDACTED]", text)
    
    # 3. Scrub Emails
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    text, email_count = re.subn(email_pattern, "[EMAIL-REDACTED]", text)

    metrics["pii_scrubbed"] = cc_count + phone_count + email_count
    return text

# Run the Secure Scrubbing Pipeline
with file_audit_context("DataLake Ingestion Sanitizer") as audit:
    sanitized_text = scrub_pii(RAW_DOC, audit)
    print("Sanitized Output:\n", sanitized_text.strip())
```

---

## 8. Interview Quick-Fire Questions

1. **Q: How does Python's Garbage Collection work?**
   - **Answer**: Python primarily relies on **Reference Counting**. Every object maintains a count of references pointing to it. When that count drops to 0, its memory is deallocated instantly. To resolve **cyclic references** (where objects reference each other and their count never hits 0), Python employs a generational cyclic garbage collector (`gc` module) that detects and frees circular memory topologies.
2. **Q: What is the difference between `re.search()` and `re.match()`?**
   - **Answer**: `re.match()` checks for a match **only at the beginning** of the string. `re.search()` scans through the **entire string** to find the first occurrence of the pattern.
3. **Q: What happens if an exception is raised inside a `@contextmanager` generator?**
   - **Answer**: The exception is re-raised at the point where `yield` was called inside the generator. Therefore, you should always wrap the `yield` statement in a `try...finally` block to ensure your cleanup code in the `finally` clause always executes!
