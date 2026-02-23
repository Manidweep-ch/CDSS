from datetime import datetime
import logging

from app.Rules.kidney_rules import KidneyRuleEngine
from app.ml.kidney_predictor import KidneyPredictor
from app.ml.kidney_shap_explainer import KidneyShapExplainer

logger = logging.getLogger(__name__)


class KidneyHybridService:

    @staticmethod
    def evaluate(data: dict):

        rule_result = KidneyRuleEngine.evaluate(data)
        
        # Try ML prediction with error handling
        try:
            ml_result = KidneyPredictor.predict(data)
        except Exception as e:
            logger.error(f"Kidney ML prediction failed: {str(e)}")
            ml_result = {
                "ml_probability": None,
                "ml_threshold": 0.5,
                "ml_risk_flag": "ML Unavailable",
                "model_version": "Error",
                "error": str(e)
            }
        
        # Try SHAP explanation with error handling
        try:
            shap_result = KidneyShapExplainer.explain(data)
        except Exception as e:
            logger.error(f"Kidney SHAP explanation failed: {str(e)}")
            shap_result = {
                "top_feature_contributions": [],
                "error": str(e)
            }

        if rule_result.get("override_required"):
            final_decision = rule_result.get("risk_level")
            decision_source = "Rule Engine (Authoritative Override)"
            confidence = 1.0
            override_reason = rule_result.get("reason")
        else:
            # Use ML result if available, otherwise fall back to rule result
            if ml_result.get("ml_probability") is not None:
                final_decision = ml_result.get("ml_risk_flag")
                decision_source = "Hybrid (Rule + ML Assist)"
                confidence = ml_result.get("ml_probability")
            else:
                final_decision = rule_result.get("risk_level", "Unknown")
                decision_source = "Rule Engine Only (ML Failed)"
                confidence = 0.5
            override_reason = ""

        severity = rule_result.get("risk_level", final_decision)

        return {
            "panel": "Kidney",
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
