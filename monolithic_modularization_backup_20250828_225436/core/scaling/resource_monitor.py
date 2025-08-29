from __future__ import annotations

import time
from typing import List, Optional

from .types import ScalingMetrics


class ResourceMonitor:
    """Collects and stores resource metrics for scaling decisions."""

    def __init__(self) -> None:
        self._history: List[ScalingMetrics] = []

    def record(self, metrics: ScalingMetrics) -> None:
        """Record a new set of metrics."""
        self._history.append(metrics)

    def latest(self) -> Optional[ScalingMetrics]:
        """Return the most recently recorded metrics."""
        return self._history[-1] if self._history else None

    def collect(
        self, current_instances: int, cpu: float, memory: float
    ) -> ScalingMetrics:
        """Create and store a ScalingMetrics entry."""
        metrics = ScalingMetrics(
            current_instances=current_instances,
            target_instances=current_instances,
            cpu_utilization=cpu,
            memory_utilization=memory,
            response_time=0.0,
            throughput=0.0,
            error_rate=0.0,
            timestamp=time.time(),
        )
        self.record(metrics)
        return metrics

    @property
    def history(self) -> List[ScalingMetrics]:
        return list(self._history)
