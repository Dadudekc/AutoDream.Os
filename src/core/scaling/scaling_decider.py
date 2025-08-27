from __future__ import annotations

import time
from typing import Tuple

from .types import ScalingConfig, ScalingDecision, ScalingMetrics


class ScalingDecider:
    """Simple rules based scaling decision engine."""

    def decide(self, metrics: ScalingMetrics, config: ScalingConfig) -> ScalingDecision:
        """Return a scaling decision based on current metrics."""
        action = "maintain"
        reason = "within target utilization"
        if (
            metrics.cpu_utilization > config.target_cpu_utilization
            or metrics.memory_utilization > config.target_memory_utilization
        ):
            action = "scale_up"
            reason = "resource utilization above target"
        elif (
            metrics.cpu_utilization < config.target_cpu_utilization * 0.5
            and metrics.memory_utilization < config.target_memory_utilization * 0.5
        ):
            action = "scale_down"
            reason = "resource utilization well below target"

        decision = ScalingDecision(
            decision_id=f"decision_{int(time.time() * 1000)}",
            action=action,
            reason=reason,
            current_metrics=metrics,
            confidence=0.8,
            timestamp=time.time(),
        )
        return decision
