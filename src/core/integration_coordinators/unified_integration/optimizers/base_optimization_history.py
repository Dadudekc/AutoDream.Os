"""Base class for optimization history handling."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..models import IntegrationType


class BaseOptimizationHistory:
    """Provides shared optimization history functionality."""

    def __init__(self) -> None:
        self.optimization_history: List[Dict[str, Any]] = []

    def _record_optimization(
        self,
        integration_type: IntegrationType,
        improvements: List[Dict[str, Any]],
        execution_time: float,
        extra_fields: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record an optimization execution."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "integration_type": integration_type.value,
            "improvements_count": len(improvements),
            "execution_time": execution_time,
            "improvements": improvements,
        }
        if extra_fields:
            record.update(extra_fields)
        self.optimization_history.append(record)
        if len(self.optimization_history) > 100:
            self.optimization_history = self.optimization_history[-100:]

    def get_optimization_history(
        self,
        integration_type: Optional[IntegrationType] = None,
        hours: int = 24,
    ) -> List[Dict[str, Any]]:
        """Retrieve optimization history records."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        history = self.optimization_history
        if integration_type:
            history = [
                record
                for record in history
                if record["integration_type"] == integration_type.value
            ]
        return [
            record
            for record in history
            if datetime.fromisoformat(record["timestamp"]) >= cutoff_time
        ]
