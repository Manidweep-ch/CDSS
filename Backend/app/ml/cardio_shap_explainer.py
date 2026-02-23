import shap
import numpy as np
from app.ml.cardio_model_loader import CardioModelLoader


class CardioSHAPExplainer:

    _explainer = None

    @classmethod
    def _initialize(cls):
        if cls._explainer is None:
            calibrated_model = CardioModelLoader.load_model()

            # Get first fitted base estimator from calibration
            if hasattr(calibrated_model, "calibrated_classifiers_"):
                base_model = calibrated_model.calibrated_classifiers_[0].estimator
            else:
                raise RuntimeError("Calibrated model not properly fitted.")

            cls._explainer = shap.TreeExplainer(base_model)

    @classmethod
    def explain(cls, patient_features: dict, top_n: int = 5):

        cls._initialize()
        metadata = CardioModelLoader.load_metadata()

        feature_order = metadata["features"]

        # Safe feature extraction
        feature_vector = np.array([
            [patient_features.get(f, 0) for f in feature_order]
        ])

        shap_values = cls._explainer.shap_values(feature_vector)

        contributions = {
            feature_order[i]: float(shap_values[0][i])
            for i in range(len(feature_order))
        }

        sorted_features = sorted(
            contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:top_n]

        return {
            "top_feature_contributions": [
                {
                    "feature": f,
                    "impact": round(val, 5),
                    "direction": "increase" if val > 0 else "decrease"
                }
                for f, val in sorted_features
            ]
        }
