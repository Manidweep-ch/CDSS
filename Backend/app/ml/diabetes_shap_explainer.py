# ============================================
# SHAP Explainability Layer
# ============================================

import shap
import numpy as np
import joblib
import os

from app.ml.diabetes_model_loader import BASE_DIR


MODEL_DIR = os.path.join(BASE_DIR, "models")
BASE_MODEL_FILE = os.path.join(MODEL_DIR, "diabetes_model_base_xgb_v2.pkl")
METADATA_FILE = os.path.join(MODEL_DIR, "diabetes_model_metadata_v2.pkl")


class DiabetesSHAPExplainer:

    _explainer = None
    _model = None
    _metadata = None

    @classmethod
    def _initialize(cls):
        if cls._explainer is None:
            cls._model = joblib.load(BASE_MODEL_FILE)
            cls._metadata = joblib.load(METADATA_FILE)
            cls._explainer = shap.TreeExplainer(cls._model)

    @classmethod
    def explain(cls, patient_features: dict, top_n: int = 5):
        cls._initialize()

        feature_order = cls._metadata["features"]

        feature_vector = [patient_features.get(f, 0) for f in feature_order]
        feature_array = np.array([feature_vector])

        shap_values = cls._explainer.shap_values(feature_array)

        contributions = {}

        for i, feature in enumerate(feature_order):
            contributions[feature] = float(shap_values[0][i])

        # Sort by absolute impact
        sorted_features = sorted(
            contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )

        top_features = sorted_features[:top_n]

        return {
            "top_feature_contributions": [
                {
                    "feature": f,
                    "impact": round(val, 5)
                }
                for f, val in top_features
            ]
        }
