from datetime import datetime
from typing import Optional, Dict, Any

# ======================================================
# Rule Metadata
# ======================================================

RULE_VERSION = "1.1.0"
GUIDELINE_SOURCE = "American Diabetes Association (ADA)"

# ======================================================
# Threshold Constants (mg/dL and %)
# ======================================================

FBS_DIABETES = 126
FBS_PREDIABETES_LOW = 100

PPBS_DIABETES = 200
PPBS_PREDIABETES_LOW = 140

HBA1C_DIABETES = 6.5
HBA1C_PREDIABETES_LOW = 5.7

SEVERE_HYPERGLYCEMIA = 300  # emergency safety flag

# ======================================================
# Severity Labels
# ======================================================

SEVERITY_NORMAL = "Normal"
SEVERITY_PREDIABETES = "Prediabetes"
SEVERITY_DIABETES = "Diabetes"

SEVERITY_RANK = {
    SEVERITY_NORMAL: 0,
    SEVERITY_PREDIABETES: 1,
    SEVERITY_DIABETES: 2
}

# ======================================================
# Validation Helpers
# ======================================================

def validate_numeric(value: Optional[float], name: str):
    if value is None:
        return
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    if value < 0:
        raise ValueError(f"{name} cannot be negative")

# ======================================================
# Marker-Level Classification
# ======================================================

def classify_hba1c(value: Optional[float]):
    validate_numeric(value, "HbA1c")

    if value is None:
        return None
    if value >= HBA1C_DIABETES:
        return SEVERITY_DIABETES
    elif value >= HBA1C_PREDIABETES_LOW:
        return SEVERITY_PREDIABETES
    else:
        return SEVERITY_NORMAL


def classify_fbs(value: Optional[float]):
    validate_numeric(value, "FBS")

    if value is None:
        return None
    if value >= FBS_DIABETES:
        return SEVERITY_DIABETES
    elif value >= FBS_PREDIABETES_LOW:
        return SEVERITY_PREDIABETES
    else:
        return SEVERITY_NORMAL


def classify_ppbs(value: Optional[float]):
    validate_numeric(value, "PPBS")

    if value is None:
        return None
    if value >= PPBS_DIABETES:
        return SEVERITY_DIABETES
    elif value >= PPBS_PREDIABETES_LOW:
        return SEVERITY_PREDIABETES
    else:
        return SEVERITY_NORMAL

# ======================================================
# Aggregation + Structured Output
# ======================================================

def analyze_diabetes(
    hba1c: Optional[float] = None,
    fbs: Optional[float] = None,
    ppbs: Optional[float] = None
) -> Dict[str, Any]:

    marker_results = {}

    hba1c_class = classify_hba1c(hba1c)
    fbs_class = classify_fbs(fbs)
    ppbs_class = classify_ppbs(ppbs)

    if hba1c_class:
        marker_results["HbA1c"] = {
            "value": hba1c,
            "classification": hba1c_class
        }

    if fbs_class:
        marker_results["FBS"] = {
            "value": fbs,
            "classification": fbs_class
        }

    if ppbs_class:
        marker_results["PPBS"] = {
            "value": ppbs,
            "classification": ppbs_class
        }

    final_risk = SEVERITY_NORMAL

    for marker in marker_results.values():
        classification = marker["classification"]
        if SEVERITY_RANK[classification] > SEVERITY_RANK[final_risk]:
            final_risk = classification

    abnormal_flag = False
    if (fbs is not None and fbs >= SEVERE_HYPERGLYCEMIA) or \
       (ppbs is not None and ppbs >= SEVERE_HYPERGLYCEMIA):
        abnormal_flag = True

    return {
        "panel": "Diabetes",
        "risk_level": final_risk,
        "confidence_type": "Rule-Based",
        "abnormal_flag": abnormal_flag,
        "markers": marker_results,
        "guideline_source": GUIDELINE_SOURCE,
        "rule_version": RULE_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "disclaimer": "Rule-based clinical support using ADA thresholds. This is not a medical diagnosis."
    }
