# ============================================
# Hybrid CDSS - Calibrated Diabetes ML Model
# ============================================

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    confusion_matrix,
    brier_score_loss
)
from sklearn.calibration import CalibratedClassifierCV
from xgboost import XGBClassifier


# -------------------------------
# 1. Load Dataset
# -------------------------------
print("Loading dataset...")
df = pd.read_csv("C:/Users/hp/Desktop/CDSS/Backend/Diabetics_Dataset.csv")

X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"]

# -------------------------------
# 2. Split Data
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

neg, pos = y_train.value_counts()
scale_weight = neg / pos

# -------------------------------
# 3. Base XGBoost Model
# -------------------------------
base_model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_weight,
    random_state=42,
    eval_metric='auc'
)

print("Training base model...")
base_model.fit(X_train, y_train)
# Save base model for SHAP explainability (v2)
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)



# -------------------------------
# 4. Calibration
# -------------------------------
print("Applying probability calibration...")

calibrated_model = CalibratedClassifierCV(
    base_model,
    method='sigmoid',
    cv=3
)

calibrated_model.fit(X_train, y_train)

# -------------------------------
# 5. Evaluation
# -------------------------------
y_prob = calibrated_model.predict_proba(X_test)[:, 1]
print("\n=== Threshold Scan (Calibrated) ===")

import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score

thresholds = np.arange(0.1, 0.7, 0.05)

for t in thresholds:
    y_pred_temp = (y_prob >= t).astype(int)
    precision = precision_score(y_test, y_pred_temp)
    recall = recall_score(y_test, y_pred_temp)
    f1 = f1_score(y_test, y_pred_temp)
    print(f"Threshold: {t:.2f} | Precision: {precision:.3f} | Recall: {recall:.3f} | F1: {f1:.3f}")

ROC = roc_auc_score(y_test, y_prob)
BRIER = brier_score_loss(y_test, y_prob)

# Updated production threshold (re-tune if needed)
PRODUCTION_THRESHOLD = 0.25

y_pred = (y_prob >= PRODUCTION_THRESHOLD).astype(int)

print("\n=== CALIBRATED MODEL PERFORMANCE ===")
print("ROC AUC:", round(ROC, 4))
print("Brier Score:", round(BRIER, 4))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# -------------------------------
# 6. Save Model + Metadata
# -------------------------------
# 1️⃣ Save base XGBoost model (for SHAP)
joblib.dump(
    base_model,
    os.path.join(MODEL_DIR, "diabetes_model_base_xgb_v2.pkl")
)

# 2️⃣ Save calibrated model (for production inference)
joblib.dump(
    calibrated_model,
    os.path.join(MODEL_DIR, "diabetes_model_v2_calibrated.pkl")
)

# 3️⃣ Save metadata (threshold + features + scores)
metadata = {
    "model_version": "v2",
    "calibrated": True,
    "threshold": PRODUCTION_THRESHOLD,
    "roc_auc": float(ROC),
    "brier_score": float(BRIER),
    "features": list(X.columns),
    "model_type": "XGBoost + Platt Calibration"
}

joblib.dump(
    metadata,
    os.path.join(MODEL_DIR, "diabetes_model_metadata_v2.pkl")
)

print("\n All v2 model artifacts saved successfully inside /models folder.")
