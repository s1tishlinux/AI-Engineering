# Day 18: Model Training, Validation & Evaluation Metrics

## 🎯 Learning Objectives
By the end of this session, you will understand:
1. Feature Engineering pipelines: `StandardScaler`, `OneHotEncoder`, and Scikit-Learn `Pipeline`.
2. Safe data partitioning: `train_test_split` with stratification.
3. The **Bias-Variance Tradeoff**: Diagnosing Overfitting vs Underfitting.
4. Robust validation using **K-Fold Cross-Validation**.
5. Classification metrics: **Confusion Matrix**, **Accuracy**, **Precision**, **Recall**, **F1-Score**, and **ROC-AUC**.
6. Regression metrics: **MAE**, **RMSE**, and **$R^2$ Score**.
7. Systematic hyperparameter optimization with `GridSearchCV`.

---

## 1. The "Why": Accuracy is a Dangerous Lie!

Imagine you build an AI model to detect a rare disease that only affects 1 in 1,000 people (0.1% incidence).
If your model is completely dumb and simply predicts **"HEALTHY" for every single person**:
- Its raw **Accuracy is 99.9%!**
- Yet it has **ZERO medical value** because it failed to diagnose the single sick patient, resulting in a fatality!

In the real world, **Accuracy alone will get you fired**. You must master **Precision, Recall, F1-Score, and ROC-AUC**.

---

## 2. The Confusion Matrix Demystified

For any binary classification problem (Positive = 1, Negative = 0):

```
                       ACTUAL REALITY
                    Positive (1)      Negative (0)
PREDICTED   Pos (1) [ True Positive ]  [ False Positive ]  <-- Type I Error (False Alarm)
OUTPUT      Neg (0) [ False Negative ] [ True Negative ]   <-- Type II Error (Missed Detection)
```

### The Big Four Classification Metrics:
1. **Accuracy**: Overall correctness.
   $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
2. **Precision**: *"When the model predicts Positive, how often is it actually right?"* (Crucial for Spam detection where False Positives trash important emails).
   $$\text{Precision} = \frac{TP}{TP + FP}$$
3. **Recall (Sensitivity)**: *"Out of all actual Positive cases in the real world, how many did the model catch?"* (Crucial for Cancer detection, Fraud detection, Airport security).
   $$\text{Recall} = \frac{TP}{TP + FN}$$
4. **F1-Score**: Harmonic mean of Precision and Recall (Use when classes are imbalanced!).
   $$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

---

## 3. Data Preprocessing & Scikit-Learn Pipelines

Prevent data leakage and build clean reproducible workflows using `Pipeline`:

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Simulated Customer Churn Data
data = pd.DataFrame({
    "credit_score": [720, 580, 810, 640, 700, 550, 780, 610, 690, 730],
    "account_age": [3.5, 1.0, 5.0, 2.0, 4.0, 0.5, 6.0, 1.5, 3.0, 4.5],
    "country": ["India", "USA", "India", "UK", "USA", "India", "UK", "USA", "India", "UK"],
    "churned": [0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
})

X = data.drop(columns=["churned"])
y = data["churned"]

# Step 1: Stratified Train-Test Split (Maintains class ratio in both splits!)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Step 2: Define Column Transformations
numeric_features = ["credit_score", "account_age"]
categorical_features = ["country"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(drop="first"), categorical_features)
    ]
)

# Step 3: Bundle into a unified Pipeline
clf_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(random_state=42))
])
```

---

## 4. Hyperparameter Tuning with `GridSearchCV`

Don't guess hyperparameters manually. Let `GridSearchCV` test all permutations systematically across 3-fold cross-validation:

```python
# Define hyperparameter search grid
param_grid = {
    "classifier__n_estimators": [10, 50],
    "classifier__max_depth": [2, 4]
}

# Run Grid Search
grid_search = GridSearchCV(clf_pipeline, param_grid, cv=3, scoring="f1")
grid_search.fit(X_train, y_train)

print(f"Optimal Hyperparameters: {grid_search.best_params_}")
print(f"Best Cross-Validation F1-Score: {grid_search.best_score_:.2f}")

# Evaluate optimal model on unseen test set
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print("\n--- TEST SET CLASSIFICATION REPORT ---")
print(classification_report(y_test, y_pred, zero_division=0))
```

---

## 5. Regression Metrics (When Predicting Numbers)

If you are forecasting continuous numbers (e.g. stock price, server latency, real estate):

1. **Mean Absolute Error (MAE)**: Average absolute dollar deviation. Intuitive and robust to outliers.
   $$\text{MAE} = \frac{1}{N} \sum |y_{\text{actual}} - y_{\text{pred}}|$$
2. **Root Mean Squared Error (RMSE)**: Penalizes large errors heavily (due to squaring).
   $$\text{RMSE} = \sqrt{\frac{1}{N} \sum (y_{\text{actual}} - y_{\text{pred}})^2}$$
3. **$R^2$ Score (Coefficient of Determination)**: Percentage of variance explained by model (1.0 = Perfect, 0.0 = Baseline average model).

---

## 6. Common Fresher Pitfalls

1. **Evaluating a model on training data**:
   - High training accuracy with poor test accuracy is the classic signature of **Overfitting** (High Variance). Always evaluate on a held-out test split.
2. **Using Accuracy for Imbalanced Datasets**:
   - In fraud detection or rare cancer screening, always optimize for **PR-AUC or Recall**, never pure accuracy.
3. **Fitting scalers on test data**:
   - Never call `scaler.fit(X_test)`. Only call `scaler.transform(X_test)` using parameters learned from training data!

---

## 7. Daily Hands-On Lab

### 🧪 Exercise: Build a Complete Model Evaluation Report Card
**Scenario**: You are an ML Engineer presenting model evaluation results to your VP of Engineering. Calculate the complete confusion matrix, precision, recall, and ROC-AUC score for a credit card fraud detection system.

```python
# =========================================================
# Day 18 Lab: Credit Card Fraud Evaluation Report Card
# =========================================================
import numpy as np
from sklearn.metrics import (
    confusion_matrix, precision_score, recall_score,
    f1_score, roc_auc_score
)

# Simulated Ground Truth Labels: 1 = Fraudulent Transaction, 0 = Legitimate
actual_transactions = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1, 1])

# Model 1: Lazy model that predicts all 0s
model_lazy_preds = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

# Model 2: Production ML model
model_ml_preds = np.array([0, 0, 0, 0, 1, 0, 0, 1, 1, 1])
model_ml_probs = np.array([0.1, 0.2, 0.05, 0.3, 0.85, 0.15, 0.25, 0.92, 0.88, 0.95])

def print_evaluation_report(name: str, y_true, y_pred, y_probs=None):
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print("\n" + "="*50)
    print(f"📊 EVALUATION REPORT: {name.upper()}")
    print("="*50)
    print(f"Confusion Matrix: [TP: {tp}, FP: {fp}, FN: {fn}, TN: {tn}]")
    print(f"Raw Accuracy    : {np.mean(y_true == y_pred) * 100:.1f}%")
    print(f"Precision (PPV) : {precision_score(y_true, y_pred, zero_division=0) * 100:.1f}%")
    print(f"Recall (Catch)  : {recall_score(y_true, y_pred) * 100:.1f}%")
    print(f"F1-Score        : {f1_score(y_true, y_pred, zero_division=0):.3f}")
    if y_probs is not None:
        print(f"ROC-AUC Score   : {roc_auc_score(y_true, y_probs):.3f}")
    print("="*50)

print_evaluation_report("Dumb Baseline (Predict All Zeros)", actual_transactions, model_lazy_preds)
print_evaluation_report("Production Fraud Classifier", actual_transactions, model_ml_preds, model_ml_probs)
```

---

## 8. Interview Quick-Fire Questions

1. **Q: In medical cancer diagnosis, would you optimize for Precision or Recall? Why?**
   - **Answer**: You must optimize for **Recall**. A False Negative (predicting a sick person is healthy) means cancer goes undetected and the patient may die. A False Positive (predicting a healthy person has cancer) only causes temporary stress resolved by follow-up tests.
2. **Q: What is the Bias-Variance tradeoff?**
   - **Answer**: **High Bias (Underfitting)** occurs when a model is too simplistic to capture the underlying data patterns (high training error, high test error). **High Variance (Overfitting)** occurs when a model memorizes random noise in the training set (near-zero training error, high test error). The goal of machine learning is to find the sweet spot that minimizes total error.
3. **Q: Why is K-Fold Cross-Validation preferred over a single train/test split?**
   - **Answer**: A single train/test split is subject to sampling variance (luck of the split), especially on smaller datasets. K-Fold CV partitions the data into $K$ equal folds, iteratively training on $K-1$ folds and testing on the remaining fold. Averaging across all $K$ iterations provides an unbiased estimate of the model's true generalization performance.
