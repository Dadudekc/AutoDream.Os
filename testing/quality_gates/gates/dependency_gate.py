"""
Dependency count quality gate implementation.
"""

from pathlib import Path
from typing import Any, Dict
from .base_gate import BaseGate
from ..models import GateStatus


class DependencyGate(BaseGate):
    """Quality gate for checking dependency count."""
    
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute dependency count quality gate."""
        dependency_count = file_metrics.get('dependency_count', 0)
        threshold = self.config.threshold
        
        passed = dependency_count <= threshold
        score = max(0, 100 - (dependency_count - threshold) * 5) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations = [
                "Reduce external dependencies",
                "Use dependency injection",
                "Consider creating internal abstractions",
                "Review if all imports are necessary"
            ]
        
        details = f"Dependency count: {dependency_count} (threshold: {threshold})"
        
        return self._create_result(status, score, details, recommendations)
