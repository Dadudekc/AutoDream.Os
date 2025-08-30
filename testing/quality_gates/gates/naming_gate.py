"""
Naming conventions quality gate implementation.
"""

from pathlib import Path
from typing import Any, Dict
from .base_gate import BaseGate
from ..models import GateStatus


class NamingGate(BaseGate):
    """Quality gate for checking naming conventions."""
    
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute naming conventions quality gate."""
        naming_score = file_metrics.get('naming_conventions_score', 100)
        threshold = self.config.threshold
        
        passed = naming_score >= threshold
        score = naming_score
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations = [
                "Follow PEP 8 naming conventions",
                "Use descriptive variable and function names",
                "Avoid abbreviations and acronyms",
                "Maintain consistent naming patterns"
            ]
        
        details = f"Naming conventions score: {naming_score:.1f}% (threshold: {threshold}%)"
        
        return self._create_result(status, score, details, recommendations)
