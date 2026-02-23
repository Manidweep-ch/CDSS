# ============================================
# Diabetes Model Loader (ML Layer)
# Responsible ONLY for loading model artifacts
# ============================================

import os
import joblib


# Base directory (Backend root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_FILE = os.path.join(MODEL_DIR, "diabetes_model_v2_calibrated.pkl")
METADATA_FILE = os.path.join(MODEL_DIR, "diabetes_model_metadata_v2.pkl")


class ModelLoaderError(Exception):
    """Custom exception for ML model loading errors."""
    pass


class DiabetesModelLoader:
    """
    Singleton-style loader for Diabetes ML Model.
    Ensures model loads once and is reused.
    """

    _model = None
    _metadata = None

    @classmethod
    def load_model(cls):
        if cls._model is None:
            if not os.path.exists(MODEL_FILE):
                raise ModelLoaderError(f"Model file not found: {MODEL_FILE}")

            cls._model = joblib.load(MODEL_FILE)

        return cls._model

    @classmethod
    def load_metadata(cls):
        if cls._metadata is None:
            if not os.path.exists(METADATA_FILE):
                raise ModelLoaderError(f"Metadata file not found: {METADATA_FILE}")

            cls._metadata = joblib.load(METADATA_FILE)

        return cls._metadata
