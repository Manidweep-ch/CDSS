# ============================================
# Kidney SHAP Explainer (NumPy Compatible)
# ============================================

import shap
import numpy as np
from app.ml.kidney_model_loader import KidneyModelLoader


class KidneyShapExplainer:

    _explainer = None
    _base_model = None
    _metadata = None

    @classmethod
    def _initialize(cls):

        if cls._explainer is None:

            calibrated_model = KidneyModelLoader.load_model()
            cls._metadata = KidneyModelLoader.load_metadata()

            # Get base model from calibrated model
            cls._base_model = calibrated_model.estimator
            classifier = cls._base_model.named_steps["classifier"]

            cls._explainer = shap.TreeExplainer(classifier)

    @classmethod
    def explain(cls, data: dict, top_n: int = 5):

        cls._initialize()

        feature_order = cls._metadata["features"]

        # Create feature vector using numpy
        feature_vector = [data.get(feature, 0) for feature in feature_order]
        feature_array = np.array([feature_vector], dtype=np.float64)

        try:
            # Apply preprocessing
            processed = cls._base_model.named_steps["preprocessing"].transform(feature_array)

            shap_values = cls._explainer.shap_values(processed)
            contributions = shap_values[0]

            top_indices = np.argsort(abs(contributions))[::-1][:top_n]

            return {
                "top_feature_contributions": [
                    {
                        "feature_index": int(idx),
                        "impact": float(round(contributions[idx], 5))
                    }
                    for idx in top_indices
                ]
            }
        except Exception as e:
            return {
                "top_feature_contributions": [],
                "error": f"SHAP explanation failed: {str(e)}"
            }
