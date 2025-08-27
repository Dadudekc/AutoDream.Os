from __future__ import annotations

from .types import ScalingConfig, ScalingStatus


class ScalingExecutor:
    """Executes scaling actions and returns new state."""

    def execute(
        self, action: str, current_instances: int, config: ScalingConfig
    ) -> tuple[int, ScalingStatus]:
        if action == "scale_up" and current_instances < config.max_instances:
            return current_instances + 1, ScalingStatus.SCALING_UP
        if action == "scale_down" and current_instances > config.min_instances:
            return current_instances - 1, ScalingStatus.SCALING_DOWN
        if action == "optimize":
            return current_instances, ScalingStatus.OPTIMIZING
        return current_instances, ScalingStatus.IDLE
