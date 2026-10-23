# Day 06: Object-Oriented Programming (OOP) Fundamentals

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The real-world philosophy of OOP: Modeling entities with State (attributes) and Behavior (methods).
2. Creating Classes, Instantiating Objects, and mastering the `__init__` constructor and `self`.
3. Encapsulation: Public vs Protected (`_`) vs Private (`__`) attributes, and modern `@property` getters/setters.
4. The difference between **Instance Methods**, **Class Methods** (`@classmethod`), and **Static Methods** (`@staticmethod`).

---

## 1. The "Why": Why OOP in the Real World?

Imagine building an AI chat service or a banking app using only dictionaries:
```python
# The messy procedural way
account1 = {"acc_num": "SB-101", "balance": 5000}
account2 = {"acc_num": "SB-102", "balance": 12000}

# Anyone can accidentally do this anywhere in the codebase!
account1["balance"] = -9999999  # Corrupt state!
```
Procedural code leaves data naked and vulnerable to corruption.
**OOP binds data together with the functions that manipulate it** into a single protective container called an **Object**.

### The Real-World Metaphor:
- **Class**: The **Architectural Blueprint** of a building. It costs zero cement and zero bricks; it is just a specification.
- **Object / Instance**: The **Actual Building constructed** from that blueprint. You can build 50 buildings from 1 blueprint, and each building can have its own paint color and tenant!

---

## 2. Anatomy of a Class: `self` and `__init__`

Freshers are often puzzled by `self`. 
- **`self` is simply Python's way of referring to "THIS specific object instance"**. 
- When `acct1.deposit(500)` is called, Python under the hood executes `BankAccount.deposit(acct1, 500)`.

```python
class BankAccount:
    # Class Attribute (Shared across ALL bank accounts)
    BANK_NAME = "TechIn FinTech Bank"
    INTEREST_RATE = 0.04  # 4% annual interest

    # Constructor / Initializer (Called whenever a new object is created)
    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        # Instance Attributes (Unique to each individual account)
        self.account_holder = account_holder
        self.balance = initial_balance

    # Instance Method (Operates on 'self' - this specific account)
    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        print(f"✅ Deposited ₹{amount:,.2f} into {self.account_holder}'s account. New Balance: ₹{self.balance:,.2f}")

    def withdraw(self, amount: float):
        if amount > self.balance:
            print(f"❌ Withdrawal of ₹{amount:,.2f} declined! Insufficient funds.")
            return False
        self.balance -= amount
        print(f"💵 Withdrawn ₹{amount:,.2f}. Remaining Balance: ₹{self.balance:,.2f}")
        return True

# Creating Instances (Objects)
acc1 = BankAccount("Rahul Sharma", 15000)
acc2 = BankAccount("Priya Patel", 50000)

acc1.deposit(2500)
acc1.withdraw(20000)  # Should fail
acc2.withdraw(10000)  # Should succeed
```

---

## 3. Encapsulation & The `@property` Decorator

In Python, encapsulation is achieved through naming conventions and properties:
- `name` : Public (Accessible everywhere).
- `_name` : Protected convention (Internal to module/subclass; do not touch unless you know what you are doing).
- `__name` : Private (Name-mangled by Python to prevent direct access).

```python
class Employee:
    def __init__(self, name: str, monthly_salary: float):
        self.name = name
        self._monthly_salary = monthly_salary  # Protected attribute

    # Getter: Read the salary cleanly like an attribute (emp.salary)
    @property
    def salary(self) -> float:
        return self._monthly_salary

    # Setter: Control and validate updates before changing data
    @salary.setter
    def salary(self, new_salary: float):
        if new_salary < 15000:
            raise ValueError("Salary cannot be below minimum wage (₹15,000)!")
        print(f"Updating salary for {self.name} to ₹{new_salary:,.2f}")
        self._monthly_salary = new_salary

emp = Employee("Vikram", 45000)
print(f"Current Salary: ₹{emp.salary:,.2f}")

emp.salary = 55000     # Calls the @salary.setter automatically!
# emp.salary = 5000    # ❌ Raises ValueError!
```

---

## 4. Method Types: Instance vs Class vs Static

| Method Type | Decorator | First Parameter | Access Level | When to Use |
| :--- | :--- | :--- | :--- | :--- |
| **Instance Method** | None | `self` | Accesses instance and class state | Default for standard object behavior |
| **Class Method** | `@classmethod` | `cls` | Accesses class state (not instance) | Factory constructors (e.g. from JSON/dict) |
| **Static Method** | `@staticmethod` | None | Pure utility (no `self`, no `cls`) | Standalone logic logically related to class |

```python
class User:
    TOTAL_USERS = 0

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        User.TOTAL_USERS += 1

    # Instance method
    def send_welcome_email(self):
        print(f"Sending welcome email to {self.email}...")

    # Class method as an alternative constructor (Factory)
    @classmethod
    def from_dict(cls, data: dict):
        return cls(username=data["username"], email=data["email"])

    # Static method (Utility function that doesn't need self or cls)
    @staticmethod
    def is_valid_email(email: str) -> bool:
        return "@" in email and "." in email

# Using the different methods:
user_data = {"username": "ananya_ai", "email": "ananya@techin.ai"}

# Checking email before creating user
if User.is_valid_email(user_data["email"]):
    user1 = User.from_dict(user_data)  # Created via Factory Classmethod
    user1.send_welcome_email()         # Instance method

print("Total registered users in system:", User.TOTAL_USERS)
```

---

## 5. Common Fresher Pitfalls

1. **Forgetting `self` as the first argument in instance methods**:
   - Defining `def deposit(amount):` instead of `def deposit(self, amount):` causes `TypeError: deposit() takes 1 positional argument but 2 were given`.
2. **Accidentally modifying class attributes on an instance**:
   - Writing `acc1.BANK_NAME = "New Bank"` creates an instance attribute on `acc1` that shadows the class attribute, without changing it for other instances.
3. **Overusing `@staticmethod` when a simple module-level function is cleaner**.

---

## 6. Daily Hands-On Lab

### 🧪 Exercise: AI Model Serving Endpoint Manager
**Scenario**: Model registry systems track deployed foundation models (e.g. GPT-4, Gemini 1.5, Claude 3.5). Build a `ModelEndpoint` class that tracks active requests, enforces maximum concurrent query limits, and calculates inference costs.

```python
# ==========================================
# Day 6 Lab: AI Model Serving Endpoint
# ==========================================

class ModelEndpoint:
    DEPLOYED_REGISTRY = []

    def __init__(self, model_name: str, cost_per_1k_tokens: float, max_concurrency: int = 5):
        self.model_name = model_name
        self.cost_per_1k_tokens = cost_per_1k_tokens
        self.max_concurrency = max_concurrency
        self._active_requests = 0
        self._total_tokens_served = 0
        ModelEndpoint.DEPLOYED_REGISTRY.append(self.model_name)

    @property
    def active_requests(self) -> int:
        return self._active_requests

    def process_inference(self, tokens_used: int) -> bool:
        """Simulates processing a query if concurrency limit is not breached."""
        if self._active_requests >= self.max_concurrency:
            print(f"⚠️ [503 OVERLOAD] {self.model_name} is at max capacity ({self.max_concurrency} active requests).")
            return False

        # Request admitted
        self._active_requests += 1
        self._total_tokens_served += tokens_used
        print(f"⚡ [{self.model_name}] Inference processing: {tokens_used} tokens (Active: {self._active_requests})")
        
        # Simulating request completion
        self._active_requests -= 1
        return True

    def calculate_billing_usd(self) -> float:
        return (self._total_tokens_served / 1000) * self.cost_per_1k_tokens

    @classmethod
    def get_deployed_catalog(cls) -> list:
        return cls.DEPLOYED_REGISTRY

# Test the Lab Implementation
gemini_endpoint = ModelEndpoint("gemini-1.5-flash", cost_per_1k_tokens=0.000375, max_concurrency=2)

gemini_endpoint.process_inference(1200)
gemini_endpoint.process_inference(4500)
print(f"Total Billing for {gemini_endpoint.model_name}: ${gemini_endpoint.calculate_billing_usd():.6f}")
print("Active Global Models Catalog:", ModelEndpoint.get_deployed_catalog())
```

---

## 7. Interview Quick-Fire Questions

1. **Q: What is `self` in Python classes?**
   - **Answer**: `self` is an explicit reference to the current instance of the class. It is passed automatically by Python when invoking an instance method, allowing access to that specific object's attributes and methods.
2. **Q: What is the difference between `@classmethod` and `@staticmethod`?**
   - **Answer**: A `@classmethod` receives the class itself (`cls`) as its first parameter and can inspect or modify class-level state. A `@staticmethod` receives neither `self` nor `cls`; it behaves like a standard function scoped within the class's namespace.
3. **Q: How does encapsulation work in Python if there is no true `private` keyword?**
   - **Answer**: Python uses conventions. A single leading underscore (`_variable`) signifies protected intent ("developer beware"). A double leading underscore (`__variable`) triggers **name mangling**, where Python internally rewrites the attribute name to `_ClassName__variable` to prevent accidental overriding in subclasses.
