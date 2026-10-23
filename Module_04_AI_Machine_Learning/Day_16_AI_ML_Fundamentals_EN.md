# Day 16: AI & Machine Learning Fundamentals (NumPy & Pandas)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The clear hierarchy: **Artificial Intelligence (AI)** vs **Machine Learning (ML)** vs **Deep Learning (DL)** vs **Generative AI (GenAI)**.
2. The 3 paradigms of learning: **Supervised**, **Unsupervised**, and **Reinforcement Learning**.
3. The end-to-end Machine Learning lifecycle in industry.
4. Numerical computing foundation: **NumPy** (ND-arrays, vectorization, broadcasting).
5. Tabular data manipulation: **Pandas** (DataFrames, Series, filtering, missing value imputation).

---

## 1. The "Why": From Rules to Data-Driven Learning

In traditional programming (Days 1–15):
$$\text{Rules (Your Code)} + \text{Input Data} \longrightarrow \text{Answers (Output)}$$
*Example: You write 50 nested `if-else` rules to detect whether an email is spam.*

In Machine Learning:
$$\text{Historical Data} + \text{Answers (Labels)} \longrightarrow \text{Rules (The Trained Model!)}$$
Instead of a human manually handcrafting thousands of fragile rules, the computer figures out the mathematical patterns directly from past data!

---

## 2. Demystifying the AI Umbrella

```
┌─────────────────────────────────────────────────────────────────┐
│ ARTIFICIAL INTELLIGENCE (1950s)                                 │
│ Any technique enabling computers to mimic human intelligence    │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ MACHINE LEARNING (1980s)                                    │ │
│ │ Statistical models that learn from data without hardcoding  │ │
│ │ ┌─────────────────────────────────────────────────────────┐ │ │
│ │ │ DEEP LEARNING (2010s)                                   │ │ │
│ │ │ Multi-layered Artificial Neural Networks (ANNs)         │ │ │
│ │ │ ┌─────────────────────────────────────────────────────┐ │ │ │
│ │ │ │ GENERATIVE AI & LLMs (2020s)                        │ │ │ │
│ │ │ │ Foundation models creating new text, code, & images │ │ │ │
│ │ │ └─────────────────────────────────────────────────────┘ │ │ │
│ │ └─────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. The 3 Types of Machine Learning

| Type | Analogy | Data Type | Common Algorithms | Real-World Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Supervised Learning** | A student studying with an **answer key** | Labeled Data (Features $X$ + Target $y$) | Linear Regression, Random Forest, XGBoost | Predicting house prices, loan default, medical diagnosis |
| **Unsupervised Learning** | Organizing a closet with **no labels** | Unlabeled Data (Only features $X$) | K-Means Clustering, PCA, Isolation Forests | Customer segmentation, anomaly detection |
| **Reinforcement Learning** | Training a puppy with **treats & scolding** | Trial and Error (State, Action, Reward) | Q-Learning, PPO (Proximal Policy Optimization) | Autonomous driving, AlphaGo, RLHF for LLMs |

---

## 4. The Foundation Libraries: NumPy & Pandas

### A. NumPy: High-Performance Vectorized Math
Python lists are slow because they store pointers to objects in scattered memory. NumPy arrays store contiguous blocks of homogeneous data in C, enabling calculations up to **100x faster**.

```python
import numpy as np

# Creating arrays
arr = np.array([10, 20, 30, 40, 50])

# Vectorized operation (No for loops required!)
scaled = arr * 2.5
print("Vectorized Multiply:", scaled)

# Array math
print("Mean:", np.mean(arr))
print("Standard Deviation:", np.std(arr))

# 2D Matrices (Tensor foundations)
matrix = np.array([[1, 2], [3, 4]])
print("Matrix Shape:", matrix.shape)
print("Matrix Transpose:\n", matrix.T)
```

### B. Pandas: The Excel Sheet of Data Science
Pandas gives you the `DataFrame`—a fast, flexible 2D table with labeled rows and columns.

```python
import pandas as pd

raw_data = {
    "Employee": ["Aarav", "Pooja", "Vikram", "Sneha", "Karan"],
    "Department": ["AI", "Cloud", "AI", "DevOps", "AI"],
    "Experience_Yrs": [2.5, 5.0, 1.0, 8.0, None],  # Contains missing data!
    "Salary_INR": [850000, 1400000, 600000, 1950000, 750000]
}

df = pd.DataFrame(raw_data)

# 1. Quick Inspection
print("DataFrame Shape:", df.shape)
print("\nSummary Statistics:\n", df.describe())

# 2. Handling Missing Values (Imputation with Median)
median_exp = df["Experience_Yrs"].median()
df["Experience_Yrs"] = df["Experience_Yrs"].fillna(median_exp)

# 3. Filtering: High-earning AI engineers
ai_high_earners = df[(df["Department"] == "AI") & (df["Salary_INR"] > 700000)]
print("\nFiltered AI Specialists:\n", ai_high_earners[["Employee", "Salary_INR"]])

# 4. GroupBy Aggregations: Average salary per department
avg_dept_salary = df.groupby("Department")["Salary_INR"].mean()
print("\nAverage Department Salary:\n", avg_dept_salary)
```

---

## 5. Common Fresher Pitfalls

1. **Using Python `for` loops instead of NumPy vectorization**:
   - Running `[x * 2 for x in huge_list]` takes seconds. `arr * 2` takes milliseconds. In AI and tensor math, vectorization is mandatory.
2. **The `SettingWithCopyWarning` in Pandas**:
   - Chaining slice assignments like `df[df["Salary"] > 50000]["Salary"] = 60000` causes unpredictable bugs. Always use `df.loc[condition, "column"] = new_value`.
3. **Data Leakage during preprocessing**:
   - Calculating mean/median on the *entire* dataset before splitting into train/test leaks test information into training data. Always compute statistics *only* on the training set!

---

## 6. Daily Hands-On Lab

### 🧪 Exercise: Build a Real-World Customer Churn Data Cleaner
**Scenario**: Telecommunications companies constantly face customer churn (subscribers canceling). Clean a dirty customer dataset: drop corrupt rows, impute missing values, and calculate churn rates by contract type.

```python
# =========================================================
# Day 16 Lab: Customer Churn Data Preprocessing Pipeline
# =========================================================
import pandas as pd
import numpy as np

dirty_telecom_data = {
    "customer_id": [101, 102, 103, 104, 105, 106],
    "monthly_charges": [450.0, 990.5, None, 1250.0, 350.0, 800.0],
    "contract_type": ["Month-to-Month", "Two-Year", "Month-to-Month", "One-Year", None, "Month-to-Month"],
    "tenure_months": [2, 36, 12, 24, 1, 8],
    "churned": [1, 0, 1, 0, 1, 0]  # 1 = Left company, 0 = Stayed
}

df_cust = pd.DataFrame(dirty_telecom_data)
print("--- RAW INGESTED DATA ---")
print(df_cust)

# Step 1: Impute missing monthly charges with column mean
mean_charge = df_cust["monthly_charges"].mean()
df_cust["monthly_charges"] = df_cust["monthly_charges"].fillna(np.round(mean_charge, 2))

# Step 2: Impute missing contract type with the most frequent value (Mode)
mode_contract = df_cust["contract_type"].mode()[0]
df_cust["contract_type"] = df_cust["contract_type"].fillna(mode_contract)

# Step 3: Feature Engineering - Total Lifetime Value (Tenure * Monthly Charge)
df_cust["estimated_lifetime_val"] = df_cust["tenure_months"] * df_cust["monthly_charges"]

# Step 4: Churn Analysis by Contract Type
churn_rate = df_cust.groupby("contract_type")["churned"].mean() * 100

print("\n--- CLEANED & ENRICHED DATASET ---")
print(df_cust[["customer_id", "monthly_charges", "contract_type", "estimated_lifetime_val", "churned"]])

print("\n--- CHURN RATE BY CONTRACT (%) ---")
for contract, rate in churn_rate.items():
    print(f"  • {contract:16}: {rate:.1f}% churn")
```

---

## 7. Interview Quick-Fire Questions

1. **Q: What is the fundamental difference between Supervised and Unsupervised Learning?**
   - **Answer**: Supervised learning trains on labeled data (where the ground truth target $y$ is provided for each input $X$) to learn a mapping function for classification or regression. Unsupervised learning trains on unlabeled data (only $X$) to discover hidden patterns, clusters, or dimensionality reductions without explicit target feedback.
2. **Q: Why is NumPy faster than standard Python lists?**
   - **Answer**: NumPy arrays are homogeneous (all elements share the same data type) and are allocated in contiguous blocks of computer memory, allowing SIMD (Single Instruction, Multiple Data) CPU vectorization and cache locality. Python lists store pointers to scattered objects in memory, requiring expensive dynamic type checking and memory indirection on every operation.
3. **Q: What is a Pandas Series vs a DataFrame?**
   - **Answer**: A `Series` is a one-dimensional labeled array capable of holding any data type (essentially a single column with an index). A `DataFrame` is a two-dimensional tabular data structure with labeled axes (rows and columns), composed of multiple aligned `Series`.
