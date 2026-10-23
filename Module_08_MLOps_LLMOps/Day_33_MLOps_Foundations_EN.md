# Day 33: MLOps Foundations & Experiment Tracking with MLflow 📊

---

## 1. Day 33 Learning Objectives
- Demystify the progression: **DevOps vs. MLOps vs. LLMOps** — understanding how data and model nondeterminism fundamentally change engineering operations.
- The 4 core pillars of MLOps: **Data Versioning**, **Experiment Tracking**, **Model Registry**, and **Automated Deployment**.
- Master **MLflow**: Tracking parameters, metrics, artifacts, and model signatures.
- Understand the **Model Lifecycle**: `Staging -> Production -> Archived` with governance and approval gates.
- Prevent model decay, reproducibility failures, and "works on my Jupyter notebook" production disasters.

---

## 2. Real-World Analogy

> 💡 **Analogy: Baking a Single Cake vs. Running an Industrial Commercial Bakery**
>
> - **Jupyter Notebook (Hobby Baker):**
>   A baker is experimenting at home. They toss in a pinch of salt, a spoonful of sugar, turn the oven knob roughly to 180°C, and bake a delicious cake. But next week, a customer asks for the exact same cake. The baker has forgotten: Did they use 2 eggs or 3? How long was it baked? Why doesn't today's cake taste the same?
> - **MLOps (Industrial Factory):**
>   In a commercial bakery, every single batch has:
>   - **Exact Batch ID (Git commit & Data hash)**
>   - **Ingredient quantities logged down to the milligram (Hyperparameters)**
>   - **Oven temperature graphs recorded every second (Training Metrics)**
>   - **Quality control inspection score (Evaluation Accuracy)**
>   - **Strict labeling & seal of approval before leaving the loading dock (Model Registry)**
>   If a batch tastes wrong, managers can trace back precisely which flour supplier and oven temperature caused the defect within seconds!

---

## 3. DevOps vs. MLOps vs. LLMOps

```
┌─────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│ Dimension       │ Traditional DevOps               │ MLOps                            │ LLMOps / GenAIOps               │
├─────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ Core Asset      │ Code                             │ Code + Data + Model Weight       │ Code + Data + Prompt + Foundational Model │
│ Output          │ Deterministic binary / web app   │ Probabilistic predictions        │ Non-deterministic natural language / media│
│ Changes Driven  │ New feature / bug fix in code    │ Data drift, concept drift        │ Prompt drift, alignment, hallucination  │
│ Testing Focus   │ Unit, integration, load tests    │ Accuracy, ROC-AUC, bias, skew    │ Groundedness, toxicity, context recall  │
│ Tooling         │ Git, Jenkins, Docker, K8s        │ DVC, MLflow, Kubeflow, Feast     │ Langfuse, Ragas, Trulens, Weights&Biases│
└─────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

---

## 4. MLflow Architecture

MLflow provides 4 key components:
1. **MLflow Tracking:** Logs parameters (`learning_rate`, `n_estimators`), metrics (`accuracy`, `f1_score`), and artifacts (plots, pickle files, confusion matrix images).
2. **MLflow Models:** Standard packaging format allowing models trained in Scikit-Learn, PyTorch, or TensorFlow to be served via REST API, Docker, or Apache Spark.
3. **MLflow Model Registry:** Centralized collaborative model store with model lineage, versioning, stage transitions (`Staging` to `Production`), and annotations.
4. **MLflow Recipes / Projects:** Reusable, reproducible project structures with exact environment specifications.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MLFLOW TRACKING SERVER                          │
│                                                                        │
│   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
│   │     Backend Store (SQL)   │      │    Artifact Store (S3/GCS)  │   │
│   │ Runs, Params, Metrics, Tags│     │ Model Weights, Plots, Logs   │   │
│   └───────────────────────────┘      └─────────────────────────────┘   │
└──────────────────────────────▲─────────────────────────────────────────┘
                               │
            Logs Runs (mlflow.log_param / log_metric)
                               │
    ┌──────────────────────────┴──────────────────────────┐
    │                                                     │
┌───┴────────────────────────┐              ┌─────────────┴──────────────┐
│  Experiment 1: Baseline LR │              │ Experiment 2: XGBoost Tuned│
│  - max_depth: 3            │              │ - max_depth: 6             │
│  - accuracy: 0.81          │              │ - accuracy: 0.89           │
└────────────────────────────┘              └─────────────┬──────────────┘
                                                          │ Promoted
                                                          ▼
                                            ┌────────────────────────────┐
                                            │   MLFLOW MODEL REGISTRY    │
                                            │ "CustomerChurnClassifier"  │
                                            │ Version 2 -> PRODUCTION    │
                                            └────────────────────────────┘
```

---

## 5. Coding Walkthrough: Training, Tracking & Registering with MLflow

Here is a complete, production-ready script training a classification model, logging all metrics and artifacts, and registering the model into the MLflow registry:

```python
# train_and_track.py
"""
Production MLflow Experiment Tracking Walkthrough
Requirements:
  pip install mlflow scikit-learn pandas
"""
import os
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from mlflow.models.signature import infer_signature

# 1. Set Experiment Name
EXPERIMENT_NAME = "breast_cancer_diagnostic"
mlflow.set_experiment(EXPERIMENT_NAME)

def run_training_experiment(n_estimators: int, max_depth: int, min_samples_split: int):
    # 2. Load and split dataset
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Start MLflow Run context
    with mlflow.start_run(run_name=f"rf_trees_{n_estimators}_depth_{max_depth}") as run:
        print(f"Started MLflow Run: {run.info.run_id}")
        
        # Log Hyperparameters
        mlflow.log_params({
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "train_size": len(X_train),
            "test_size": len(X_test)
        })
        
        # Log Environment Tags
        mlflow.set_tags({
            "model_type": "RandomForest",
            "developer": "FresherAI",
            "framework": "scikit-learn"
        })

        # 4. Train Model
        clf = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=42
        )
        clf.fit(X_train, y_train)

        # 5. Evaluate Metrics
        preds = clf.predict(X_test)
        preds_proba = clf.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds)
        rec = recall_score(y_test, preds)
        auc = roc_auc_score(y_test, preds_proba)

        # Log Metrics
        mlflow.log_metrics({
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "roc_auc": auc
        })
        print(f"Metrics: Accuracy={acc:.4f}, AUC={auc:.4f}")

        # 6. Generate & Save Artifact (Feature Importances)
        feature_importance_df = pd.DataFrame({
            "feature": X.columns,
            "importance": clf.feature_importances_
        }).sort_values(by="importance", ascending=False).head(10)
        
        artifact_path = "top_features.csv"
        feature_importance_df.to_csv(artifact_path, index=False)
        mlflow.log_artifact(artifact_path)
        os.remove(artifact_path)  # cleanup local temp file

        # 7. Infer Model Signature (Inputs/Outputs Schema) & Log Model
        signature = infer_signature(X_train, clf.predict(X_train))
        
        # Log and Register Model in Registry
        mlflow.sklearn.log_model(
            sk_model=clf,
            artifact_path="random_forest_model",
            signature=signature,
            registered_model_name="DiagnosticClassifier"
        )
        print("Model and signature successfully logged to MLflow Registry!")

if __name__ == "__main__":
    # Run multiple experiments to compare hyperparameter performance
    print("=== Running Experiment 1: Small Forest ===")
    run_training_experiment(n_estimators=20, max_depth=3, min_samples_split=2)

    print("\n=== Running Experiment 2: Deep Forest ===")
    run_training_experiment(n_estimators=100, max_depth=10, min_samples_split=4)
```

---

## 6. Common Fresher Pitfalls

| Pitfall | Why It Causes Production Failure | How to Avoid |
| :--- | :--- | :--- |
| **No Model Signature (`infer_signature`)** | Saving a model without an input schema allows callers in production to send mismatched column names or invalid data types, failing silently or throwing 500 errors. | Always use `infer_signature(X_train, y_pred)` so MLflow records and validates the expected input dataframe schema. |
| **Logging Huge Datasets directly to MLflow** | Uploading 10GB raw CSVs via `mlflow.log_artifact` overwhelms the tracking server disk. | Track data hashes or URLs using DVC (Data Version Control) or cloud storage paths (S3/GCS URI), logging only the reference string in MLflow params. |
| **Hardcoding Local Paths in Saved Models** | If your preprocessing code contains `/Users/username/data.csv`, the model will crash immediately when deployed into a Docker container or AWS SageMaker. | Use relative paths or environment variables for all data and configuration access. |

---

## 7. Hands-on Lab: Hyperparameter Optimization with MLflow Comparison

### Objective:
Write a script that runs a grid of 4 combinations of `max_depth` (2, 5) and `n_estimators` (10, 50). Use the MLflow client to programmatically query the runs, find the run with the highest ROC-AUC score, and print its Run ID.

```python
# lab_day33_mlflow.py
import mlflow

client = mlflow.tracking.MlflowClient()
experiment = client.get_experiment_by_name("breast_cancer_diagnostic")

if experiment:
    # Query all runs ordered by metric
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.roc_auc DESC"],
        max_results=1
    )
    if runs:
        best_run = runs[0]
        print(f"🏆 Best Run ID: {best_run.info.run_id}")
        print(f"Top ROC-AUC: {best_run.data.metrics['roc_auc']:.4f}")
        print(f"Hyperparameters: {best_run.data.params}")
```

---

## 8. Top 3 Interview Questions & Answers

### Q1: What is the difference between DevOps and MLOps?
**Answer:**
DevOps focuses on standardizing and automating software code development, testing, and continuous integration/continuous deployment (CI/CD) where behavior is deterministic.
MLOps extends DevOps to manage the triad of **Code + Data + Model Weights**. Machine learning systems are probabilistic; even if the code does not change, changes in real-world data (data drift and concept drift) degrade model performance over time. MLOps introduces continuous training (CT), experiment tracking, data lineage, and model monitoring in production.

### Q2: What is the purpose of the MLflow Model Registry?
**Answer:**
The MLflow Model Registry provides a centralized hub to manage a model's full lifecycle. It tracks distinct versions of trained models, supports stage transitions (e.g., transitioning from `Staging` to `Production` or `Archived`), stores lineage back to the exact code commit and training experiment run, and enables governance approvals before models are deployed into production environments.

### Q3: Why is tracking Model Signatures critical in enterprise MLOps?
**Answer:**
A model signature defines the formal input and output schema (column names and data types, like `float64`, `int32`, `string`) for the model. Without a signature, if downstream clients deploy the model as a REST API and send an unexpected schema (such as missing a required feature or sending a string instead of a float), the model can fail catastrophically at runtime. Signatures enable automatic request payload validation before inference code executes.
