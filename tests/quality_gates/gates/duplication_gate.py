"""
Code duplication quality gate implementation.
"""

from pathlib import Path
from typing import Any, Dict
from .base_gate import BaseGate
from ..models import GateStatus


class DuplicationGate(BaseGate):
    """Quality gate for checking code duplication."""
    
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute code duplication quality gate."""
        duplication_percent = file_metrics.get('code_duplication_percent', 0)
        threshold = self.config.threshold
        
        passed = duplication_percent <= threshold
        score = max(0, 100 - duplication_percent * 5) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations = [
                "Extract common functionality into utility functions",
                "Use inheritance or composition to reduce duplication",
                "Create shared constants and configuration",
                "Consider using design patterns to eliminate duplication"
            ]
        
        details = f"Code duplication: {duplication_percent:.1f}% (threshold: {threshold}%)"
        
        return self._create_result(status, score, details, recommendations)
