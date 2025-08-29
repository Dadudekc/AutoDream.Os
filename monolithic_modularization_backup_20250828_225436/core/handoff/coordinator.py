"""Coordinator for handoff subsystems."""

from typing import Any, Dict, List, Callable
import logging

from .detection import HandoffDetector
from .transition import execute_step


class HandoffCoordinator:
    """Sequence detection and transition operations."""

    def __init__(self, detector: HandoffDetector, logger: logging.Logger) -> None:
        self.detector = detector
        self.logger = logger

    async def coordinate(
        self,
        steps: List[Dict[str, Any]],
        context: Any,
        execution: Any,
        validation_engines: Dict[str, Callable],
    ) -> bool:
        """Run detection and sequentially execute transition steps.

        Returns:
            ``True`` when all steps succeed.
        """
        if not self.detector.should_handoff(context):
            self.logger.info(
                "No handoff required for %s", getattr(context, "handoff_id", "unknown")
            )
            return False

        for step in steps:
            execution.current_step = step.get("step_id", 0)
            success = await execute_step(step, context, execution, self.logger, validation_engines)
            if success:
                execution.steps_completed.append(step.get("step_id", 0))
                self.logger.info(
                    "✅ Step %s completed: %s", step.get("step_id"), step.get("name")
                )
            else:
                execution.steps_failed.append(step.get("step_id", 0))
                self.logger.error(
                    "❌ Step %s failed: %s", step.get("step_id"), step.get("name")
                )
                return False

        return True
