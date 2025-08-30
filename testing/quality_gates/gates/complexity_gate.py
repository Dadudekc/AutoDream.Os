"""
Cyclomatic complexity quality gate implementation.
"""

from pathlib import Path
from typing import Any, Dict
from .base_gate import BaseGate
from ..models import GateStatus


class ComplexityGate(BaseGate):
    """Quality gate for checking cyclomatic complexity."""
    
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute complexity quality gate."""
        complexity = file_metrics.get('cyclomatic_complexity', 0)
        threshold = self.config.threshold
        
        passed = complexity <= threshold
        score = max(0, 100 - (complexity - threshold) * 5) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations = [
                "Break down complex functions into smaller ones",
                "Extract conditional logic into separate methods",
                "Use early returns to reduce nesting",
                "Consider using strategy pattern for complex logic"
            ]
        
        details = f"Cyclomatic complexity: {complexity} (threshold: {threshold})"
        
        return self._create_result(status, score, details, recommendations)
