# ============================================
# Kidney Panel – Calibrated XGBoost Training
# Fixed for pandas/sklearn compatibility
# ============================================

import os
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    confusion_matrix,
    f1_score
)

from xgboost import XGBClassifier


# --------------------------------------------------------
# 1️⃣ Load Dataset
# --------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "Data_set", "kidney_Dataset.csv")

df = pd.read_csv(DATASET_PATH)

print("=" * 60)
print("Kidney Model Training - Calibrated XGBoost")
print("=" * 60)
print(f"Dataset Loaded: {df.shape}")


# --------------------------------------------------------
# 2️⃣ Prepare Data
# --------------------------------------------------------

# Use only the 3 features we need
feature_cols = ["sc", "bu", "age"]  # serum_creatinine, blood_urea, age

X = df[feature_cols].fillna(0).values
y = (df["classification"] == "ckd").astype(int).values

print(f"Features: {feature_cols}")
print(f"Samples: {len(X)}, CKD: {y.sum()}, Not CKD: {len(y)-y.sum()}")


# --------------------------------------------------------
# 3️⃣ Split Data
# --------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print(f"Train: {len(X_train)}, Test: {len(X_test)}")


# --------------------------------------------------------
# 4️⃣ Build Pipeline
# --------------------------------------------------------

base_model = Pipeline([
    ("preprocessing", StandardScaler()),
    ("classifier", XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42,
        use_label_encoder=False
    ))
])

print("\nTraining base model...")
base_model.fit(X_train, y_train)

train_acc = base_model.score(X_train, y_train)
test_acc = base_model.score(X_test, y_test)
print(f"Base Model - Train: {train_acc:.4f}, Test: {test_acc:.4f}")


# --------------------------------------------------------
# 5️⃣ Calibration
# --------------------------------------------------------

print("\nCalibrating model...")
calibrated_model = CalibratedClassifierCV(
    base_model,
    method="sigmoid",
    cv=3
)

calibrated_model.fit(X_train, y_train)

cal_acc = calibrated_model.score(X_test, y_test)
print(f"Calibrated Model - Test: {cal_acc:.4f}")


# --------------------------------------------------------
# 6️⃣ Evaluation
# --------------------------------------------------------

y_prob = calibrated_model.predict_proba(X_test)[:, 1]
y_pred = calibrated_model.predict(X_test)

auc = roc_auc_score(y_test, y_prob)
print(f"AUC: {auc:.4f}")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------------------------------
# 7️⃣ Threshold Optimization
# --------------------------------------------------------

best_threshold = 0.5
best_f1 = 0

for t in np.arange(0.3, 0.7, 0.01):
    preds = (y_prob >= t).astype(int)
    score = f1_score(y_test, preds)
    if score > best_f1:
        best_f1 = score
        best_threshold = t

print(f"Optimal Threshold: {best_threshold:.3f} (F1: {best_f1:.4f})")


# --------------------------------------------------------
# 8️⃣ Save Models
# --------------------------------------------------------

MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Save base model for SHAP
joblib.dump(base_model, os.path.join(MODEL_DIR, "kidney_model_base_xgb_v2.pkl"))

# Save calibrated model for predictions
joblib.dump(calibrated_model, os.path.join(MODEL_DIR, "kidney_model_v2_calibrated.pkl"))

# Save metadata with display names
metadata = {
    "model_version": "v2_calibrated",
    "threshold": float(best_threshold),
    "auc": float(auc),
    "test_accuracy": float(cal_acc),
    "model_type": "XGBoost + Sigmoid Calibration",
    "features": ["serum_creatinine", "blood_urea", "age"]  # Display names for API
}

joblib.dump(metadata, os.path.join(MODEL_DIR, "kidney_model_metadata_v2.pkl"))

print("\n" + "=" * 60)
print("✅ Kidney models saved successfully!")
print("=" * 60)
print(f"Calibrated Model: kidney_model_v2_calibrated.pkl")
print(f"Base Model: kidney_model_base_xgb_v2.pkl")
print(f"Metadata: kidney_model_metadata_v2.pkl")
