from typing import Dict


class KidneyRuleEngine:

    @staticmethod
    def evaluate(data: Dict) -> Dict:

        egfr = data.get("egfr")
        acr = data.get("albumin_creatinine_ratio")

        result = {
            "ckd_stage": None,
            "risk_level": "Low",
            "override_required": False,
            "reason": None
        }

        if egfr is None:
            return result

        if egfr >= 90:
            result["ckd_stage"] = "Stage 1"
        elif 60 <= egfr < 90:
            result["ckd_stage"] = "Stage 2"
        elif 30 <= egfr < 60:
            result["ckd_stage"] = "Stage 3"
            result["risk_level"] = "Moderate"
        elif 15 <= egfr < 30:
            result["ckd_stage"] = "Stage 4"
            result["risk_level"] = "High"
            result["override_required"] = True
            result["reason"] = "Severe CKD (Stage 4)"
        else:
            result["ckd_stage"] = "Stage 5"
            result["risk_level"] = "Critical"
            result["override_required"] = True
            result["reason"] = "Kidney Failure"

        if acr is not None and acr > 300:
            result["risk_level"] = "High"
            result["override_required"] = True
            result["reason"] = "Severe albuminuria"

        return result
