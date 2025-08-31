"""
Class complexity quality gate implementation.
"""

from pathlib import Path
from typing import Any, Dict
from .base_gate import BaseGate
from ..models import GateStatus


class ClassComplexityGate(BaseGate):
    """Quality gate for checking class complexity."""
    
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute class complexity quality gate."""
        class_complexity = file_metrics.get('class_complexity', 0)
        threshold = self.config.threshold
        
        passed = class_complexity <= threshold
        score = max(0, 100 - (class_complexity - threshold) * 5) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations = [
                "Break down complex classes into smaller ones",
                "Use composition over inheritance",
                "Extract complex methods into separate classes",
                "Consider using design patterns to simplify structure"
            ]
        
        details = f"Class complexity: {class_complexity} (threshold: {threshold})"
        
        return self._create_result(status, score, details, recommendations)
