"""
Function length quality gate implementation.
"""

from pathlib import Path
from typing import Any, Dict
from .base_gate import BaseGate
from ..models import GateStatus


class FunctionLengthGate(BaseGate):
    """Quality gate for checking function length."""
    
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute function length quality gate."""
        max_function_length = file_metrics.get('max_function_length', 0)
        threshold = self.config.threshold
        
        passed = max_function_length <= threshold
        score = max(0, 100 - (max_function_length - threshold) * 2) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations = [
                "Break down long functions into smaller ones",
                "Extract complex logic into helper methods",
                "Use early returns to reduce nesting",
                "Consider splitting functions by responsibility"
            ]
        
        details = f"Maximum function length: {max_function_length} lines (threshold: {threshold})"
        
        return self._create_result(status, score, details, recommendations)
