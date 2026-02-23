from datetime import datetime

from app.Rules.diabetes import analyze_diabetes
from app.ml.diabetes_predictor import DiabetesPredictor
from app.ml.diabetes_shap_explainer import DiabetesSHAPExplainer


class DiabetesHybridService:

    @staticmethod
    def evaluate(patient_data: dict) -> dict:

        rule_result = analyze_diabetes(
            fbs=patient_data.get("fasting_glucose_level"),
            hba1c=patient_data.get("HbA1c_level")
        )

        rule_decision = rule_result.get("risk_level")

        ml_result = DiabetesPredictor.predict(patient_data)
        shap_result = DiabetesSHAPExplainer.explain(patient_data)

        # Override case
        if rule_decision == "Diabetes":

            triggered_markers = {
                k: v for k, v in rule_result.get("markers", {}).items()
                if v.get("classification") == "Diabetes"
            }

            override_reason = (
                "Clinical diagnosis triggered due to threshold breach in: "
                + ", ".join(triggered_markers.keys())
            )

            final_decision = "Diabetes"
            decision_source = "Rule Engine (Authoritative Override)"
            confidence = 1.0

        else:
            final_decision = rule_decision
            decision_source = "Hybrid (Rule + ML Assist)"
            confidence = ml_result.get("ml_probability")
            override_reason = ""

        severity = rule_result.get("risk_level", final_decision)

        return {
            "panel": "Diabetes",
            "final_decision": final_decision,
            "decision_source": decision_source,
            "confidence": round(confidence, 4) if confidence is not None else None,
            "severity": severity,
            "rule_result": rule_result,
            "ml_result": ml_result,
            "ml_explainability": shap_result,
            "override_reason": override_reason,
            "model_version": ml_result.get("model_version"),
            "timestamp": datetime.utcnow().isoformat()
        }
