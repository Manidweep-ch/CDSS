# ============================================
# Diabetes ML Predictor (Inference Layer)
# Responsible ONLY for ML predictions
# ============================================

import numpy as np
from app.ml.diabetes_model_loader import DiabetesModelLoader


class DiabetesPredictor:
    """
    Handles ML inference using calibrated diabetes model.
    """

    @staticmethod
    def predict(patient_features: dict) -> dict:
        """
        Takes patient features as dictionary,
        returns calibrated probability + ML risk flag.
        """

        # Load model + metadata
        model = DiabetesModelLoader.load_model()
        metadata = DiabetesModelLoader.load_metadata()

        expected_features = metadata["features"]
        threshold = metadata["threshold"]

        # Ensure correct feature order
        feature_vector = []

        for feature in expected_features:
            feature_vector.append(patient_features.get(feature, 0))

        feature_array = np.array([feature_vector])

        # Predict probability with error handling
        try:
            probability = float(model.predict_proba(feature_array)[0][1])
        except Exception as e:
            # Fallback: try to get base estimator if calibrated model fails
            try:
                if hasattr(model, 'base_estimator'):
                    probability = float(model.base_estimator.predict_proba(feature_array)[0][1])
                elif hasattr(model, 'estimator'):
                    probability = float(model.estimator.predict_proba(feature_array)[0][1])
                else:
                    raise Exception(f"Model prediction failed: {str(e)}")
            except:
                raise Exception(f"XGBClassifier calibration error: {str(e)}. Model may need retraining with current sklearn version.")

        # Threshold classification
        if probability >= threshold:
            risk_flag = "Elevated ML Risk"
        else:
            risk_flag = "Low/Moderate ML Risk"

        return {
            "ml_probability": round(probability, 4),
            "ml_threshold": threshold,
            "ml_risk_flag": risk_flag,
            "model_version": metadata.get("model_version", "Unknown")
        }
