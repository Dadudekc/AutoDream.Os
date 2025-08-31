"""
Base class for all quality gates.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict
from ..models import QualityGateConfig, QualityGateResult, GateStatus


class BaseGate(ABC):
    """Base class for all quality gates."""
    
    def __init__(self, config: QualityGateConfig):
        self.config = config
    
    @abstractmethod
    def execute(self, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute the quality gate check."""
        pass
    
    def _create_result(self, status: GateStatus, score: float, details: str, 
                      recommendations: list[str]) -> QualityGateResult:
        """Create a quality gate result."""
        from datetime import datetime
        
        return QualityGateResult(
            gate_name=self.config.gate_name,
            status=status,
            score=score,
            threshold=self.config.threshold,
            weight=self.config.weight,
            severity=self.config.severity,
            details=details,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
