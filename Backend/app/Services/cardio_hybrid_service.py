from datetime import datetime

from app.Rules.cardio_rules import analyze_cardio
from app.ml.cardio_predictor import CardioPredictor
from app.ml.cardio_shap_explainer import CardioSHAPExplainer


class CardioHybridService:

    SEVERITY_ORDER = ["Low", "Borderline", "Moderate", "Intermediate", "High"]

    @staticmethod
    def stratify_risk(prob):
        if prob < 0.05:
            return "Low"
        elif prob < 0.075:
            return "Borderline"
        elif prob < 0.20:
            return "Intermediate"
        else:
            return "High"

    @staticmethod
    def _normalize_rule_label(label):
        if label == "Moderate":
            return "Intermediate"
        return label

    @staticmethod
    def evaluate(patient_data: dict):

        # ===============================
        # Rule Engine
        # ===============================

        rule_result = analyze_cardio(
            totChol=patient_data.get("totChol"),
            hdl=patient_data.get("hdl"),
            triglycerides=patient_data.get("triglycerides"),
            sysBP=patient_data.get("sysBP"),
            diaBP=patient_data.get("diaBP"),
            age=patient_data.get("age"),
            sex=patient_data.get("sex")
        )

        rule_decision = rule_result.get("risk_level")
        rule_decision = CardioHybridService._normalize_rule_label(rule_decision)

        # ===============================
        # ML
        # ===============================

        ml_output = CardioPredictor.predict(patient_data)
        ml_probability = ml_output.get("probability")

        ml_risk_level = CardioHybridService.stratify_risk(ml_probability)

        shap_result = CardioSHAPExplainer.explain(patient_data)

        ml_result = {
            "ml_probability": ml_probability,
            "ml_threshold": 0.20,
            "ml_risk_flag": ml_risk_level,
            "model_version": "cardio_xgb_v1"
        }

        # ===============================
        # Override Logic
        # ===============================

        if rule_decision == "High":
            final_decision = "High"
            decision_source = "Rule Engine (Authoritative Override)"
            confidence = 1.0
            override_reason = "Clinical threshold exceeded per AHA/ACC guideline."
        else:

            severity_scale = ["Low", "Borderline", "Intermediate", "High"]

            final_decision = max(
                [rule_decision, ml_risk_level],
                key=lambda x: severity_scale.index(x)
            )

            decision_source = "Hybrid (Rule + ML Assist)"
            confidence = ml_probability
            override_reason = ""

        severity = rule_result.get("risk_level", final_decision)

        return {
            "panel": "Cardiovascular",
            "final_decision": final_decision,
            "decision_source": decision_source,
            "confidence": round(confidence, 4) if confidence is not None else None,
            "severity": severity,
            "rule_result": rule_result,
            "ml_result": ml_result,
            "ml_explainability": shap_result,
            "override_reason": override_reason,
            "model_version": ml_result["model_version"],
            "timestamp": datetime.utcnow().isoformat()
        }
