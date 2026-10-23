# Day 02: Operators & Control Flow

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Python's operator ecosystem (Arithmetic, Comparison, Logical, Assignment, Membership).
2. Decision-making using `if`, `elif`, and `else` blocks.
3. Looping constructs: `for` loops (traversing sequences) and `while` loops (condition-based execution).
4. Controlling loop behavior with `break`, `continue`, and `pass`.
5. Solving real-world logic problems with nested conditions.

---

## 1. The "Why": Decision Making & Repetition in Software

Computers are dumb machines that happen to calculate really fast. Their power comes from two things:
1. **Making decisions**: *"If a customer's credit score is above 750, approve the loan, otherwise reject it."*
2. **Repetition**: *"Send an email receipt to all 10,000 customers who paid today."*

Without operators and control flow, software cannot make decisions or automate repetitive work.

---

## 2. Operators Overview

### A. Arithmetic Operators
| Operator | Name | Example | Result |
| :--- | :--- | :--- | :--- |
| `+` | Addition | `10 + 5` | `15` |
| `-` | Subtraction | `10 - 5` | `5` |
| `*` | Multiplication | `10 * 5` | `50` |
| `/` | True Division | `10 / 4` | `2.5` (always float) |
| `//` | Floor Division | `10 // 4` | `2` (truncates decimal) |
| `%` | Modulo (Remainder) | `10 % 3` | `1` (useful for even/odd check) |
| `**` | Exponentiation (Power) | `2 ** 3` | `8` ($2^3$) |

### B. Comparison & Logical Operators
- **Comparison**: `==` (equal to), `!=` (not equal to), `>`, `<`, `>=`, `<=`
- **Logical**: `and` (both true), `or` (at least one true), `not` (inverts truth)
- **Membership**: `in`, `not in` (checks if an item exists inside a collection)

```python
# Real-world security authentication check
user_role = "Admin"
has_2fa_enabled = True
is_account_locked = False

# Logical compound condition
can_access_database = (user_role == "Admin" or user_role == "SuperUser") and has_2fa_enabled and not is_account_locked
print(f"Access Granted: {can_access_database}")  # True
```

---

## 3. Conditional Blocks (`if`, `elif`, `else`)

### Analogy: Traffic Light System
- `if green`: Proceed.
- `elif yellow`: Slow down and prepare to stop.
- `else`: Stop completely.

```python
# Real-world e-commerce discount engine
cart_total = 3200  # in INR

if cart_total >= 5000:
    discount_percent = 25
elif cart_total >= 2500:
    discount_percent = 15
elif cart_total >= 1000:
    discount_percent = 5
else:
    discount_percent = 0

discount_amount = cart_total * (discount_percent / 100)
final_price = cart_total - discount_amount

print(f"Cart: ₹{cart_total} | Discount: {discount_percent}% (₹{discount_amount}) | Total: ₹{final_price}")
```

---

## 4. Loops (`for` and `while`)

### A. `for` Loop: Definite Iteration (You know the collection or count)
Use `for` when you have a list, a string, or a known range of numbers.

```python
# The range(start, stop, step) function
# Generates numbers from start up to (stop - 1)
print("Processing batches:")
for batch_id in range(1, 6):  # 1 to 5
    print(f"  → Processed batch #{batch_id}")

# Iterating over characters or collections
servers = ["web-prod-01", "web-prod-02", "db-prod-01"]
for server in servers:
    print(f"Pinging {server}... Status: 200 OK")
```

### B. `while` Loop: Indefinite Iteration (Run until a condition flips to False)
Use `while` when you don't know in advance how many times it must run (e.g. waiting for a database connection or API response).

```python
# Simulating an API Retry mechanism
max_attempts = 3
attempt = 1
is_connected = False

while attempt <= max_attempts and not is_connected:
    print(f"Attempting to connect to payment gateway (Try #{attempt})...")
    # Simulate success on attempt 2
    if attempt == 2:
        is_connected = True
        print("  ✅ Connection established successfully!")
    attempt += 1

if not is_connected:
    print("  ❌ Failed to connect after all attempts. Alerting DevOps team!")
```

---

## 5. Controlling Loops: `break`, `continue`, `pass`

- `break`: Immediately exits the loop entirely.
- `continue`: Skips the rest of the **current** iteration and jumps directly to the next one.
- `pass`: A placeholder statement that does nothing (avoids syntax errors when writing skeletons).

```python
# Scanning server log errors
log_lines = ["INFO: Health check OK", "DEBUG: Cache refreshed", "ERROR: Database timeout", "INFO: Job finished"]

for log in log_lines:
    if "DEBUG" in log:
        continue  # Skip debug logs; we don't care to alert on them
    
    if "ERROR" in log:
        print(f"🚨 CRITICAL ALERT TRIGGERED: {log}")
        break     # Stop processing logs immediately and trigger pager
```

---

## 6. Common Fresher Pitfalls

1. **Confusing `=` with `==`**:
   - `=` is an **assignment** (`x = 10` puts 10 into x).
   - `==` is a **comparison** (`if x == 10:` checks if x equals 10).
2. **Infinite `while` Loops**:
   - Forgetting to increment your counter inside a `while` loop (e.g. omitting `count += 1`), causing the program to freeze.
3. **Off-by-One Errors in `range()`**:
   - `range(1, 10)` stops at **9**, not 10! The second parameter is strictly exclusive.

---

## 7. Daily Hands-On Lab

### 🧪 Exercise: ATM Cash Withdrawal & Pin Verification System
**Scenario**: Build a console simulation where a user has 3 attempts to enter the correct PIN (1234). Once authenticated, allow them to check balance or withdraw funds with validation checks.

```python
# ==========================================
# Day 2 Lab: ATM Simulation
# ==========================================

CORRECT_PIN = "1234"
account_balance = 25000.0
max_attempts = 3
authenticated = False

print("🏦 Welcome to TechIn Global Bank ATM")

for attempt in range(1, max_attempts + 1):
    pin_input = input(f"Enter your 4-digit PIN (Attempt {attempt}/{max_attempts}): ")
    if pin_input == CORRECT_PIN:
        authenticated = True
        print("\n✅ PIN Verified Successfully!\n")
        break
    else:
        remaining = max_attempts - attempt
        print(f"❌ Incorrect PIN. Remaining attempts: {remaining}")

if not authenticated:
    print("🚨 Card blocked due to 3 consecutive wrong PIN attempts. Contact branch.")
else:
    # Transaction Menu
    print("1. Check Balance")
    print("2. Cash Withdrawal")
    choice = input("Select an option (1 or 2): ")

    if choice == "1":
        print(f"Your current balance is: ₹{account_balance:,.2f}")
    elif choice == "2":
        withdraw_amount = float(input("Enter amount to withdraw (multiples of 500): "))
        if withdraw_amount <= 0:
            print("❌ Invalid amount.")
        elif withdraw_amount % 500 != 0:
            print("❌ Amount must be in multiples of ₹500.")
        elif withdraw_amount > account_balance:
            print(f"❌ Insufficient funds! Your balance is only ₹{account_balance:,.2f}")
        else:
            account_balance -= withdraw_amount
            print(f"💵 Dispensing ₹{withdraw_amount:,.2f}... Collect your cash!")
            print(f"Remaining balance: ₹{account_balance:,.2f}")
    else:
        print("❌ Invalid choice selected.")
```

---

## 8. Interview Quick-Fire Questions

1. **Q: What is the difference between `break` and `continue`?**
   - **Answer**: `break` terminates the entire loop immediately, transferring control to the code outside the loop. `continue` only terminates the current iteration and jumps directly to the next iteration of the loop.
2. **Q: Does Python have a `switch-case` statement?**
   - **Answer**: Historically Python used `if-elif-else`. However, starting with Python 3.10, Python introduced Structural Pattern Matching with the `match-case` statement.
3. **Q: What is short-circuit evaluation in Python logical operators?**
   - **Answer**: Python stops evaluating logical expressions as soon as the outcome is certain. In `A and B`, if `A` is `False`, `B` is never evaluated. In `A or B`, if `A` is `True`, `B` is never evaluated.
