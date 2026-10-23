# Day 03: Python Collections (Lists, Tuples, Sets & Dictionaries)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The 4 core built-in data structures in Python and when to use which.
2. Indexing, slicing (`[start:stop:step]`), and key collection methods.
3. The fundamental concept of **Mutability vs Immutability** in memory.
4. Pythonic **List & Dictionary Comprehensions** for fast, clean data manipulation.
5. Real-world data transformation (e.g., cleaning duplicate data, fast lookup tables).

---

## 1. The "Why": Data Structures in Real Systems

In real-world engineering, you never deal with single variables like `price = 100`. You deal with:
- A stream of transactions: `[120.5, 45.0, 990.0]` → **List**
- Fixed geographical coordinates of a server: `(17.3850, 78.4867)` → **Tuple**
- Unique visitor IP addresses: `{"192.168.1.1", "10.0.0.5"}` → **Set**
- A user's profile metadata: `{"user_id": 101, "role": "engineer"}` → **Dictionary**

Choosing the wrong collection can make your program 1,000 times slower!

---

## 2. The 4 Core Collections at a Glance

| Collection | Syntax | Ordered? | Indexed? | Mutable (Can edit)? | Allows Duplicates? | Best Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **List** | `[1, 2, 3]` | ✅ Yes | ✅ Yes (`[0]`) | ✅ Yes | ✅ Yes | Sequences, queues, dynamic items |
| **Tuple** | `(1, 2, 3)` | ✅ Yes | ✅ Yes (`[0]`) | ❌ No | ✅ Yes | Fixed records, coordinates, DB rows |
| **Set** | `{1, 2, 3}` | ❌ No | ❌ No | ✅ Yes | ❌ No | Deduplication, fast membership ($O(1)$) |
| **Dictionary** | `{"a": 1}` | ✅ Yes* | 🔑 By Key | ✅ Yes | ❌ Keys unique | Fast lookup tables, JSON data |

*(Note: Dictionaries maintain insertion order starting from Python 3.7+).*

---

## 3. Deep Dive into Collections

### A. Lists & Slicing
Lists are ordered, mutable arrays that can hold mixed data types.

```python
tech_stack = ["Python", "FastAPI", "Docker", "PyTorch", "Kubernetes"]

# Indexing (0-based) and Negative Indexing (from end)
print(tech_stack[0])   # 'Python'
print(tech_stack[-1])  # 'Kubernetes' (last element)

# Slicing: list[start : stop : step] (stop is exclusive!)
print(tech_stack[1:4])   # ['FastAPI', 'Docker', 'PyTorch']
print(tech_stack[::-1])  # Reverse the entire list!

# Essential List Methods
tech_stack.append("LangChain")       # Adds to end
tech_stack.insert(1, "PostgreSQL")   # Inserts at index 1
tech_stack.pop()                     # Removes last item
print("Updated Stack:", tech_stack)
```

---

### B. Tuples: Immutable Records
Once created, you **cannot** add, remove, or change elements in a tuple.

```python
# Server location (Latitude, Longitude)
server_location = (17.3850, 78.4867)

# ❌ TypeError: 'tuple' object does not support item assignment
# server_location[0] = 18.0000

# Tuple Unpacking (Clean Pythonic idiom)
lat, lon = server_location
print(f"Latitude: {lat}, Longitude: {lon}")
```

---

### C. Sets: Unique Elements & Mathematical Operations
Sets automatically drop duplicate values and provide lightning-fast lookups ($O(1)$ time complexity).

```python
# Raw user login logs with duplicate user IDs
raw_user_ids = [101, 102, 103, 101, 104, 102, 105]

# Deduplication in one line!
unique_users = set(raw_user_ids)
print("Unique Active Users:", unique_users)  # {101, 102, 103, 104, 105}

# Set Math: Operations on employee skill sets
team_a_skills = {"Python", "SQL", "Docker"}
team_b_skills = {"Docker", "Kubernetes", "AWS"}

print("Common Skills (Intersection):", team_a_skills & team_b_skills)  # {'Docker'}
print("All Skills (Union):", team_a_skills | team_b_skills)
print("Skills in A but not B (Difference):", team_a_skills - team_b_skills)  # {'Python', 'SQL'}
```

---

### D. Dictionaries: Key-Value Mappings
Dictionaries power the modern web (JSON formats are essentially Python dictionaries).

```python
employee = {
    "emp_id": "EMP-9021",
    "name": "Pooja Reddy",
    "designation": "AI Engineer",
    "skills": ["Python", "Transformers", "GCP"],
    "is_active": True
}

# Accessing values safely using .get() (Avoids KeyError if key is missing)
print(employee["name"])                     # 'Pooja Reddy'
print(employee.get("salary", "Not Disclosed"))  # Returns fallback instead of crashing!

# Adding / Updating keys
employee["salary"] = 850000
employee["designation"] = "Senior AI Engineer"

# Iterating over Dictionary
for key, value in employee.items():
    print(f"{key:12} -> {value}")
```

---

## 4. Comprehensions (Write Clean, Expressive Python)

Instead of writing 4 lines of `for` loop with `.append()`, comprehensions let you transform data in a single elegant line:

```python
# Traditional Approach
squares = []
for n in range(1, 6):
    squares.append(n ** 2)

# ✅ Pythonic List Comprehension: [expression for item in iterable if condition]
even_squares = [n ** 2 for n in range(1, 11) if n % 2 == 0]
print("Even Squares:", even_squares)  # [4, 16, 36, 64, 100]

# ✅ Dictionary Comprehension
products = ["laptop", "mouse", "keyboard"]
prices_usd = [1000, 25, 75]
USD_TO_INR = 83.0

inr_price_map = {item: price * USD_TO_INR for item, price in zip(products, prices_usd)}
print("Product Prices in INR:", inr_price_map)
```

---

## 5. Common Fresher Pitfalls

1. **Modifying a list while looping over it**:
   - Doing `for item in my_list: my_list.remove(item)` causes unexpected skips because indices shift under the hood. Iterate over a copy: `for item in my_list.copy():`.
2. **Accessing missing dictionary keys directly**:
   - `data["missing_key"]` crashes your program with `KeyError`. Always prefer `data.get("missing_key", default_value)`.
3. **Empty collections gotcha**:
   - `x = {}` creates an empty **dictionary**, NOT an empty set! To create an empty set, use `x = set()`.

---

## 6. Daily Hands-On Lab

### 🧪 Exercise: E-Commerce Inventory & Order Analyzer
**Scenario**: You are given a list of customer transactions. Parse the data, deduplicate product purchases, calculate category revenues, and find high-spending customers.

```python
# ==========================================
# Day 3 Lab: E-Commerce Transaction Analyzer
# ==========================================

orders = [
    {"order_id": 1001, "customer": "Ananya", "item": "Mechanical Keyboard", "category": "Electronics", "price": 4500},
    {"order_id": 1002, "customer": "Ravi",   "item": "Coffee Mug",          "category": "Home",        "price": 450},
    {"order_id": 1003, "customer": "Ananya", "item": "Wireless Mouse",      "category": "Electronics", "price": 1200},
    {"order_id": 1004, "customer": "Kiran",  "item": "Python AI Handbook",  "category": "Books",       "price": 850},
    {"order_id": 1005, "customer": "Ravi",   "item": "Ergonomic Chair",     "category": "Furniture",   "price": 12500},
]

# Task 1: Find all unique customers using a Set
unique_customers = {order["customer"] for order in orders}
print(f"1. Unique Customers ({len(unique_customers)}): {unique_customers}")

# Task 2: Calculate total revenue per category using a Dictionary
category_revenue = {}
for order in orders:
    cat = order["category"]
    category_revenue[cat] = category_revenue.get(cat, 0) + order["price"]

print("\n2. Revenue by Category:")
for cat, rev in category_revenue.items():
    print(f"   - {cat:15}: ₹{rev:,.2f}")

# Task 3: Filter orders above ₹2000 using List Comprehension
premium_orders = [
    f"{order['item']} by {order['customer']} (₹{order['price']})"
    for order in orders
    if order["price"] >= 2000
]
print("\n3. High-Value Orders (>= ₹2,000):")
for p in premium_orders:
    print(f"   ★ {p}")
```

---

## 7. Interview Quick-Fire Questions

1. **Q: What is the key difference between a List and a Tuple in Python?**
   - **Answer**: Lists are mutable (can add/remove/change elements in-place) and use square brackets `[]`. Tuples are immutable (cannot be changed after creation), use parentheses `()`, and are faster with lower memory overhead.
2. **Q: Why is looking up an item in a Set or Dict key faster than searching a List?**
   - **Answer**: Sets and Dictionaries use **Hash Tables** under the hood, providing average $O(1)$ (constant) lookup time. Lists require linear search $O(n)$ scanning through elements one by one.
3. **Q: What happens if you try to use a list as a dictionary key?**
   - **Answer**: It raises a `TypeError: unhashable type: 'list'`. Dictionary keys must be immutable and hashable (e.g., strings, numbers, or tuples).
