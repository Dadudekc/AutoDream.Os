import logging
from datetime import datetime
from typing import Any, Dict, List


class ReportGenerator:
    """Creates human readable reports from optimisation results."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__ + ".ReportGenerator")

    def generate(self, optimization_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive optimisation report."""
        report = {
            "report_id": f"performance_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "optimization_results": optimization_results,
            "performance_improvements": self._calculate_final_improvements(optimization_results),
            "recommendations": self._generate_final_recommendations(),
            "next_steps": self._generate_next_steps(),
        }
        self.logger.debug("Generated report: %s", report)
        return report

    # ------------------------------------------------------------------ helpers
    def _calculate_final_improvements(self, results: Dict[str, Any]) -> Dict[str, Any]:
        phases = results.get("phases", {})
        score = sum(len(v) for v in phases.values())
        return {"final_score": score}

    def _generate_final_recommendations(self) -> List[str]:
        return [
            "Maintain optimised performance monitoring systems",
            "Continue resource utilisation optimisation",
            "Plan next optimisation cycle",
        ]

    def _generate_next_steps(self) -> List[str]:
        return [
            "Monitor optimisation results",
            "Coordinate with other agents for system-wide optimisation",
        ]
