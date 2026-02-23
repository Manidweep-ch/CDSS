def analyze_cardio(totChol=None,
                   hdl=None,
                   triglycerides=None,
                   sysBP=None,
                   diaBP=None,
                   age=None,
                   sex=None):

    findings = []
    severity = 0
    guideline_refs = []

    # ===============================
    # Total Cholesterol (proxy if LDL missing)
    # ===============================

    if totChol is not None:
        if totChol >= 240:
            findings.append("High Total Cholesterol (≥240 mg/dL)")
            severity += 2
            guideline_refs.append("ACC/AHA Cholesterol Guideline")
        elif totChol >= 200:
            findings.append("Borderline High Cholesterol")
            severity += 1

    # ===============================
    # HDL
    # ===============================

    if hdl is not None and sex is not None:
        # Handle both string and numeric sex values
        sex_str = str(sex).lower() if isinstance(sex, (int, float)) else sex.lower()
        
        # Convert numeric: 1=male, 0=female
        if sex_str in ["1", "1.0"]:
            sex_str = "male"
        elif sex_str in ["0", "0.0"]:
            sex_str = "female"
            
        if (sex_str == "male" and hdl < 40) or \
           (sex_str == "female" and hdl < 50):
            findings.append("Low HDL")
            severity += 1
            guideline_refs.append("ACC/AHA Lipid Guideline")

    # ===============================
    # Triglycerides
    # ===============================

    if triglycerides is not None:
        if triglycerides >= 200:
            findings.append("High Triglycerides")
            severity += 1

    # ===============================
    # Blood Pressure
    # ===============================

    if sysBP is not None and diaBP is not None:
        if sysBP >= 160 or diaBP >= 100:
            findings.append("Stage 2 Hypertension")
            severity += 3
            guideline_refs.append("AHA 2017 Hypertension Guideline")
        elif sysBP >= 140 or diaBP >= 90:
            findings.append("Stage 1 Hypertension")
            severity += 2
            guideline_refs.append("AHA 2017 Hypertension Guideline")

    # ===============================
    # Age Risk Modifier
    # ===============================

    if age is not None:
        if age >= 65:
            severity += 2
        elif age >= 55:
            severity += 1

    # ===============================
    # Risk Classification
    # ===============================

    if severity >= 6:
        risk = "High"
    elif severity >= 3:
        risk = "Moderate"
    else:
        risk = "Low"

    return {
        "risk_level": risk,
        "severity_score": severity,
        "findings": findings,
        "guideline_references": list(set(guideline_refs))
    }
