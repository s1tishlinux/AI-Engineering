# Day 09: Functional Programming & Decorators

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Functions as **First-Class Citizens** in Python (passing, returning, and nesting functions).
2. Functional primitives: `map()`, `filter()`, and `functools.reduce()`.
3. **Closures**: Encapsulating state without creating classes.
4. **Decorators**: The `@decorator` syntax, how it modifies function behavior dynamically.
5. The critical role of `@functools.wraps` in preserving docstrings and function names.

---

## 1. The "Why": Clean Cross-Cutting Concerns

In any production backend or AI application, you constantly need to:
- Time how long an LLM call takes (Performance profiling).
- Log incoming arguments (Audit logging).
- Validate if the user is authenticated (Security guards).
- Retry network failures (Fault tolerance).

Without decorators, you would have to copy-paste timing and logging logic into **every single function** in your project.
**Decorators allow you to wrap reusable behavior around any function with a single line: `@timing_decorator`**.

---

## 2. Functions as First-Class Citizens

In Python, functions are objects! You can:
1. Assign them to variables.
2. Pass them as arguments to other functions (**Higher-Order Functions**).
3. Return functions from inside functions.

```python
def shout(text):
    return text.upper() + "!"

def whisper(text):
    return text.lower() + "..."

# Higher-Order Function: Accepts a function as an argument
def format_announcement(formatter_func, message):
    return formatter_func(message)

print(format_announcement(shout, "Deployment complete"))
print(format_announcement(whisper, "Keep this secret"))
```

---

## 3. The Functional Trifecta: `map`, `filter`, `reduce`

```python
from functools import reduce

salaries = [45000, 60000, 85000, 120000, 38000]

# 1. map(): Apply a transformation to EVERY element
hike_10_percent = list(map(lambda s: s * 1.10, salaries))
print("10% Hike:", hike_10_percent)

# 2. filter(): Keep ONLY elements matching a condition (predicate)
high_earners = list(filter(lambda s: s >= 80000, salaries))
print("High Earners (>= 80k):", high_earners)

# 3. reduce(): Aggregate a sequence into a SINGLE scalar value
total_payroll = reduce(lambda acc, s: acc + s, salaries, 0)
print(f"Total Company Payroll: ₹{total_payroll:,}")
```

---

## 4. Closures: Preserving State

A **Closure** occurs when an inner function remembers and has access to variables from its outer enclosing scope, even after the outer function has finished executing!

```python
def make_multiplier(factor: float):
    # Outer function creates a closed environment around 'factor'
    def multiplier(number: float) -> float:
        return number * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print("Double 10:", double(10))  # 20 (remembers factor=2)
print("Triple 10:", triple(10))  # 30 (remembers factor=3)
```

---

## 5. Decorators Demystified

A decorator is simply a function that takes another function as input, wraps extra functionality around it, and returns the modified function.

### The Fundamental Syntax:
```python
import time
from functools import wraps

# Step 1: Define the decorator
def measure_execution_time(func):
    @wraps(func)  # Crucial! Preserves func.__name__ and func.__doc__
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"⏱️ [START] Executing '{func.__name__}'...")
        
        # Execute the original function
        result = func(*args, **kwargs)
        
        duration = time.time() - start_time
        print(f"⏱️ [DONE] '{func.__name__}' completed in {duration:.4f} seconds.\n")
        return result
    return wrapper

# Step 2: Apply the decorator using '@'
@measure_execution_time
def simulate_ai_inference(tokens: int):
    """Simulates an LLM generation delay."""
    time.sleep(0.5)  # Simulate network / GPU latency
    return f"Completed output for {tokens} tokens."

# Step 3: Call the function normally
output = simulate_ai_inference(512)
print("Result:", output)
print("Function Name:", simulate_ai_inference.__name__)  # Preserved as 'simulate_ai_inference'
```

---

## 6. Decorators with Arguments (Advanced Pattern)

What if your decorator needs its own parameters (e.g. `@retry(max_retries=3)`)?
You need **three levels of nested functions**:

```python
def retry(max_attempts: int = 3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️ [Attempt {attempt}/{max_attempts}] Failed with: {e}")
                    if attempt == max_attempts:
                        print("🚨 Max retries reached. Raising error to caller.")
                        raise
        return wrapper
    return decorator

@retry(max_attempts=3)
def unstable_api_call():
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionResetError("Connection dropped by peer!")
    print("✅ API Call Succeeded!")

try:
    unstable_api_call()
except Exception:
    print("Handled terminal failure gracefully.")
```

---

## 7. Common Fresher Pitfalls

1. **Forgetting `@functools.wraps`**:
   - If you don't use `@wraps(func)`, your decorated function's `__name__` becomes `"wrapper"`, breaking debugging tools, documentation generators, and FastAPI routers!
2. **Forgetting to `return result` from `wrapper`**:
   - If your wrapper forgets to return the output of `func(*args, **kwargs)`, the decorated function will unexpectedly return `None`!
3. **Overusing decorators where a simple function call suffices**.

---

## 8. Daily Hands-On Lab

### 🧪 Exercise: Build an Enterprise Role-Based Access Control (RBAC) Decorator
**Scenario**: In secure microservices and AI agent endpoints, only users with authorized roles (e.g., `admin`, `data_scientist`) should be allowed to run sensitive workflows. Build a role-checking decorator.

```python
# ==========================================
# Day 9 Lab: RBAC Security Guard Decorator
# ==========================================
from functools import wraps

# Simulated current user session
CURRENT_USER = {
    "username": "kavya_m",
    "role": "ai_researcher"
}

def require_role(allowed_roles: list[str]):
    """Enforces that the current authenticated user has an authorized role."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = CURRENT_USER.get("role")
            if user_role not in allowed_roles:
                raise PermissionError(
                    f"⛔ Access Denied for '{CURRENT_USER['username']}'! "
                    f"Required: {allowed_roles}, Found: '{user_role}'"
                )
            print(f"🛡️ [AUTH PASSED] User '{CURRENT_USER['username']}' authorized for {func.__name__}.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Protected Functions
@require_role(allowed_roles=["admin", "ai_researcher"])
def deploy_model_to_production(model_name: str):
    return f"🚀 Model '{model_name}' successfully deployed to Kubernetes cluster!"

@require_role(allowed_roles=["admin"])
def wipe_database():
    return "💥 Production Database Purged!"

# Test Authorization
print(deploy_model_to_production("Llama-3-70B-FineTuned"))

try:
    wipe_database()
except PermissionError as err:
    print(err)
```

---

## 9. Interview Quick-Fire Questions

1. **Q: What is a closure in Python and when would you use one?**
   - **Answer**: A closure is a function object that retains access to variables from its lexical enclosing scope, even after the outer function has returned. Closures are used to avoid global state, implement data hiding without full classes, and serve as the building blocks for function decorators.
2. **Q: Why is `@functools.wraps` recommended inside decorators?**
   - **Answer**: When wrapping a function, the wrapper function replaces the original. `@functools.wraps` copies metadata (such as `__name__`, `__doc__`, and `__annotations__`) from the original function onto the wrapper, preventing metadata loss.
3. **Q: Can you apply multiple decorators to a single function? In what order do they execute?**
   - **Answer**: Yes. Decorators are applied from the **bottom up** (closest to the function definition first), but when the decorated function is called, the wrappers execute from the **top down** (outside in).
