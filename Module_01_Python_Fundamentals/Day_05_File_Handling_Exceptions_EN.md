# Day 05: File Handling & Exception Management (Module 01 Capstone)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Safe file operations using Python's `with` statement (**Context Managers**).
2. Working with industry data formats: **JSON** and **CSV**.
3. Graceful error handling using `try`, `except`, `else`, and `finally`.
4. Production-grade logging using Python's standard `logging` module (replacing amateur `print` debugging).
5. **Module 01 Capstone Mini-Project**: A robust CLI Expense Tracker with persistent storage and validation.

---

## 1. The "Why": Persistence & Failure Resistance

- **Variables die when the program terminates**: If your Python app restarts or your computer turns off, all data in RAM vanishes. File handling gives your software **permanent memory**.
- **The Real World is Unforgiving**: In production, servers run out of disk space, network connections drop, and users enter corrupt inputs. If your code does not catch exceptions, your entire application crashes at 2:00 AM.

---

## 2. File Handling & Context Managers (`with` Statement)

### Mental Model: The Door Lock
- Without `with`: You open a file, read it, and must remember to call `file.close()`. If your code crashes in between, the file handle remains locked in the OS!
- With `with`: Python automatically guarantees the file is safely closed when the block exits, even if a disaster occurs inside.

```python
# Writing to a text file
log_entry = "2026-10-15 10:00:00 | System Initialized | Status: HEALTHY\n"

with open("app.log", mode="a", encoding="utf-8") as f:
    f.write(log_entry)

# Reading from a text file
with open("app.log", mode="r", encoding="utf-8") as f:
    content = f.read()
    print("Log Contents:\n", content)
```

---

## 3. Handling Structured Formats: JSON & CSV

### A. Working with JSON (JavaScript Object Notation)
JSON is the standard format for web APIs, configuration files, and AI model outputs.

```python
import json

# Python Dictionary to JSON File (json.dump)
user_session = {
    "user_id": 1045,
    "username": "satish_g",
    "roles": ["admin", "ai_developer"],
    "preferences": {"theme": "dark", "notifications": True}
}

with open("session.json", "w", encoding="utf-8") as f:
    json.dump(user_session, f, indent=4)  # indent=4 creates pretty readable JSON

# JSON File back to Python Dictionary (json.load)
with open("session.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print("Loaded Username:", loaded_data["username"])
```

### B. Working with CSV (Comma Separated Values)
CSV is ubiquitous in Data Science, Finance, and Analytics.

```python
import csv

# Writing CSV rows
employees = [
    ["EmpID", "Name", "Department", "Salary"],
    [101, "Aarav", "AI Labs", 95000],
    [102, "Diya", "Data Platform", 88000]
]

with open("employees.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(employees)

# Reading CSV rows
with open("employees.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print("Row:", row)
```

---

## 4. Exception Handling (`try`, `except`, `else`, `finally`)

### The 4 Blocks Explained:
- `try`: Run the risky code here.
- `except`: What to do if an error occurs (fallback/recovery).
- `else`: Runs **only if no error occurred** in `try`.
- `finally`: **Always runs**, whether an error occurred or not (cleanup, closing connections).

```python
def process_user_payment(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        print(f"✅ Processing transaction of ₹{amount:,.2f}...")
    except ValueError as err:
        print(f"❌ Input Validation Error: {err}")
    except Exception as general_err:
        print(f"🚨 Unexpected System Error: {general_err}")
    else:
        print("🎉 Payment succeeded! Receipt generated.")
    finally:
        print("🔒 Database lock released. Session terminated.\n")

process_user_payment("1500.50")  # Success case
process_user_payment("-500")     # Custom validation failure
process_user_payment("abc")      # Parsing failure
```

---

## 5. Professional Logging (Stop Using `print()`!)

In production systems, `print()` statements are lost in the void. Python's `logging` module writes timestamped, categorized logs to files and cloud dashboards.

```python
import logging

# Configure logger
logging.basicConfig(
    filename="production.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("BillingService")

logger.info("Billing service started successfully.")
logger.warning("Payment gateway latency is higher than 800ms.")
try:
    10 / 0
except ZeroDivisionError:
    logger.error("Division by zero occurred in tax calculation!", exc_info=True)
```

---

## 6. Common Fresher Pitfalls

1. **Bare `except:` blocks**:
   ```python
   # ❌ NEVER DO THIS (Catches system interrupts like Ctrl+C and obscures real bugs!)
   try:
       risky_code()
   except:
       pass

   # ✅ ALWAYS specify the exception type:
   except (ValueError, FileNotFoundError) as e:
       logger.error(f"Handled error: {e}")
   ```
2. **Missing `encoding="utf-8"`**:
   - On Windows, failing to specify `encoding="utf-8"` causes silent crashes when processing non-English text or emojis.
3. **Overwriting files with `"w"` instead of appending with `"a"`**:
   - Opening with mode `"w"` immediately clears all existing data in that file!

---

## 7. Module 01 Capstone Project: Personal Expense Tracker CLI

This project integrates everything learned across Days 1–5: variables, conditions, loops, collections, functions, file handling, and error validation!

```python
# =========================================================
# Module 01 Capstone: Personal Expense Tracker CLI
# =========================================================
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

def load_expenses() -> list:
    """Loads expenses from JSON file. Returns empty list if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Corrupt data file detected. Starting with fresh ledger.")
        return []

def save_expenses(expenses: list):
    """Saves expense records to persistent JSON storage."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)

def add_expense(expenses: list):
    """Prompts user and records a validated expense."""
    title = input("Enter description (e.g., Grocery, Rent): ").strip()
    if not title:
        print("❌ Description cannot be blank.")
        return

    category = input("Enter category (Food, Travel, Utilities, Misc): ").strip()
    try:
        amount = float(input("Enter amount (in INR): "))
        if amount <= 0:
            print("❌ Amount must be positive.")
            return
    except ValueError:
        print("❌ Invalid amount entered. Please enter a valid number.")
        return

    record = {
        "id": len(expenses) + 1,
        "title": title,
        "category": category.title(),
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    expenses.append(record)
    save_expenses(expenses)
    print(f"✅ Added: '{title}' (₹{amount:,.2f}) successfully!")

def view_summary(expenses: list):
    """Displays total spend and breakdown by category."""
    if not expenses:
        print("ℹ️ No expenses recorded yet.")
        return

    total_spend = sum(item["amount"] for item in expenses)
    print("\n" + "="*45)
    print(f"💰 TOTAL EXPENDITURE: ₹{total_spend:,.2f}")
    print("="*45)

    category_totals = {}
    for item in expenses:
        cat = item["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + item["amount"]

    for cat, total in category_totals.items():
        percentage = (total / total_spend) * 100
        print(f"  • {cat:15}: ₹{total:,.2f} ({percentage:.1f}%)")
    print("="*45)

def main():
    expenses = load_expenses()
    while True:
        print("\n--- 📊 PERSONAL EXPENSE MANAGER ---")
        print("1. Add New Expense")
        print("2. View Expense Summary")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            print("Goodbye! Keeping your finances healthy.")
            break
        else:
            print("❌ Invalid choice. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
```

---

## 8. Interview Quick-Fire Questions

1. **Q: What is a context manager in Python and how does the `with` statement work?**
   - **Answer**: A context manager manages runtime resources by automatically executing setup and teardown logic. It implements the `__enter__()` and `__exit__()` protocol. The `with` statement guarantees that `__exit__()` is called (closing files or database connections), even if an unhandled exception occurs inside the block.
2. **Q: What is the difference between `json.dump()` and `json.dumps()`?**
   - **Answer**: `json.dump()` writes Python data directly into an open file pointer. `json.dumps()` (dump string) serializes Python data into a formatted JSON string in memory.
3. **Q: Can the `finally` block execute if a `return` statement is hit inside `try`?**
   - **Answer**: Yes! Even if you return a value inside the `try` block, Python guarantees that the `finally` block will execute before the function actually exits.
