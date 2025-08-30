"""
Test coverage quality gate implementation.
"""

from pathlib import Path
from typing import Any, Dict
from .base_gate import BaseGate
from ..models import GateStatus


class TestCoverageGate(BaseGate):
    """Quality gate for checking test coverage."""
    
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute test coverage quality gate."""
        coverage = file_metrics.get('test_coverage', 0)
        threshold = self.config.threshold
        
        passed = coverage >= threshold
        score = min(100, coverage) if passed else max(0, coverage)
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations = [
                "Add unit tests for uncovered functions",
                "Increase test coverage for critical paths",
                "Consider integration tests for complex logic",
                "Review test strategy and priorities"
            ]
        
        details = f"Test coverage: {coverage:.1f}% (threshold: {threshold}%)"
        
        return self._create_result(status, score, details, recommendations)
