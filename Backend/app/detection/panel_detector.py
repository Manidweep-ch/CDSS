from typing import Dict, List, Any


# ---- PANEL REQUIREMENT MAP ---- #

PANEL_REQUIREMENTS = {
    "diabetes": {
        "any_of": [
            "fasting_glucose",
            "hba1c",
            "random_glucose"
        ]
    },
    "cardiovascular": {
        "all_of": [
            "total_cholesterol",
            "ldl",
            "hdl"
        ],
        "any_of": [
            "systolic_bp",
            "diastolic_bp"
        ]
    },
    "kidney": {
        "any_of": [
            "serum_creatinine"
        ]
    }
}


def _has_all(data_keys: set, required_keys: List[str]) -> bool:
    return all(key in data_keys for key in required_keys)


def _has_any(data_keys: set, required_keys: List[str]) -> bool:
    return any(key in data_keys for key in required_keys)


def detect_panels(extracted_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Detect supported panels based purely on presence of required biomarkers.
    Deterministic logic only.
    No ML.
    """

    detected_panels = []
    unsupported_tests = []

    data_keys = set(extracted_data.keys())

    for panel_name, rules in PANEL_REQUIREMENTS.items():

        all_of = rules.get("all_of", [])
        any_of = rules.get("any_of", [])

        has_all_required = True
        has_any_required = True

        if all_of:
            has_all_required = _has_all(data_keys, all_of)

        if any_of:
            has_any_required = _has_any(data_keys, any_of)

        if has_all_required and has_any_required:
            detected_panels.append(panel_name)

    # Identify unsupported biomarkers
    supported_markers = set()
    for rules in PANEL_REQUIREMENTS.values():
        supported_markers.update(rules.get("all_of", []))
        supported_markers.update(rules.get("any_of", []))

    for key in data_keys:
        if key not in supported_markers:
            unsupported_tests.append(key)

    return {
        "detected_panels": detected_panels,
        "unsupported_tests": unsupported_tests
    }
