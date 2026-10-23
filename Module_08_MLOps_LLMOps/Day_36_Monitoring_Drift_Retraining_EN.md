# Day 36: Model Monitoring, Data Drift & Automated Retraining 📉

---

## 1. Day 36 Learning Objectives
- Master the fundamental failure modes of machine learning in production: **Data Drift (Covariate Shift)** vs. **Concept Drift**.
- Compute statistical drift detection metrics in Python: **Kolmogorov-Smirnov (KS) test**, **Wasserstein Distance**, and **Population Stability Index (PSI)**.
- Understand continuous production monitoring architecture: Logging inference payloads to data lakes (Parquet/BigQuery) and running scheduled drift jobs.
- Build automated **Retraining Triggers** and alerting pipelines when feature distributions diverge beyond acceptable safety bounds.
- Distinguish between Silent Failures (model returns HTTP 200 with garbage predictions) and Software Crashes (HTTP 500).

---

## 2. Real-World Analogy

> 💡 **Analogy: Autonomous Weather Radar vs. Seasonal Climate Change**
>
> - **Data Drift (Covariate Shift):**
>   Imagine you trained an AI in Dubai to predict when people need coats based on outdoor temperature (where it's usually 30°C to 45°C). Then you deploy that exact same AI to Alaska where temperatures drop to -20°C.
>   The relationship between temperature and coats didn't change (people still wear coats when cold), but the **input distribution ($P(X)$)** drifted drastically into values the model has never encountered before!
> - **Concept Drift:**
>   Imagine an AI trained to detect fraud during normal retail seasons. Suddenly, **Black Friday** arrives.
>   People are suddenly buying 20 items in 5 minutes from new IP addresses at 3:00 AM. In July, this was 99% fraudulent behavior; on Black Friday, this is 99% normal human shopper behavior!
>   The statistical relationship between the inputs and the target label ($P(Y|X)$) has flipped!

---

## 3. Types of Model Drift

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TYPES OF PRODUCTION DRIFT                       │
├────────────────────────────────────────────────────────────────────────┤
│ 1. DATA DRIFT (Covariate Shift)                                        │
│    - What changes: The distribution of inputs P(X) changes.            │
│    - Example: Camera sensor degrades, producing darker image pixels;   │
│      or an app marketing campaign attracts teenagers instead of adults.│
├────────────────────────────────────────────────────────────────────────┤
│ 2. CONCEPT DRIFT                                                       │
│    - What changes: The mathematical relationship between input and     │
│      target output P(Y|X) changes.                                     │
│    - Example: Inflation causes a ₹50,000 monthly income to represent a │
│      different credit risk profile today than it did 10 years ago.     │
├────────────────────────────────────────────────────────────────────────┤
│ 3. TARGET DRIFT (Prior Probability Shift)                              │
│    - What changes: The distribution of actual labels P(Y) changes.     │
│    - Example: COVID-19 pandemic causes infection test positivity rates │
│      to spike from 1% to 35% across the entire population.             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Architecture Overview: Automated Drift Detection & Retraining Loop

```
  Live User Request
         │
         ▼
┌────────────────────────┐
│  Inference Service     │
│  (FastAPI on K8s)      │
└────────┬───────────────┘
         │
         ├──────────────────────────────────────────┐
         ▼                                          ▼
   HTTP 200 Prediction                     Async Payload Streaming
         │                                 (Kafka / AWS Kinesis)
         ▼                                          │
   End User App                                     ▼
                                           ┌──────────────────────┐
                                           │  Inference Feature   │
                                           │  Store / Data Lake   │
                                           │  (S3 / Parquet)      │
                                           └──────────┬───────────┘
                                                      │
                       Nightly Cron Job (Airflow / Prefect)
                                                      │
                                                      ▼
                                           ┌──────────────────────┐
                                           │ Drift Detection Job  │
                                           │ (KS-Test / PSI)      │
                                           └──────────┬───────────┘
                                                      │
                                    Did Drift exceed threshold?
                                    ┌─────────────────┴─────────────────┐
                                    │ No                                │ Yes (P < 0.05 / PSI > 0.2)
                                    ▼                                   ▼
                             [Status: Green]                   ┌─────────────────────┐
                                                               │  1. Slack/Email Alert│
                                                               │  2. Trigger Retrain  │
                                                               │     Pipeline in CI/CD│
                                                               └─────────────────────┘
```

---

## 5. Coding Walkthrough: Python Drift Detection Engine (KS-Test & PSI)

Here is a standalone production drift calculator comparing production inference data against the reference baseline training set using the two-sample Kolmogorov-Smirnov test and Population Stability Index:

```python
# drift_detector.py
"""
Production Data Drift Detection Module
Methods:
  1. Kolmogorov-Smirnov (KS) Test for continuous numerical features.
  2. Population Stability Index (PSI) for binned distributions.
"""
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Any

def calculate_psi(baseline: np.ndarray, target: np.ndarray, num_buckets: int = 10) -> float:
    """
    Computes Population Stability Index (PSI) between baseline and production target.
    PSI < 0.1  -> No significant drift (Stable).
    PSI 0.1 - 0.2 -> Moderate drift (Warning).
    PSI > 0.2  -> Significant drift (Action Required).
    """
    # Create quantile buckets based on baseline
    percentiles = np.linspace(0, 100, num_buckets + 1)
    bucket_edges = np.percentile(baseline, percentiles)
    bucket_edges[0] -= 1e-5
    bucket_edges[-1] += 1e-5

    # Count frequencies
    base_counts, _ = np.histogram(baseline, bins=bucket_edges)
    target_counts, _ = np.histogram(target, bins=bucket_edges)

    # Convert to fractions with Laplace smoothing to avoid division by zero
    base_pct = (base_counts + 1e-4) / len(baseline)
    target_pct = (target_counts + 1e-4) / len(target)

    # PSI Formula: sum((Actual - Expected) * ln(Actual / Expected))
    psi_value = np.sum((target_pct - base_pct) * np.log(target_pct / base_pct))
    return float(psi_value)

class FeatureDriftMonitor:
    def __init__(self, p_value_threshold: float = 0.05, psi_threshold: float = 0.2):
        self.p_value_threshold = p_value_threshold
        self.psi_threshold = psi_threshold

    def analyze_feature(self, feature_name: str, baseline: np.ndarray, current: np.ndarray) -> Dict[str, Any]:
        # 1. Two-sample Kolmogorov-Smirnov Test
        # Null Hypothesis: The two distributions are identical.
        ks_stat, p_value = stats.ks_2samp(baseline, current)
        
        # 2. Population Stability Index
        psi_score = calculate_psi(baseline, current)

        # Drift Decision
        is_ks_drift = p_value < self.p_value_threshold
        is_psi_drift = psi_score >= self.psi_threshold
        drift_detected = is_ks_drift and is_psi_drift

        return {
            "feature": feature_name,
            "ks_statistic": round(ks_stat, 4),
            "p_value": round(p_value, 6),
            "psi_score": round(psi_score, 4),
            "drift_detected": drift_detected,
            "severity": "CRITICAL" if psi_score > 0.25 else ("WARNING" if psi_score > 0.1 else "NORMAL")
        }

if __name__ == "__main__":
    np.random.seed(42)

    # Simulate Baseline Training Data: Age of credit applicants (mean=38, std=8)
    training_age = np.random.normal(loc=38.0, scale=8.0, size=2000)

    # Scenario A: Normal Production Traffic (mean=38.2, std=8.1)
    stable_traffic_age = np.random.normal(loc=38.2, scale=8.1, size=1000)

    # Scenario B: Drifted Traffic due to Gen-Z student marketing campaign (mean=22.0, std=4.0)
    drifted_traffic_age = np.random.normal(loc=22.0, scale=4.0, size=1000)

    monitor = FeatureDriftMonitor()

    print("=== Scenario 1: Stable Production Traffic ===")
    res_stable = monitor.analyze_feature("applicant_age", training_age, stable_traffic_age)
    print(f"P-Value    : {res_stable['p_value']} (Threshold: > 0.05)")
    print(f"PSI Score  : {res_stable['psi_score']} (Threshold: < 0.2)")
    print(f"Drift State: {res_stable['severity']} | Drift Detected: {res_stable['drift_detected']}")

    print("\n=== Scenario 2: Severe Traffic Shift (Gen-Z Campaign) ===")
    res_drifted = monitor.analyze_feature("applicant_age", training_age, drifted_traffic_age)
    print(f"P-Value    : {res_drifted['p_value']} (Threshold: > 0.05)")
    print(f"PSI Score  : {res_drifted['psi_score']} (Threshold: < 0.2)")
    print(f"Drift State: {res_drifted['severity']} | Drift Detected: {res_drifted['drift_detected']}")

    if res_drifted["drift_detected"]:
        print("\n🚨 ACTION TRIGGERED: Firing webhook to trigger automated model retraining pipeline!")
```

---

## 6. Common Fresher Pitfalls

| Pitfall | Root Cause | Best Practice |
| :--- | :--- | :--- |
| **Confusing High Traffic with Data Drift** | Running statistical tests on small sample windows (e.g., 20 requests) yields volatile p-values and false alerts. | Aggregate inference traffic over statistically significant sample sizes (e.g., minimum 1,000 requests or 24-hour windows). |
| **Silent Failures: Relying solely on HTTP 200s** | Your inference microservice can return HTTP 200 OK continuously while predicting 0 for 100% of loans because an upstream engineer changed a date format string. | Monitor input feature summary statistics (mean, null percentage, quantiles) in addition to API uptime. |
| **Immediate Blind Retraining on Bad Data** | If an upstream API introduces an accidental bug producing garbage inputs, blindly retraining on that corrupted data will destroy your model. | Implement Data Quality & Integrity gates (Great Expectations) before feeding new production data into retraining jobs. |

---

## 7. Hands-on Lab: Automated Retraining Orchestrator

### Objective:
Write a workflow trigger function that evaluates drift metrics across 3 features (`age`, `income`, `debt_ratio`). If more than 50% of the features show severe drift, trigger an automated GitHub Actions webhook to retrain the model.

```python
# lab_day36_orchestrator.py
from typing import List, Dict

def evaluate_production_health(feature_reports: List[Dict[str, any]]) -> str:
    drifted_count = sum(1 for f in feature_reports if f.get("drift_detected"))
    total_features = len(feature_reports)
    drift_ratio = drifted_count / total_features

    print(f"Drift Analysis: {drifted_count}/{total_features} features drifted ({drift_ratio*100:.1f}%)")

    if drift_ratio >= 0.5:
        # Trigger Retrain Webhook (Simulated)
        return "🚀 TRIGGER_RETRAIN_PIPELINE"
    elif drift_ratio > 0:
        return "⚠️ SEND_SLACK_WARNING"
    return "✅ ALL_SYSTEMS_HEALTHY"

# Test evaluation
mock_reports = [
    {"feature": "age", "drift_detected": True},
    {"feature": "income", "drift_detected": True},
    {"feature": "debt_ratio", "drift_detected": False}
]
status = evaluate_production_health(mock_reports)
print("Action Decision:", status)
```

---

## 8. Top 3 Interview Questions & Answers

### Q1: What is the difference between Data Drift and Concept Drift?
**Answer:**
- **Data Drift (Covariate Shift):** Occurs when the statistical distribution of input features $P(X)$ changes over time, while the mapping from inputs to outputs $P(Y|X)$ remains constant. (e.g., users skewing younger over time).
- **Concept Drift:** Occurs when the underlying real-world relationship between inputs and outputs $P(Y|X)$ changes, even if input feature ranges look identical. (e.g., macroeconomic inflation making loan defaults more likely for people earning previously safe income levels).

### Q2: What is the Population Stability Index (PSI) and how are its thresholds interpreted?
**Answer:**
PSI measures how much a variable's distribution has shifted between a reference baseline dataset and a target production dataset.
Industry standard benchmark thresholds are:
- **PSI < 0.1:** Negligible shift; the population is stable.
- **0.1 $\le$ PSI < 0.2:** Moderate shift; requires monitoring and investigation.
- **PSI $\ge$ 0.2:** Significant distributional shift; requires immediate model retraining or intervention.

### Q3: Why is monitoring Ground Truth delayed in production ML, and how do you monitor models without labels?
**Answer:**
In many industries (e.g., credit card loan defaults or insurance claims), the true label $Y$ is only known months or years after the prediction was made. Therefore, real-time accuracy cannot be computed immediately. Instead, teams monitor proxy indicators:
1. **Input Feature Drift (KS-test / PSI):** Detecting if inputs deviate from training distributions.
2. **Prediction Drift:** Detecting if the distribution of model output probabilities changes (e.g., model suddenly predicting 80% positives instead of its historical 15%).
3. **Data Quality Metrics:** Tracking null values, unexpected category values, or data type schema violations.
