from typing import Dict, List, Any

from app.Services.diabetes_hybrid_service import DiabetesHybridService
from app.Services.cardio_hybrid_service import CardioHybridService
from app.Services.kidney_hybrid_service import KidneyHybridService


class CDSSMasterRouter:

    PANEL_MAP = {
        "Diabetes": DiabetesHybridService,
        "Cardiovascular": CardioHybridService,
        "Kidney": KidneyHybridService
    }

    @staticmethod
    def route_single(panel_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a single panel safely.
        Returns { panel_name: result }
        """

        if panel_name not in CDSSMasterRouter.PANEL_MAP:
            raise ValueError(f"Unsupported panel: {panel_name}")

        service = CDSSMasterRouter.PANEL_MAP[panel_name]

        try:
            result = service.evaluate(data)
            return {panel_name: result}

        except Exception as e:
            # Error isolation — do not crash entire system
            return {
                panel_name: {
                    "error": str(e),
                    "status": "execution_failed"
                }
            }

    @staticmethod
    def route_multiple(panels: List[str], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes multiple panels safely.
        Each panel isolated.
        """

        results = {}

        for panel_name in panels:

            if panel_name not in CDSSMasterRouter.PANEL_MAP:
                results[panel_name] = {
                    "error": "Unsupported panel",
                    "status": "invalid_panel"
                }
                continue

            service = CDSSMasterRouter.PANEL_MAP[panel_name]

            try:
                results[panel_name] = service.evaluate(data)

            except Exception as e:
                results[panel_name] = {
                    "error": str(e),
                    "status": "execution_failed"
                }

        return results
