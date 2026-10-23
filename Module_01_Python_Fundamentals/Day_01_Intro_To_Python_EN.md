# Day 01: Introduction to Python & Setup

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Why Python dominates modern AI, Data Science, and Web Development.
2. How Python code runs behind the scenes (Interpreter vs Compiler).
3. How to set up your environment (Python 3.11+, VS Code, Jupyter Notebook).
4. Python core syntax, clean indentation rules, variables, and primitive data types.
5. User input/output and basic expressions.

---

## 1. The "Why": Why Python in the Age of AI?

Imagine you want to build an AI chatbot or a web service. 
- In **C++** or **Java**, you might need 15–20 lines of boilerplate code (classes, main methods, memory allocation) just to read a file or call an API.
- In **Python**, you write what you think in plain, human-readable English:

```python
# Reading a file in Python
with open("data.txt") as file:
    print(file.read())
```

### The Real-World Metaphor:
Think of programming languages like vehicles:
- **C/C++** is a Formula 1 racing car: Insanely fast, but if you don't know how to handle the clutch and gearbox (memory management), you will crash.
- **Python** is a modern Tesla: It handles transmission, automatic braking, and navigation for you. You focus on the destination (the business problem or AI model).

---

## 2. Environment Setup (Zero-to-Hero)

### Step 1: Install Python
- Go to [python.org](https://www.python.org/) and download Python 3.11 or 3.12.
- ⚠️ **CRITICAL FOR WINDOWS USERS**: Always check the box **"Add Python to PATH"** before clicking Install.

Verify in your Terminal (macOS/Linux) or Command Prompt (Windows):
```bash
python --version
# or
python3 --version
```

### Step 2: Code Editor (VS Code)
1. Download **Visual Studio Code** from [code.visualstudio.com](https://code.visualstudio.com/).
2. Open VS Code and install the official **Python Extension** (by Microsoft).

### Step 3: Interactive Notebooks (Jupyter)
Jupyter allows you to run code cell-by-cell and inspect outputs instantly:
```bash
pip install jupyter
```

---

## 3. Core Concepts & Syntax

### Concept A: Indentation (Python's Signature Rule)
Unlike Java, C, or JavaScript, Python does **not** use curly braces `{ }` to define blocks of code. It uses **whitespace indentation** (standard: 4 spaces).

```python
# ✅ CORRECT (4-space indentation)
is_logged_in = True
if is_logged_in:
    print("Welcome back to TeachIn!")
    print("Dashboard loaded successfully.")

# ❌ INCORRECT (IndentationError: unexpected indent)
# if is_logged_in:
# print("This will throw an error")
```

---

### Concept B: Variables and Dynamic Typing
In Python, you do not declare types like `int age = 22;`. Python figures out the type automatically at runtime (**Dynamic Typing**).

#### Mental Model:
Variables in Python are **not boxes** where you keep data. They are **sticky name-tags** tied to values floating in computer memory!

```python
# Integer (Whole number)
student_age = 22

# Float (Decimal number)
course_fee = 4999.50

# String (Text enclosed in single or double quotes)
student_name = "Rahul Sharma"

# Boolean (True or False - Capitalized!)
is_enrolled = True

# NoneType (Represents absence of value - like null in other languages)
certificate_id = None

# Checking the type dynamically
print(type(student_age))   # Output: <class 'int'>
print(type(course_fee))    # Output: <class 'float'>
print(type(student_name))  # Output: <class 'str'>
print(type(is_enrolled))   # Output: <class 'bool'>
```

---

### Concept C: Input / Output Operations & Type Casting

By default, the `input()` function **always captures everything as a string (`str`)**!

```python
# 1. Output using print()
print("Hello, Welcome to Day 1 of Python Training!")

# 2. Capturing user input
user_name = input("Enter your name: ")
user_age_str = input("Enter your age: ")

# ❌ Common Fresher Trap:
# next_year_age = user_age_str + 1
# TypeError: can only concatenate str (not "int") to str

# ✅ The Fix: Explicit Type Conversion (Type Casting)
user_age = int(user_age_str)
next_year_age = user_age + 1

# Modern Python String Formatting (f-strings)
print(f"Hi {user_name}! Next year you will be {next_year_age} years old.")
```

---

## 4. Common Fresher Pitfalls & "Watch Out!"

1. **Mixing Tabs and Spaces**:
   - Always stick to 4 spaces. VS Code does this automatically when you press the `Tab` key.
2. **Boolean Capitalization**:
   - Python keywords are case-sensitive. It is `True` and `False`, not `true` or `false`.
3. **Forgetting `int()` or `float()` on user input**:
   - If someone enters `10` and `20`, `input() + input()` gives `"1020"`, not `30`!

---

## 5. Daily Hands-On Coding Lab

### 🧪 Exercise: Build a "Fresher Salary Calculator"
**Scenario**: You are onboarding a new graduate. Calculate their monthly in-hand salary after standard tax deductions.

```python
# ==========================================
# Day 1 Lab: Fresher Salary & Offer Calculator
# ==========================================

candidate_name = input("Enter Candidate Name: ")
annual_ctc = float(input("Enter Annual CTC (in INR Lakhs, e.g. 6.5): "))

# Calculations
monthly_gross = (annual_ctc * 100000) / 12
tax_deduction = monthly_gross * 0.10  # 10% standard TDS deduction
monthly_in_hand = monthly_gross - tax_deduction

print("\n" + "="*40)
print(f"OFFER SUMMARY FOR: {candidate_name.upper()}")
print("="*40)
print(f"Annual CTC       : ₹{annual_ctc:.2f} Lakhs")
print(f"Monthly Gross    : ₹{monthly_gross:,.2f}")
print(f"Est. Tax (10%)   : ₹{tax_deduction:,.2f}")
print(f"Monthly In-Hand  : ₹{monthly_in_hand:,.2f}")
print("="*40)
```

---

## 6. Interview Quick-Fire Questions

1. **Q: Is Python an interpreted or compiled language?**
   - **Answer**: Python is both! Source code (`.py`) is compiled into intermediate Bytecode (`.pyc`), which is then interpreted line-by-line by the Python Virtual Machine (PVM).
2. **Q: What is dynamic typing in Python?**
   - **Answer**: You don't need to specify variable data types explicitly. The data type is determined at runtime based on the value assigned.
3. **Q: What is the difference between `/` and `//` in Python?**
   - **Answer**: `/` performs standard float division (e.g. `7 / 2 = 3.5`), whereas `//` performs floor (integer) division (e.g. `7 // 2 = 3`).
