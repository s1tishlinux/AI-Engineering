# డే 18 (Day 18): మోడల్ ట్రైనింగ్ & ఎవాల్యుయేషన్ మెట్రిక్స్ (Model Evaluation & Metrics)

## 🎯 ఈ సెషన్ లక్ష్యాలు (Learning Objectives)
ఈ క్లాస్ పూర్తయ్యేసరికి మీరు క్రింది అంశాలను చాలా స్పష్టంగా అర్థం చేసుకుంటారు:
1. ఫీచర్ ఇంజనీరింగ్ పైప్‌లైన్లు: `StandardScaler`, `OneHotEncoder` మరియు Scikit-Learn `Pipeline`.
2. డేటాను సురక్షితంగా విభజించడం: స్ట్రాటిఫైడ్ `train_test_split`.
3. **బయాస్-వేరియన్స్ ట్రేడ్‌ఆఫ్**: ఓవర్‌ఫిట్టింగ్ vs అండర్‌ఫిట్టింగ్ గుర్తించడం.
4. క్రాస్-వాలిడేషన్: **K-Fold Cross-Validation** ఎందుకు అత్యంత నమ్మకమైనది?
5. క్లాసిఫికేషన్ మెట్రిక్స్: **కన్‌ఫ్యూజన్ మ్యాట్రిక్స్**, **Accuracy**, **Precision**, **Recall**, **F1-Score** మరియు **ROC-AUC**.
6. రిగ్రెషన్ మెట్రిక్స్: **MAE**, **RMSE**, మరియు **$R^2$ స్కోర్**.
7. `GridSearchCV` ద్వారా ఆటోమేటిక్‌గా బెస్ట్ సెట్టింగ్స్ కనుగొనడం.

---

## 1. "ఖచ్చితత్వం (Accuracy)" ఒక ప్రమాదకరమైన అబద్ధం! (The "Why")

ఒక ఉదాహరణ చూద్దాం: ఒక అరుదైన క్యాన్సర్ వ్యాధి 1,000 మందిలో కేవలం ఒక్కరికి (0.1%) మాత్రమే వస్తుంది.
మీరు ఒక మోడల్ తయారు చేశారు. అది ఏ పరీక్షా చేయకుండా, వచ్చిన ప్రతి రోగికీ **"ఆరోగ్యంగా ఉన్నారు"** అని మాత్రమే సమాధానం ఇస్తుంది!
- ఇప్పుడు ఆ మోడల్ యొక్క రా **Accuracy ఎంతంటే: 99.9%!**
- కానీ వాస్తవానికి ఆ మోడల్ వల్ల **ఎలాంటి ఉపయోగం లేదు!** ఆ ఒక్క రోగికి వ్యాధి గుర్తించకపోవడం వల్ల ఆ వ్యక్తి ప్రాణం పోతుంది.

రియల్ వరల్డ్ ప్రాజెక్టులలో **కేవలం Accuracy చూసి మోసపోతే ఉద్యోగం పోతుంది!** అందుకే మనం **Precision, Recall, F1-Score మరియు ROC-AUC** లను తప్పకుండా నేర్చుకోవాలి.

---

## 2. కన్‌ఫ్యూజన్ మ్యాట్రిక్స్ (Confusion Matrix)

రెండు క్లాసుల సమస్యలో (Positive = 1, Negative = 0):

```
                        నిజమైన పరిస్థితి (ACTUAL)
                    క్యాన్సర్ ఉంది (1)    క్యాన్సర్ లేదు (0)
మోడల్      ఉంది (1) [ True Positive ]   [ False Positive ]  <-- టైప్ 1 ఎర్రర్ (తప్పుడు అలారం)
చెప్పినది  లేదు (0) [ False Negative ]  [ True Negative ]   <-- టైప్ 2 ఎర్రర్ (వ్యాధిని గుర్తించకపోవడం!)
```

### నాలుగు ముఖ్యమైన మెట్రిక్స్:
1. **Accuracy (మొత్తం ఖచ్చితత్వం):** మొత్తం కేసులలో మోడల్ ఎన్ని సరైన సమాధానాలు చెప్పింది?
   $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
2. **Precision (ఖచ్చితమైన గుర్తింపు):** మోడల్ పాజిటివ్ అని చెప్పిన వాటిలో నిజంగా ఎన్ని పాజిటివ్ ఉన్నాయి? (స్పామ్ ఫిల్టర్లలో ఇది ముఖ్యం; మంచి ఈమెయిల్ స్పామ్‌లోకి వెళ్లకూడదు).
   $$\text{Precision} = \frac{TP}{TP + FP}$$
3. **Recall (వ్యాప్తి / రికాల్):** సమాజంలో ఉన్న మొత్తం రోగులలో మోడల్ ఎంతమందిని పట్టుకోగలిగింది? (క్యాన్సర్ నిర్ధారణ, మోసాల గుర్తింపులో రికాల్ అత్యంత ముఖ్యం!).
   $$\text{Recall} = \frac{TP}{TP + FN}$$
4. **F1-Score:** Precision మరియు Recall రెండింటి సగటు (హార్మోనిక్ మీన్). డేటా అసమానంగా ఉన్నప్పుడు ఇదే బెస్ట్ మెట్రిక్.
   $$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

---

## 3. డేటా పైప్‌లైన్ (Pipeline) & ప్రీ-ప్రాసెసింగ్

డేటా లీకేజ్ జరగకుండా ఒకే పద్ధతిలో కోడ్ రాయడానికి Scikit-Learn `Pipeline` వాడతాం:

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# శాంపిల్ బ్యాంక్ కస్టమర్ డేటా
data = pd.DataFrame({
    "credit_score": [720, 580, 810, 640, 700, 550, 780, 610, 690, 730],
    "account_age": [3.5, 1.0, 5.0, 2.0, 4.0, 0.5, 6.0, 1.5, 3.0, 4.5],
    "country": ["India", "USA", "India", "UK", "USA", "India", "UK", "USA", "India", "UK"],
    "churned": [0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
})

X = data.drop(columns=["churned"])
y = data["churned"]

# 1. స్ట్రాటిఫైడ్ స్ప్లిట్ (ట్రైన్ మరియు టెస్ట్ లోనూ సమాన నిష్పత్తిలో 0, 1 లు ఉండేలా చేస్తుంది)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 2. కాలమ్ ట్రాన్స్‌ఫార్మర్ (నంబర్లను స్కేల్ చేయడం, టెక్స్ట్‌ను నంబర్లుగా మార్చడం)
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), ["credit_score", "account_age"]),
        ("cat", OneHotEncoder(drop="first"), ["country"])
    ]
)

# 3. ఒకే పైప్‌లైన్‌లో కలపడం
clf_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(random_state=42))
])
```

---

## 4. `GridSearchCV` తో బెస్ట్ సెట్టింగ్స్ కనుగొనడం

మోడల్‌కి ఎన్ని చెట్లు పెట్టాలి (`n_estimators`), డెప్త్ ఎంత ఉండాలి అని మనం ఊహించాల్సిన పనిలేదు. `GridSearchCV` అన్ని రకాల కాంబినేషన్లను టెస్ట్ చేసి బెస్ట్ మోడల్‌ను ఎంపిక చేస్తుంది:

```python
param_grid = {
    "classifier__n_estimators": [10, 50],
    "classifier__max_depth": [2, 4]
}

# 3-Fold క్రాస్ వాలిడేషన్‌తో గ్రిడ్ సెర్చ్ రన్ చేయడం
grid_search = GridSearchCV(clf_pipeline, param_grid, cv=3, scoring="f1")
grid_search.fit(X_train, y_train)

print(f"ఉత్తమ సెట్టింగ్స్: {grid_search.best_params_}")
print(f"ఉత్తమ F1-స్కోర్: {grid_search.best_score_:.2f}")

# టెస్ట్ డేటాపై పరీక్షించడం
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print("\n--- టెస్ట్ సెట్ ఫలితాల నివేదిక ---")
print(classification_report(y_test, y_pred, zero_division=0))
```

---

## 5. రిగ్రెషన్ మెట్రిక్స్ (సంఖ్యలను అంచనా వేసేటప్పుడు)

మీరు ఇంటి ధర లేదా స్టాక్ మార్కెట్ నంబర్లను అంచనా వేస్తుంటే:
1. **MAE (Mean Absolute Error):** తప్పుల సగటు మొత్తం రూపాయల్లో.
2. **RMSE (Root Mean Squared Error):** పెద్ద తప్పులను ఎక్కువగా శిక్షిస్తుంది (స్క్వేర్ చేయడం వల్ల).
3. **$R^2$ Score:** మీ మోడల్ డేటాను ఎంతవరకు వివరించగలిగింది (1.0 అంటే పర్ఫెక్ట్ మోడల్, 0.0 అంటే సగటు మోడల్).

---

## 6. ఫ్రెషర్స్ చేసే సాధారణ తప్పులు (Common Pitfalls)

1. **ట్రైనింగ్ డేటాపై మాత్రమే టెస్ట్ చేయడం:** మోడల్ ట్రైనింగ్ డేటాను బట్టీ పట్టి 100% స్కోర్ సాధించి, కొత్త టెస్ట్ డేటాపై ఫెయిల్ అవ్వడాన్నే **ఓవర్‌ఫిట్టింగ్ (Overfitting)** అంటారు.
2. **అసమాన డేటాలో Accuracy ని నమ్మడం:** మోసాలు (Fraud) లేదా వ్యాధుల గుర్తింపులో Accuracy చూడకూడదు; **Recall లేదా F1-Score** మాత్రమే చూడాలి.
3. **టెస్ట్ డేటాపై స్కేలర్‌ను ఫిట్ చేయడం:** `scaler.fit(X_test)` ఎప్పుడూ కొట్టకూడదు! కేవలం ట్రైనింగ్ డేటా నుండి నేర్చుకున్న విలువలనే టెస్ట్ డేటాపై వాడాలి (`scaler.transform(X_test)`).

---

## 7. ప్రాక్టీస్ ల్యాబ్ (Daily Hands-On Lab)

### 🧪 టాస్క్: క్రెడిట్ కార్డు మోసాల గుర్తింపు రిపోర్ట్ కార్డు
**సన్నివేశం:** మీ కంపెనీ వైస్ ప్రెసిడెంట్‌కి మోడల్ పనితీరు రిపోర్ట్ ఇవ్వాలి. ఒక డమ్మీ మోడల్‌కి మరియు రియల్ ML మోడల్‌కి కన్‌ఫ్యూజన్ మ్యాట్రిక్స్, ప్రెసిషన్, రికాల్ మరియు ROC-AUC స్కోర్లు లెక్కించండి.

```python
# =========================================================
# Day 18 Lab: క్రెడిట్ కార్డ్ ఫ్రాడ్ డిటెక్షన్ రిపోర్ట్ కార్డ్
# =========================================================
import numpy as np
from sklearn.metrics import (
    confusion_matrix, precision_score, recall_score,
    f1_score, roc_auc_score
)

# అసలైన నిజం: 1 = ఫ్రాడ్ లావాదేవీ, 0 = సాధారణ లావాదేవీ
actual_transactions = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1, 1])

# మోడల్ 1: సోమరి మోడల్ (అన్నీ 0 అని చెప్పేసింది)
model_lazy_preds = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

# మోడల్ 2: నిజమైన ML మోడల్
model_ml_preds = np.array([0, 0, 0, 0, 1, 0, 0, 1, 1, 1])
model_ml_probs = np.array([0.1, 0.2, 0.05, 0.3, 0.85, 0.15, 0.25, 0.92, 0.88, 0.95])

def print_evaluation_report(name: str, y_true, y_pred, y_probs=None):
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print("\n" + "="*50)
    print(f"📊 పనితీరు నివేదిక: {name.upper()}")
    print("="*50)
    print(f"కన్‌ఫ్యూజన్ మ్యాట్రిక్స్: [TP: {tp}, FP: {fp}, FN: {fn}, TN: {tn}]")
    print(f"రా ఖచ్చితత్వం (Accuracy): {np.mean(y_true == y_pred) * 100:.1f}%")
    print(f"ప్రెసిషన్ (Precision)   : {precision_score(y_true, y_pred, zero_division=0) * 100:.1f}%")
    print(f"రికాల్ (Recall)         : {recall_score(y_true, y_pred) * 100:.1f}%")
    print(f"F1-స్కోర్ (F1-Score)     : {f1_score(y_true, y_pred, zero_division=0):.3f}")
    if y_probs is not None:
        print(f"ROC-AUC స్కోర్          : {roc_auc_score(y_true, y_probs):.3f}")
    print("="*50)

print_evaluation_report("సోమరి మోడల్ (అన్నీ సున్నాలు చెప్పినది)", actual_transactions, model_lazy_preds)
print_evaluation_report("నిజమైన ML ఫ్రాడ్ డిటెక్టర్", actual_transactions, model_ml_preds, model_ml_probs)
```

---

## 8. ఇంటర్వ్యూలలో అడిగే ప్రశ్నలు (Interview Questions & Answers)

1. **ప్రశ్న: క్యాన్సర్ రోగ నిర్ధారణలో ప్రెసిషన్ ముఖ్యమా లేక రికాల్ ముఖ్యమా? ఎందుకు?**
   - **సమాధానం:** ఖచ్చితంగా **రికాల్ (Recall)** అత్యంత ముఖ్యం! ఎందుకంటే ఫాల్స్ నెగటివ్ (రోగం ఉన్న వ్యక్తికి రోగం లేదని చెప్పడం) జరిగితే రోగికి చికిత్స అందక ప్రాణం పోతుంది. అదే ఫాల్స్ పాజిటివ్ (ఆరోగ్యంగా ఉన్న వ్యక్తికి అనుమానం రావడం) జరిగితే ఇంకోసారి పరీక్ష చేసి నిర్ధారించుకోవచ్చు.
2. **ప్రశ్న: బయాస్-వేరియన్స్ ట్రేడ్‌ఆఫ్ (Bias-Variance Tradeoff) అంటే ఏమిటి?**
   - **సమాధానం:** **హై బయాస్ (Underfitting)** అంటే మోడల్ చాలా సింపుల్‌గా ఉండి డేటాలోని అసలైన ప్యాటర్న్‌లను కూడా నేర్చుకోలేకపోవడం (ట్రైనింగ్‌లోనూ, టెస్టింగ్‌లోనూ ఎక్కువ ఎర్రర్స్ రావడం). **హై వేరియన్స్ (Overfitting)** అంటే మోడల్ ట్రైనింగ్ డేటాను కంఠస్థం చేసి, కొత్త టెస్ట్ డేటాపై ఘోరంగా ఫెయిల్ అవ్వడం. ఈ రెండింటి మధ్య సమతుల్యతను సాధించడమే ట్రేడ్‌ఆఫ్.
3. **ప్రశ్న: సింగిల్ train/test split కంటే K-Fold Cross-Validation ఎందుకు మంచిది?**
   - **సమాధానం:** ఒకేసారి డేటాను విడదీస్తే, కేవలం అదృష్టవశాత్తూ టెస్ట్ సెట్‌లో సులభమైన రికార్డులు పడటం వల్ల స్కోర్ ఎక్కువగా కనిపించే ప్రమాదం ఉంది. K-Fold లో మొత్తం డేటాను $K$ భాగాలుగా చేసి, ప్రతి భాగాన్ని ఒకసారి టెస్ట్ సెట్‌గా మారుస్తూ సగటు స్కోర్ లెక్కించడం వల్ల మోడల్ యొక్క నిజమైన సామర్థ్యం బయటపడుతుంది.
