# ============================================
# Kidney Predictor (NumPy Compatible)
# ============================================

import numpy as np
from app.ml.kidney_model_loader import KidneyModelLoader


class KidneyPredictor:

    @staticmethod
    def predict(data: dict):

        model = KidneyModelLoader.load_model()
        metadata = KidneyModelLoader.load_metadata()

        expected_features = metadata["features"]
        threshold = metadata.get("threshold", 0.5)

        # Create feature vector in correct order
        feature_vector = []
        for feature in expected_features:
            value = data.get(feature, 0)
            try:
                feature_vector.append(float(value) if value is not None else 0.0)
            except (ValueError, TypeError):
                feature_vector.append(0.0)
        
        # Use numpy array directly
        feature_array = np.array([feature_vector], dtype=np.float64)

        try:
            # Model is calibrated, use directly
            probability = float(model.predict_proba(feature_array)[0][1])
        except Exception as e:
            # Fallback for calibrated model
            try:
                if hasattr(model, 'estimator'):
                    probability = float(model.estimator.predict_proba(feature_array)[0][1])
                else:
                    raise Exception(f"Model prediction failed: {str(e)}")
            except:
                raise Exception(f"Kidney model error: {str(e)}")

        return {
            "ml_probability": round(probability, 4),
            "ml_threshold": threshold,
            "ml_risk_flag": "High" if probability >= threshold else "Low",
            "model_version": metadata.get("model_version")
        }
