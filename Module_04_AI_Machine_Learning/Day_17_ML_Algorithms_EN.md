# Day 17: Machine Learning Algorithms (Regression, Classification & Clustering)

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. The mathematical intuition behind **Linear Regression** (continuous forecasting).
2. How **Logistic Regression** uses the **Sigmoid function** for binary classification.
3. **Decision Trees** (Gini Impurity) and why **Random Forests** (Ensembles) dominate tabular data.
4. The core difference between **Classification** (discrete labels) and **Regression** (continuous numbers).
5. Unsupervised pattern discovery using **K-Means Clustering**.

---

## 1. Classification vs Regression: The Big Division

Every supervised machine learning problem belongs to one of two categories:

| Dimension | Regression Problem | Classification Problem |
| :--- | :--- | :--- |
| **Output Type** | Continuous numerical value | Discrete category / class label |
| **Question Asked** | *"How much?"* or *"How many?"* | *"Which category?"* or *"Yes or No?"* |
| **Examples** | House price (₹75.5 Lakhs), Temperature (38.2°C) | Email is Spam (1) or Ham (0), Tumor is Benign or Malignant |
| **Key Algorithms** | Linear Regression, Ridge, Random Forest Regressor | Logistic Regression, Decision Tree Classifier, SVM |

---

## 2. Linear Regression (Finding the Line of Best Fit)

### The Equation:
$$y = W \cdot X + b$$
- $y$ : Predicted target (e.g. Salary)
- $X$ : Feature (e.g. Years of Experience)
- $W$ : Weight / Slope (How much $y$ changes when $X$ increases by 1)
- $b$ : Bias / Intercept (The baseline value when $X = 0$)

The model minimizes the **Mean Squared Error (MSE)** loss function:
$$\text{MSE} = \frac{1}{N} \sum (y_{\text{actual}} - y_{\text{pred}})^2$$

```python
import numpy as np
from sklearn.linear_model import LinearRegression

# Training Data: Experience in Years (X) vs Salary in INR (y)
X = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])  # Must be 2D array
y = np.array([400000, 550000, 720000, 900000, 1100000])

# Train the model
model = LinearRegression()
model.fit(X, y)

print(f"Weight (Slope)    : ₹{model.coef_[0]:,.2f} per year of experience")
print(f"Bias (Intercept)  : ₹{model.intercept_:,.2f} baseline starting salary")

# Predict for a candidate with 6.5 years experience
candidate_exp = np.array([[6.5]])
predicted_salary = model.predict(candidate_exp)
print(f"Predicted Salary for 6.5 yrs: ₹{predicted_salary[0]:,.2f}")
```

---

## 3. Logistic Regression (Probabilities & The Sigmoid Curve)

Despite the name "Regression", Logistic Regression is used for **Classification**!
Linear regression outputs values from $-\infty$ to $+\infty$. But probabilities must be bounded strictly between **0 and 1**.
We pass the linear output through the **Sigmoid function**:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

```python
from sklearn.linear_model import LogisticRegression

# Features: [Credit_Score, Monthly_Income_Lakhs]
X_train = np.array([
    [780, 1.2],
    [620, 0.4],
    [810, 2.5],
    [580, 0.3],
    [720, 0.9]
])
# Labels: 1 = Loan Approved, 0 = Loan Rejected
y_train = np.array([1, 0, 1, 0, 1])

clf = LogisticRegression()
clf.fit(X_train, y_train)

# Predict for a new applicant: Credit 710, Income 0.85L
new_applicant = np.array([[710, 0.85]])
prediction = clf.predict(new_applicant)
probabilities = clf.predict_proba(new_applicant)[0]

print(f"Decision: {'APPROVED' if prediction[0] == 1 else 'REJECTED'}")
print(f"Approval Probability: {probabilities[1]*100:.2f}% | Rejection Probability: {probabilities[0]*100:.2f}%")
```

---

## 4. Decision Trees & Random Forests (The Wisdom of Crowds)

### Decision Tree:
Asks a sequence of binary questions (e.g., *"Is Income > 50,000?"*), splitting data based on **Gini Impurity** (measuring how mixed the classes are).
- *Downside*: Single trees easily **overfit** (memorize noise).

### Random Forest (Ensemble Learning):
Instead of relying on 1 tree, build an entire forest of **100 independent trees**, each trained on a random subset of data and features.
- In classification: The forest takes a **majority vote**.
- In regression: The forest takes the **average**.

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Feature Importance: See which feature mattered most!
print("Feature Importances [Credit Score, Income]:", rf.feature_importances_)
```

---

## 5. Unsupervised Learning: K-Means Clustering

K-Means automatically partitions unlabelled data into $K$ distinct clusters by minimizing the distance between data points and their cluster centroids.

```python
from sklearn.cluster import KMeans

# Customer data: [Annual_Spend_INR, Visit_Frequency_Per_Month]
customer_data = np.array([
    [15000, 2], [18000, 3], [12000, 1],       # Cluster 1: Low spend, low visits
    [85000, 12], [92000, 15], [78000, 10],    # Cluster 2: VIP high spend, frequent
    [45000, 20], [50000, 22], [42000, 18]     # Cluster 3: Medium spend, bargain hunters
])

kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
kmeans.fit(customer_data)

print("Cluster Labels Assigned:", kmeans.labels_)
print("Cluster Centroids:\n", kmeans.cluster_centers_)
```

---

## 6. Common Fresher Pitfalls

1. **Using Linear Regression for Classification**:
   - Linear regression can output values $< 0$ or $> 1$, which makes no mathematical sense as a probability. Always use Logistic Regression.
2. **Ignoring Feature Scaling in Distance-Based Algorithms (like K-Means)**:
   - If Feature 1 is Salary (₹10,00,000) and Feature 2 is Age (25), the salary feature will completely dominate Euclidean distance calculations. Always scale features using `StandardScaler` before clustering!
3. **Setting `n_estimators` too low or depth unlimited**:
   - Single deep trees overfit severely. Limit `max_depth` to avoid memorizing data.

---

## 7. Daily Hands-On Lab

### 🧪 Exercise: Build a Machine Learning Model Comparison Engine
**Scenario**: You are an AI Engineer given medical diagnostic records. Compare **Logistic Regression** and **Random Forest** to classify whether a patient has diabetes based on diagnostic features.

```python
# =========================================================
# Day 17 Lab: Classification Algorithm Comparison
# =========================================================
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Diagnostic Features: [Glucose_Level, BMI, Age]
X_records = np.array([
    [85, 22.0, 25], [92, 24.5, 30], [105, 26.0, 35], [78, 21.0, 22],
    [165, 33.5, 45], [180, 38.0, 52], [145, 31.0, 48], [190, 36.5, 60]
])
# Labels: 0 = Healthy, 1 = Diabetic
y_labels = np.array([0, 0, 0, 0, 1, 1, 1, 1])

# Model 1: Logistic Regression
log_model = LogisticRegression()
log_model.fit(X_records, y_labels)
log_preds = log_model.predict(X_records)

# Model 2: Random Forest (10 trees)
rf_model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
rf_model.fit(X_records, y_labels)
rf_preds = rf_model.predict(X_records)

# Evaluation
print("--- MODEL EVALUATION SUMMARY ---")
print(f"Logistic Regression Accuracy: {accuracy_score(y_labels, log_preds) * 100:.1f}%")
print(f"Random Forest Classifier Accuracy: {accuracy_score(y_labels, rf_preds) * 100:.1f}%")

# Test on an unseen patient: Glucose 170, BMI 34.0, Age 50
unseen_patient = np.array([[170, 34.0, 50]])
print(f"\nUnseen Patient Diagnosis:")
print(f"  • Logistic Regression : {'DIABETIC' if log_model.predict(unseen_patient)[0] == 1 else 'HEALTHY'}")
print(f"  • Random Forest       : {'DIABETIC' if rf_model.predict(unseen_patient)[0] == 1 else 'HEALTHY'}")
```

---

## 8. Interview Quick-Fire Questions

1. **Q: Why is Logistic Regression called a regression model if it performs classification?**
   - **Answer**: Under the hood, Logistic Regression performs a linear regression calculation ($z = W \cdot X + b$) to model the **log-odds** (logit) of the positive class. It is only transformed into a categorical probability via the non-linear Sigmoid activation function.
2. **Q: What is the primary difference between Bagging and Boosting in Ensemble Learning?**
   - **Answer**: **Bagging** (Bootstrap Aggregation, e.g. Random Forest) trains multiple independent models in parallel on random data subsets and averages their votes to reduce variance (overfitting). **Boosting** (e.g. XGBoost, LightGBM) trains models sequentially, where each new model focuses specifically on correcting the errors of the previous models, reducing bias.
3. **Q: How do you choose the optimal number of clusters $K$ in K-Means?**
   - **Answer**: By using the **Elbow Method**. You compute the Within-Cluster Sum of Squares (Inertia) across different values of $K$ (e.g. 1 to 10) and plot it. The "elbow point"—where the rate of decrease abruptly bends and flattens—indicates the optimal tradeoff between simplicity and variance.
