"""
Import organization quality gate implementation.
"""

from pathlib import Path
from typing import Any, Dict
from .base_gate import BaseGate
from ..models import GateStatus


class ImportOrganizationGate(BaseGate):
    """Quality gate for checking import organization."""
    
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute import organization quality gate."""
        import_score = file_metrics.get('import_organization_score', 100)
        threshold = self.config.threshold
        
        passed = import_score >= threshold
        score = import_score
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations = [
                "Group imports: standard library, third-party, local",
                "Sort imports alphabetically within groups",
                "Remove unused imports",
                "Use absolute imports for clarity"
            ]
        
        details = f"Import organization score: {import_score:.1f}% (threshold: {threshold}%)"
        
        return self._create_result(status, score, details, recommendations)
