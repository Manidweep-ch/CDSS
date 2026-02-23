import numpy as np
from app.ml.cardio_model_loader import CardioModelLoader


class CardioPredictor:

    @staticmethod
    def predict(patient_features: dict):

        model = CardioModelLoader.load_model()
        metadata = CardioModelLoader.load_metadata()

        feature_order = metadata["features"]
        threshold = metadata["threshold"]

        # Safe feature extraction (no crash if missing)
        feature_vector = [
            patient_features.get(f, 0)
            for f in feature_order
        ]

        feature_array = np.array([feature_vector])

        try:
            probability = float(model.predict_proba(feature_array)[0][1])
        except Exception as e:
            # Fallback for calibrated model issues
            try:
                if hasattr(model, 'base_estimator'):
                    probability = float(model.base_estimator.predict_proba(feature_array)[0][1])
                elif hasattr(model, 'estimator'):
                    probability = float(model.estimator.predict_proba(feature_array)[0][1])
                else:
                    raise Exception(f"Model prediction failed: {str(e)}")
            except:
                raise Exception(f"Cardio model error: {str(e)}. Model may need retraining.")

        return {
            "probability": round(probability, 4),
            "threshold": round(threshold, 4),
            "above_threshold": probability >= threshold,
            "model_version": metadata["model_version"]
        }
