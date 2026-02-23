import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_FILE = os.path.join(MODEL_DIR, "kidney_model_v2_calibrated.pkl")
METADATA_FILE = os.path.join(MODEL_DIR, "kidney_model_metadata_v2.pkl")


class KidneyModelLoader:

    _model = None
    _metadata = None

    @classmethod
    def load_model(cls):
        if cls._model is None:
            cls._model = joblib.load(MODEL_FILE)
        return cls._model

    @classmethod
    def load_metadata(cls):
        if cls._metadata is None:
            cls._metadata = joblib.load(METADATA_FILE)
        return cls._metadata
