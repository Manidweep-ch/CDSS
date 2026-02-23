# ============================================
# Cardiovascular (10-Year CHD) Training Script
# Production Version (v3 - Stable Compatible)
# ============================================

import os
import joblib
import pandas as pd
import numpy as np
import xgboost as xgb

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, brier_score_loss, roc_curve
from sklearn.calibration import CalibratedClassifierCV


# ===============================
# 1. Load Dataset
# ===============================

DATA_PATH = "C:/Users/hp/Desktop/CDSS/Backend/Data_set/Cardiovascular_Dataset.csv"
df = pd.read_csv(DATA_PATH)

for col in df.columns:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())


# ===============================
# 2. Clinical Feature Engineering
# ===============================

df["pulse_pressure"] = df["sysBP"] - df["diaBP"]
df["mean_arterial_pressure"] = (2 * df["diaBP"] + df["sysBP"]) / 3
df["chol_age_interaction"] = df["totChol"] * df["age"]
df["smoking_intensity"] = df["cigsPerDay"] * df["currentSmoker"]
df["bmi_age_interaction"] = df["BMI"] * df["age"]
df["is_elderly"] = (df["age"] >= 60).astype(int)
df["is_stage2_htn"] = (df["sysBP"] >= 140).astype(int)


# ===============================
# 3. Features
# ===============================

features = [
    "male", "age", "education", "currentSmoker", "cigsPerDay",
    "BPMeds", "prevalentHyp", "diabetes",
    "totChol", "sysBP", "diaBP", "BMI", "heartRate", "glucose",
    "pulse_pressure",
    "mean_arterial_pressure",
    "chol_age_interaction",
    "smoking_intensity",
    "bmi_age_interaction",
    "is_elderly",
    "is_stage2_htn"
]

X = df[features]
y = df["TenYearCHD"]


# ===============================
# 4. 5-Fold CV (Stable)
# ===============================

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_auc_scores = []

for train_idx, val_idx in skf.split(X, y):

    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

    neg, pos = y_train.value_counts()
    scale_weight = neg / pos

    model = xgb.XGBClassifier(
        n_estimators=600,     # manually tuned
        max_depth=3,
        learning_rate=0.02,
        subsample=0.85,
        colsample_bytree=0.85,
        gamma=0.5,
        min_child_weight=5,
        reg_alpha=0.3,
        reg_lambda=1.2,
        scale_pos_weight=scale_weight,
        eval_metric="auc",
        random_state=42
    )

    model.fit(X_train, y_train)

    y_val_prob = model.predict_proba(X_val)[:, 1]
    fold_auc = roc_auc_score(y_val, y_val_prob)
    cv_auc_scores.append(fold_auc)

mean_cv_auc = float(np.mean(cv_auc_scores))


# ===============================
# 5. Train Final Model on Full Data
# ===============================

neg, pos = y.value_counts()
scale_weight = neg / pos

final_model = xgb.XGBClassifier(
    n_estimators=600,
    max_depth=3,
    learning_rate=0.02,
    subsample=0.85,
    colsample_bytree=0.85,
    gamma=0.5,
    min_child_weight=5,
    reg_alpha=0.3,
    reg_lambda=1.2,
    scale_pos_weight=scale_weight,
    eval_metric="logloss",
    random_state=42
)

final_model.fit(X, y)


# ===============================
# 6. Calibration
# ===============================

calibrated_model = CalibratedClassifierCV(
    final_model,
    method="sigmoid",
    cv=3
)

calibrated_model.fit(X, y)


# ===============================
# 7. Threshold (Sensitivity ≥ 0.75)
# ===============================

y_prob_full = calibrated_model.predict_proba(X)[:, 1]

fpr, tpr, thresholds = roc_curve(y, y_prob_full)

sensitivity_target = 0.75
valid_indices = np.where(tpr >= sensitivity_target)[0]

if len(valid_indices) > 0:
    best_index = valid_indices[0]
else:
    youden = tpr - fpr
    best_index = np.argmax(youden)

PRODUCTION_THRESHOLD = float(thresholds[best_index])
BRIER = float(brier_score_loss(y, y_prob_full))


# ===============================
# 8. Save Artifacts
# ===============================

BASE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(BASE_DIR)      # parent of BASE_DIR

MODEL_DIR = os.path.join(PARENT_DIR, "models")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

joblib.dump(calibrated_model, os.path.join(MODEL_DIR, "cardio_model_v3_calibrated.pkl"))

metadata = {
    "model_version": "v3",
    "mean_cv_auc": mean_cv_auc,
    "brier_score": BRIER,
    "threshold": PRODUCTION_THRESHOLD,
    "features": features,
    "model_type": "XGBoost + Platt Calibration (5-Fold CV)",
    "clinical_bias": "High Sensitivity (>=0.75)",
    "panel": "Cardiovascular",
    "target": "10-Year CHD Risk"
}

joblib.dump(metadata, os.path.join(MODEL_DIR, "cardio_model_metadata_v3.pkl"))

print("\nCardio v3 model training complete.")
print("Mean CV AUC:", round(mean_cv_auc, 4))
print("Brier Score:", round(BRIER, 4))
print("Production Threshold:", round(PRODUCTION_THRESHOLD, 4))
