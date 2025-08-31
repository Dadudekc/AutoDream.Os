"""
Documentation coverage quality gate implementation.
"""

from pathlib import Path
from typing import Any, Dict
from .base_gate import BaseGate
from ..models import GateStatus


class DocumentationGate(BaseGate):
    """Quality gate for checking documentation coverage."""
    
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute documentation coverage quality gate."""
        doc_coverage = file_metrics.get('documentation_coverage', 100)
        threshold = self.config.threshold
        
        passed = doc_coverage >= threshold
        score = doc_coverage
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations = [
                "Add docstrings to all functions and classes",
                "Include parameter and return type documentation",
                "Document complex algorithms and business logic",
                "Maintain up-to-date README and API documentation"
            ]
        
        details = f"Documentation coverage: {doc_coverage:.1f}% (threshold: {threshold}%)"
        
        return self._create_result(status, score, details, recommendations)
