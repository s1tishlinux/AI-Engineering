# Day 33: MLOps బేసిక్స్ & MLflow ఎక్స్‌పెరిమెంట్ ట్రాకింగ్ 📊

---

## 1. ఈ రోజు మన గోల్స్ (Day 33 Learning Objectives)
- సాధారణ సాఫ్ట్‌వేర్ ఇంజనీరింగ్ కి మరియు మెషిన్ లెర్నింగ్ కి మధ్య గల తేడా: **DevOps vs MLOps vs LLMOps**.
- MLOps లోని 4 మూలస్తంభాలు: **Data Versioning**, **Experiment Tracking**, **Model Registry**, మరియు **Automated Deployment**.
- **MLflow** టూల్ ను నేర్చుకోవడం: పారామీటర్లు (`learning_rate`), మెట్రిక్స్ (`accuracy`, `AUC`), మరియు ఆర్టిఫాక్ట్స్ ను ట్రాక్ చేయడం.
- మోడల్ జీవిత చక్రం (Model Lifecycle): `Staging -> Production -> Archived` స్టేజ్‌లను మరియు అప్రూవల్ గేట్లను అర్థం చేసుకోవడం.
- "నా లాప్‌టాప్ లోని Jupyter Notebook లో బాగా పనిచేసింది, కానీ సర్వర్ లో పనిచేయడం లేదు" అనే సమస్యను MLOps ద్వారా శాశ్వతంగా ఎలా పరిష్కరించవచ్చో తెలుసుకోవడం.

---

## 2. రియల్ వరల్డ్ అనలాజీ (Real-World Analogy)

> 💡 **అనలాజీ: ఇంట్లో ఒక కేక్ తయారుచేయడం vs ఆధునిక కేక్ ఫ్యాక్టరీ నడపడం**
>
> - **సాధారణ జూపిటర్ నోట్‌బుక్ (ఇంట్లో కేక్ చేయడం):**
>   ఒక వ్యక్తి ఇంట్లో సరదాగా కేక్ చేస్తున్నాడు. కొలతలు లేకుండా కొద్దిగా పంచదార, మైదా, ఉప్పు వేసి ఓవెన్ లో పెట్టాడు. కేక్ చాలా రుచిగా వచ్చింది! కానీ వారం తర్వాత ఒక కస్టమర్ వచ్చి "నాకు అచ్చం అలాంటి కేకే 100 కావాలి" అని అడిగాడు. ఆ వ్యక్తికి గుర్తులేదు: ఎన్ని గుడ్లు వాడాడు? ఎన్ని నిమిషాలు బేక్ చేశాడు? పంచదార ఎంత వేశాడు? దీనివల్ల రెండోసారి కేక్ నాణ్యత పూర్తిగా పాడైపోతుంది.
> - **MLOps (ఆధునిక పారిశ్రామిక ఫ్యాక్టరీ):**
>   ఒక పెద్ద బేకరీ ఫ్యాక్టరీలో ప్రతి బ్యాచ్ కీ:
>   - **ఖచ్చితమైన బ్యాచ్ నంబర్ ఉంటుంది (Git Commit & Data Version)**
>   - **ప్రతి పదార్ధాన్ని మిల్లీగ్రాములతో సహా సిస్టమ్ లో లాగ్ చేస్తారు (Hyperparameters)**
>   - **ఓవెన్ ఉష్ణోగ్రత గ్రాఫ్ ప్రతి సెకను రికార్డ్ అవుతుంది (Training Metrics)**
>   - **క్వాలిటీ ఇన్‌స్పెక్టర్ టెస్ట్ చేసి సీల్ వేస్తాడు (Model Evaluation & Registry)**
>   ఏదైనా కేక్ పాడైతే, ఏ పిండి వల్ల లేదా ఏ ఓవెన్ వల్ల సమస్య వచ్చిందో ఒక్క నిమిషంలో కనిపెట్టవచ్చు! ఇదే MLOps!

---

## 3. DevOps vs MLOps vs LLMOps మధ్య పోలిక

```
┌─────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│ అంశం            │ సాంప్రదాయ DevOps                │ MLOps (మెషిన్ లెర్నింగ్)         │ LLMOps / GenAIOps (జనరేటివ్ AI)  │
├─────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ ముఖ్యమైన అసెట్  │ Code (కోడ్ మాత్రమే)             │ Code + Data + Model Weights      │ Code + Data + Prompts + LLM      │
│ ఫలితం (Output)  │ నిర్దిష్టమైనది (Deterministic)   │ సంభావ్యత ఆధారితం (Probabilistic) │ అనూహ్యమైన నేచురల్ లాంగ్వేజ్ టెక్స్ట్│
│ మార్పులకు కారణం │ కొత్త ఫీచర్ లేదా కోడ్ లో బగ్     │ Data Drift (డేటా మారడం), డ్రిఫ్ట్ │ ప్రాంప్ట్ మార్పులు, హాలూసినేషన్లు │
│ టెస్టింగ్ ఫోకస్ │ Unit, Integration, Load Tests    │ Accuracy, ROC-AUC, Bias, Skew    │ Groundedness, Toxicity, Ragas    │
│ వాడే టూల్స్     │ Git, Docker, Kubernetes, Jenkins │ MLflow, DVC, Kubeflow, Feast     │ Langfuse, Ragas, Trulens, W&B    │
└─────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

---

## 4. MLflow ఆర్కిటెక్చర్ లోని 4 విభాగాలు

1. **MLflow Tracking:** మోడల్ ట్రైనింగ్ సమయంలో వాడిన పారామీటర్లు (`n_estimators`), మెట్రిక్స్ (`accuracy`, `loss`), మరియు గ్రాఫ్ ఇమేజ్‌లను డేటాబేస్ లో రికార్డ్ చేస్తుంది.
2. **MLflow Models:** ఏ ఫ్రేమ్‌వర్క్ లోనైనా (Scikit-Learn, PyTorch, TensorFlow) తయారైన మోడల్ ని ఒక స్టాండర్డ్ ఫార్మాట్ లో ప్యాక్ చేస్తుంది.
3. **MLflow Model Registry:** కంపెనీ మొత్తానికి ఒకే సెంట్రల్ మోడల్ హబ్. ఇందులో మోడల్ వర్షన్లు (`v1`, `v2`) ఉంటాయి. ఏ వర్షన్ `Production` లో ఉండాలి, ఏది `Staging` లో ఉండాలి అనేది ఇక్కడే నిర్ణయిస్తారు.
4. **MLflow Projects:** ఎవరైనా సరే ఒకే కమాండ్ తో ఆ కోడ్ ని రన్ చేసుకునేలా రీయూజబుల్ ఎన్విరాన్మెంట్ ని క్రియేట్ చేస్తుంది.

---

## 5. కోడింగ్ వాక్‌త్రూ: Python లో MLflow తో ట్రైనింగ్ & మోడల్ రిజిస్ట్రీ

కింది పూర్తి స్క్రిప్ట్ లో మోడల్ ట్రైన్ చేయడమే కాకుండా, ఫలితాలను లాగ్ చేసి, మోడల్ ని సెంట్రల్ రిజిస్ట్రీ లో ఎలా నమోదు చేయాలో చూద్దాం:

```python
# train_with_mlflow.py
import os
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, roc_auc_score
from mlflow.models.signature import infer_signature

# 1. ఎక్స్‌పెరిమెంట్ పేరు సెట్ చేద్దాం
EXPERIMENT_NAME = "cancer_prediction_project"
mlflow.set_experiment(EXPERIMENT_NAME)

def train_and_evaluate(n_estimators: int, max_depth: int):
    # 2. డేటా లోడ్ చేయడం
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. MLflow రన్ ప్రారంభం
    with mlflow.start_run(run_name=f"rf_trees_{n_estimators}_depth_{max_depth}") as run:
        print(f"\n🚀 MLflow Run ID: {run.info.run_id} ప్రారంభమైంది...")
        
        # Hyperparameters ని లాగ్ చేయడం
        mlflow.log_params({
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "train_samples": len(X_train),
            "test_samples": len(X_test)
        })

        # 4. మోడల్ ట్రైనింగ్
        clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        clf.fit(X_train, y_train)

        # 5. ఫలితాల మూల్యాంకనం (Evaluation)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)

        # Metrics ని లాగ్ చేయడం
        mlflow.log_metrics({
            "accuracy": acc,
            "precision": prec,
            "roc_auc": auc
        })
        print(f"📊 రిజల్ట్స్ -> Accuracy: {acc:.4f}, AUC: {auc:.4f}")

        # 6. ఫీచర్ ఇంపార్టెన్స్ ఫైల్ ని ఆర్టిఫాక్ట్ గా సేవ్ చేయడం
        importance_df = pd.DataFrame({
            "feature": X.columns,
            "importance": clf.feature_importances_
        }).sort_values(by="importance", ascending=False).head(5)
        
        importance_df.to_csv("top_5_features.csv", index=False)
        mlflow.log_artifact("top_5_features.csv")
        os.remove("top_5_features.csv")

        # 7. మోడల్ సిగ్నేచర్ (ఇన్‌పుట్/అవుట్‌పుట్ స్కీమా) & రిజిస్ట్రీ లో సేవ్
        signature = infer_signature(X_train, clf.predict(X_train))
        
        mlflow.sklearn.log_model(
            sk_model=clf,
            artifact_path="random_forest_model",
            signature=signature,
            registered_model_name="CancerDiagnosticModel"
        )
        print("✅ మోడల్ విజయవంతంగా MLflow Model Registry లో రిజిస్టర్ అయింది!")

if __name__ == "__main__":
    # రెండు వేర్వేరు హైపర్‌పారామీటర్లతో రన్ చేసి పోల్చి చూద్దాం
    print("--- మొదటి ప్రయోగం: చిన్న చెట్లు (Small Trees) ---")
    train_and_evaluate(n_estimators=10, max_depth=3)

    print("\n--- రెండవ ప్రయోగం: పెద్ద అడవి (Deep Forest) ---")
    train_and_evaluate(n_estimators=50, max_depth=8)
```

---

## 6. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు

| పొరపాటు | ఎందుకు సమస్య వస్తుంది? | సరైన పద్ధతి |
| :--- | :--- | :--- |
| **Model Signature ఇవ్వకపోవడం** | ఇన్పుట్ లో ఏ కాలమ్స్ రావాలో స్కీమా రికార్డ్ చేయకపోతే, రేపు ప్రొడక్షన్ లో వేరే డేటాటైప్ వచ్చినప్పుడు మోడల్ సైలెంట్ గా క్రాష్ అవుతుంది. | తప్పకుండా `infer_signature(X_train, y_train)` ఉపయోగించి మోడల్ తో పాటు స్కీమాను కూడా లాగ్ చేయాలి. |
| **భారీ డేటాసెట్లను MLflow సర్వర్ కి అప్‌లోడ్ చేయడం** | గిగాబైట్ల డేటా CSV లను `log_artifact` చేస్తే సర్వర్ డిస్క్ నిండిపోయి క్రాష్ అవుతుంది. | డేటాను S3/GCS లో ఉంచి, కేవలం దాని వర్షన్ హ్యాష్ లేదా లింక్ ని మాత్రమే MLflow పారామీటర్లలో లాగ్ చేయాలి. |
| **హార్డ్‌కోడెడ్ లోకల్ పాత్‌లు రాయడం** | `C:/Users/Satish/data.csv` అని రాస్తే, రేపు ఆ కోడ్ AWS క్లౌడ్ లో లేదా డాకర్ లో రన్ చేసినప్పుడు ఫైల్ దొరకక ఫెయిల్ అవుతుంది. | ఎల్లప్పుడూ రిలేటివ్ పాత్స్ లేదా ఎన్విరాన్మెంట్ వేరియబుల్స్ (`os.getenv`) మాత్రమే వాడాలి. |

---

## 7. ప్రాక్టికల్ ల్యాబ్ (Hands-on Lab)

### లక్ష్యం:
MLflow Client API ని ఉపయోగించి, ప్రాజెక్ట్ లో నమోదైన అన్ని రన్స్ లో ఏ మోడల్ కి అత్యధిక `roc_auc` స్కోరు వచ్చిందో కనిపెట్టే పైథాన్ స్క్రిప్ట్ రాయండి.

```python
# lab_day33_client.py
import mlflow

client = mlflow.tracking.MlflowClient()
experiment = client.get_experiment_by_name("cancer_prediction_project")

if experiment:
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.roc_auc DESC"],
        max_results=1
    )
    if runs:
        top_run = runs[0]
        print(f"🏆 టాప్ రన్ ఐడీ: {top_run.info.run_id}")
        print(f"అత్యుత్తమ AUC స్కోరు: {top_run.data.metrics['roc_auc']:.4f}")
        print(f"వాడిన పారామీటర్లు: {top_run.data.params}")
```

---

## 8. టాప్ 3 ఇంటర్వ్యూ ప్రశ్నలు & సమాధానాలు

### Q1: DevOps కి మరియు MLOps కి ప్రధాన తేడా ఏమిటి?
**సమాధానం:**
DevOps లో కేవలం సాఫ్ట్‌వేర్ కోడ్ (Code) మాత్రమే మారుతుంది, దాని ఫలితం ఖచ్చితంగా ఒకేలా ఉంటుంది (Deterministic). కానీ MLOps లో **Code + Data + Model Weights** అనే మూడు అంశాలుంటాయి. కోడ్ లో ఏ మార్పు చేయకపోయినా, బయట సమాజంలో మార్కెట్ డేటా మారితే (Data Drift) మోడల్ నాణ్యత తగ్గిపోతుంది. అందుకే MLOps లో నిరంతరం ఎక్స్‌పెరిమెంట్ ట్రాకింగ్, డేటా వర్షనింగ్ మరియు రీట్రైనింగ్ అవసరమవుతాయి.

### Q2: MLflow Model Registry ఎందుకు అవసరం?
**సమాధానం:**
మోడల్ ట్రైన్ అయిన తర్వాత అది ఏ దశలో ఉందో ట్రాక్ చేయడానికి Model Registry ఉపయోగపడుతుంది. కొత్తగా ట్రైన్ అయిన మోడల్ ని `Staging` లో పెట్టి టెస్టింగ్ టీమ్ పరిశీలిస్తుంది. అన్ని టెస్టులు పాస్ అయ్యాక దాన్ని `Production` కి మారుస్తారు. పాతబడిన మోడల్స్ ని `Archived` చేస్తారు. దీనివల్ల ప్రొడక్షన్ లో ఎల్లప్పుడూ అనుమతించబడిన ఉత్తమ మోడల్ మాత్రమే రన్ అవుతుంది.

### Q3: మోడల్ సిగ్నేచర్ (Model Signature) అంటే ఏమిటి?
**సమాధానం:**
మోడల్ కి ఇన్పుట్ గా ఏ కాలమ్స్ రావాలి (ఉదా: age: int, salary: float), అవుట్‌పుట్ గా ఏ విలువలు వస్తాయి అని నిర్వచించే డాక్యుమెంట్ ని Model Signature అంటారు. ప్రొడక్షన్ లో క్లయింట్లు తప్పుడు కాలమ్ పేర్లు పంపినప్పుడు ఎర్రర్ రాకుండా ముందే వాలిడేట్ చేయడానికి ఇది ఎంతో కీలకం.
