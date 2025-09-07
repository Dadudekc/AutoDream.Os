"""
Line count quality gate implementation.
"""

from pathlib import Path
from typing import Any, Dict
from .base_gate import BaseGate
from ..models import GateStatus


class LineCountGate(BaseGate):
    """Quality gate for checking file line count."""
    
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute line count quality gate."""
        line_count = file_metrics.get('original_lines', 0)
        threshold = self.config.threshold
        
        # Adjust threshold for test files
        if 'test' in str(file_path).lower():
            threshold = 500.0
        
        passed = line_count <= threshold
        score = max(0, 100 - (line_count - threshold) / 10) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations = [
                "Break down the file into smaller modules",
                "Extract classes into separate files",
                "Move utility functions to dedicated modules",
                "Consider using composition over inheritance"
            ]
        
        details = f"Line count: {line_count} (threshold: {threshold})"
        
        return self._create_result(status, score, details, recommendations)
