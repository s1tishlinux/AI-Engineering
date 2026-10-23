# Day 04: Strings & Functions

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Modern Python string manipulation (cleaning, splitting, joining, f-strings).
2. The philosophy of **DRY (Don't Repeat Yourself)** using modular functions.
3. Function parameters: Positional, Keyword, Default, and Arbitrary args (`*args`, `**kwargs`).
4. Variable Scope and the **LEGB** rule (Local, Enclosing, Global, Built-in).
5. Anonymous functions: **Lambda expressions** and when to use them.

---

## 1. The "Why": Strings and Reusable Logic

In modern software (and especially GenAI/LLM pipelines):
- **Strings are the currency of AI**: Every prompt sent to an LLM, every document retrieved, and every response parsed is a string. If you cannot slice, sanitize, and format strings, you cannot build AI applications!
- **Functions are Lego bricks**: Writing 500 lines of flat code without functions makes software unmaintainable and buggy. Functions allow you to test, reuse, and compose complex logic cleanly.

---

## 2. String Manipulation Mastery

Strings in Python are **immutable** (any modification returns a brand-new string).

```python
raw_prompt = "   ### USER QUESTION: How to Train an LLM?   \n"

# 1. Stripping whitespaces
clean_prompt = raw_prompt.strip()
print(f"Stripped: '{clean_prompt}'")

# 2. Case conversions
print("Upper:", clean_prompt.upper())
print("Lower:", clean_prompt.lower())

# 3. Splitting and Joining (Crucial for Tokenization & NLP)
sentence = "python,fastapi,docker,langchain,chroma"
tags = sentence.split(",")                # Converts string to list
print("Tags List:", tags)

reconstructed = " | ".join(tags)          # Joins list back to string
print("Reconstructed:", reconstructed)

# 4. Checking prefixes/suffixes
filename = "invoice_2026_march.pdf"
print("Is PDF?", filename.endswith(".pdf"))
print("Is Invoice?", filename.startswith("invoice_"))

# 5. Modern f-strings (with formatting specifiers)
cpu_usage = 84.5678
active_users = 14250
print(f"Server Load: {cpu_usage:.1f}% | Active Sessions: {active_users:,}")
```

---

## 3. Defining & Calling Functions

### The Golden Rule: Single Responsibility
A function should do **one thing and do it well**.

```python
# Function Definition
def calculate_tax(income: float, tax_rate: float = 0.18) -> float:
    """Calculates tax on a given income. Defaults to 18% GST."""
    calculated_tax = income * tax_rate
    return calculated_tax

# Calling the function
service_bill = 5000.0
# Using default tax_rate
tax_default = calculate_tax(service_bill)
# Overriding default tax_rate
tax_custom = calculate_tax(service_bill, tax_rate=0.05)

print(f"Default Tax (18%): ₹{tax_default}")
print(f"Custom Tax (5%)  : ₹{tax_custom}")
```

---

## 4. Function Arguments: Positional, Keyword, `*args`, `**kwargs`

Freshers often get confused when seeing `*args` and `**kwargs` in open-source AI libraries (like LangChain or PyTorch). Here is the crystal-clear breakdown:

```python
# 1. *args (Arbitrary Positional Arguments) -> Packed into a TUPLE
def calculate_cart_total(*prices):
    total = sum(prices)
    return total

print("Cart 1 Total:", calculate_cart_total(100, 250, 400))  # 750
print("Cart 2 Total:", calculate_cart_total(50, 20))         # 70

# 2. **kwargs (Arbitrary Keyword Arguments) -> Packed into a DICTIONARY
def create_ai_agent(agent_name, model="gemini-1.5-pro", **config):
    print(f"\nInitializing Agent: '{agent_name}' with Model: {model}")
    for key, value in config.items():
        print(f"  - Config Setting [{key}]: {value}")

create_ai_agent(
    "CodeReviewer",
    temperature=0.2,
    max_tokens=2048,
    memory_type="vector_store",
    verbose=True
)
```

---

## 5. Variable Scope & The LEGB Rule

Where does Python look for a variable? It follows the **LEGB** hierarchy:
1. **L**ocal: Inside the current function.
2. **E**nclosing: Inside any outer/parent function (closures).
3. **G**lobal: At the top level of the `.py` script.
4. **B**uilt-in: In Python's built-in namespace (`print`, `len`, `int`).

```python
# Global Scope
company_name = "TechIn AI Labs"

def generate_badge(employee_name):
    # Local Scope
    department = "Engineering"
    badge_info = f"[{company_name}] {employee_name} - {department}"
    return badge_info

print(generate_badge("Satish"))
# print(department) # ❌ NameError: name 'department' is not defined (it died with the function!)
```

---

## 6. Lambda Functions (Anonymous Quick Functions)

A lambda is a small, one-line function without a name.
**Syntax**: `lambda arguments: expression`

```python
# Standard Function
def double(x):
    return x * 2

# Equivalent Lambda
double_lambda = lambda x: x * 2
print(double_lambda(5))  # 10

# Where Lambda shines: Sorting complex data
students = [
    {"name": "Sneha", "gpa": 8.9},
    {"name": "Arjun", "gpa": 9.4},
    {"name": "Kavya", "gpa": 7.8}
]

# Sort students by GPA in descending order
sorted_by_gpa = sorted(students, key=lambda s: s["gpa"], reverse=True)
print("Top Students:", sorted_by_gpa)
```

---

## 7. Common Fresher Pitfalls

1. **The Mutable Default Argument Trap** (⚠️ Number 1 Python Interview Trap):
   ```python
   # ❌ DANGEROUS: Default list is created ONCE at function definition!
   def add_item(item, basket=[]):
       basket.append(item)
       return basket

   print(add_item("Apple"))   # ['Apple']
   print(add_item("Banana"))  # ['Apple', 'Banana'] -> Unexpected shared state!

   # ✅ THE CORRECT PATTERN:
   def add_item_safe(item, basket=None):
       if basket is None:
           basket = []
       basket.append(item)
       return basket
   ```
2. **Forgetting the `return` statement**:
   - If a function has no `return`, it implicitly returns `None`.

---

## 8. Daily Hands-On Lab

### 🧪 Exercise: Build a "Prompt Cleaner & Token Estimator"
**Scenario**: In LLM applications, user input often contains messy whitespace and formatting issues. Build a utility function to sanitize user text, redact sensitive terms, and estimate LLM token cost (~1 token ≈ 4 characters in English).

```python
# ==========================================
# Day 4 Lab: LLM Prompt Sanitizer & Estimator
# ==========================================

BANNED_WORDS = {"password", "secret_key", "aadhaar", "ssn"}

def sanitize_prompt(raw_text: str) -> str:
    """Cleans extra whitespace, normalizes tabs/newlines."""
    cleaned = " ".join(raw_text.strip().split())
    return cleaned

def redact_sensitive_info(text: str, sensitive_words: set) -> str:
    """Masks confidential keywords with [REDACTED]."""
    words = text.split()
    redacted_words = [
        "[REDACTED]" if word.lower().strip(".,!?") in sensitive_words else word
        for word in words
    ]
    return " ".join(redacted_words)

def estimate_tokens_and_cost(text: str, cost_per_1k_tokens_usd: float = 0.0015) -> dict:
    """Estimates token count (~4 chars = 1 token) and API call cost."""
    char_count = len(text)
    estimated_tokens = max(1, char_count // 4)
    estimated_cost_usd = (estimated_tokens / 1000) * cost_per_1k_tokens_usd
    estimated_cost_inr = estimated_cost_usd * 83.0

    return {
        "characters": char_count,
        "estimated_tokens": estimated_tokens,
        "cost_usd": f"${estimated_cost_usd:.6f}",
        "cost_inr": f"₹{estimated_cost_inr:.4f}"
    }

# Test the pipeline
user_input = "   Please help me verify my password   and process the payroll for employee 901.   "

print("Original Input :", repr(user_input))
clean_step = sanitize_prompt(user_input)
safe_step = redact_sensitive_info(clean_step, BANNED_WORDS)
metrics = estimate_tokens_and_cost(safe_step)

print("Sanitized Input:", safe_step)
print("Cost Metrics   :", metrics)
```

---

## 9. Interview Quick-Fire Questions

1. **Q: Explain the mutable default argument bug in Python.**
   - **Answer**: In Python, default arguments are evaluated only once when the function is defined, not every time it is called. If you use a mutable object (like a list or dict) as a default argument, all invocations of that function will mutate and share the exact same object. Always use `None` as the default value and instantiate the list inside the function body.
2. **Q: What is the LEGB rule?**
   - **Answer**: LEGB defines Python's variable name lookup order: Local (inside current function), Enclosing (outer enclosing functions), Global (module level), and Built-in (Python's predefined functions like `len`).
3. **Q: What is the difference between `*args` and `**kwargs`?**
   - **Answer**: `*args` allows a function to accept any number of positional arguments which are received inside the function as a Tuple. `**kwargs` allows accepting any number of keyword arguments which are received as a Dictionary.
