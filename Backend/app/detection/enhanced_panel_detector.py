from typing import Dict, List, Any


class EnhancedPanelDetector:
    """
    Enhanced panel detection with detailed test mapping.
    Maps extracted biomarkers to available analyzers.
    """

    # Map biomarkers to required model inputs
    PANEL_REQUIREMENTS = {
        "Diabetes": {
            "required_any": ["fasting_glucose_level", "HbA1c_level"],
            "model_inputs": ["fasting_glucose_level", "HbA1c_level"],
            "description": "Diabetes Risk Analysis"
        },
        "Cardiovascular": {
            "required_all": ["totChol", "hdl"],
            "required_any": ["sysBP", "diaBP"],
            "model_inputs": ["totChol", "hdl", "triglycerides", "sysBP", "diaBP", "age", "sex"],
            "description": "Cardiovascular Risk Analysis"
        },
        "Kidney": {
            "required_any": ["serum_creatinine"],
            "model_inputs": ["serum_creatinine", "blood_urea", "age"],
            "description": "Kidney Function Analysis"
        }
    }

    @staticmethod
    def detect_available_panels(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect which panels can be analyzed based on extracted data.
        Returns detailed information about each panel's readiness.
        """
        data_keys = set(extracted_data.keys())
        
        available_panels = []
        panel_details = {}
        unsupported_tests = []
        
        # Check each panel
        for panel_name, requirements in EnhancedPanelDetector.PANEL_REQUIREMENTS.items():
            required_all = requirements.get("required_all", [])
            required_any = requirements.get("required_any", [])
            model_inputs = requirements.get("model_inputs", [])
            
            # Check if panel requirements are met
            has_all = all(key in data_keys for key in required_all) if required_all else True
            has_any = any(key in data_keys for key in required_any) if required_any else True
            
            if has_all and has_any:
                # Panel is available
                available_panels.append(panel_name)
                
                # Check which inputs are present
                present_inputs = [inp for inp in model_inputs if inp in data_keys]
                missing_inputs = [inp for inp in model_inputs if inp not in data_keys]
                
                panel_details[panel_name] = {
                    "status": "available",
                    "description": requirements["description"],
                    "present_inputs": present_inputs,
                    "missing_inputs": missing_inputs,
                    "can_analyze": len(present_inputs) >= len(required_all or required_any)
                }
        
        # Identify tests that don't belong to any supported panel
        all_supported_markers = set()
        for requirements in EnhancedPanelDetector.PANEL_REQUIREMENTS.values():
            all_supported_markers.update(requirements.get("model_inputs", []))
        
        for key in data_keys:
            if key not in all_supported_markers:
                unsupported_tests.append(key)
        
        return {
            "available_panels": available_panels,
            "panel_details": panel_details,
            "unsupported_tests": unsupported_tests,
            "total_tests_found": len(data_keys),
            "extracted_data": extracted_data
        }

    @staticmethod
    def get_panel_status_message(panel_name: str, panel_details: Dict) -> str:
        """
        Generate user-friendly status message for a panel.
        """
        if panel_name not in panel_details:
            return f"{panel_name}: Model not yet built"
        
        detail = panel_details[panel_name]
        
        if detail["status"] == "available":
            if detail["missing_inputs"]:
                return f"{panel_name}: Available (some optional inputs missing)"
            return f"{panel_name}: Ready for analysis"
        
        return f"{panel_name}: Insufficient data"
