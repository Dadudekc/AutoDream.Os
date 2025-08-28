"""High level orchestration for smooth handoffs."""

from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import Any, Dict, Optional

from .base_manager import BaseManager
from .handoff.detection import HandoffDetector
from .handoff.logging import get_handoff_logger
from .handoff.coordinator import HandoffCoordinator
from .handoff.transition import execute_rollback
from .handoff.models import (
    HandoffContext,
    HandoffExecution,
    HandoffProcedure,
    HandoffStatus,
)
from .handoff.defaults import get_default_procedures


class SmoothHandoffSystem(BaseManager):
    """Manage handoff procedures and delegate execution to subsystems."""

    def __init__(self, project_root: str = ".") -> None:
        super().__init__("SmoothHandoffSystem")
        self.project_root = Path(project_root)
        self.logger = get_handoff_logger(__name__)
        self.detector = HandoffDetector()
        self.coordinator = HandoffCoordinator(self.detector, self.logger)

        self.handoff_procedures: Dict[str, HandoffProcedure] = {}
        self.active_handoffs: Dict[str, HandoffExecution] = {}
        self.handoff_history: Dict[str, HandoffExecution] = {}

        self._load_default_procedures()

    def _load_default_procedures(self) -> None:
        """Populate the procedure registry with built-in procedures."""
        for procedure in get_default_procedures():
            self.handoff_procedures[procedure.procedure_id] = procedure

    def initiate_handoff(self, context: HandoffContext, procedure_id: str) -> str:
        """Start executing a handoff procedure.

        Returns an execution identifier used for status lookups.
        """
        if procedure_id not in self.handoff_procedures:
            raise ValueError(f"Unknown procedure ID: {procedure_id}")

        execution_id = f"handoff_{int(time.time())}_{context.handoff_id}"
        execution = HandoffExecution(
            execution_id=execution_id,
            handoff_id=context.handoff_id,
            procedure_id=procedure_id,
            status=HandoffStatus.PENDING,
            current_step=0,
        )
        self.active_handoffs[execution_id] = execution
        asyncio.create_task(
            self._execute_handoff(execution, context, self.handoff_procedures[procedure_id])
        )
        return execution_id

    async def _execute_handoff(
        self,
        execution: HandoffExecution,
        context: HandoffContext,
        procedure: HandoffProcedure,
    ) -> None:
        """Run the steps for a procedure and track basic status."""
        execution.status = HandoffStatus.IN_PROGRESS
        success = await self.coordinator.coordinate(
            procedure.steps,
            context,
            execution,
            {},
        )
        if not success:
            await execute_rollback(execution, context, procedure, self.logger, HandoffStatus)
            execution.status = HandoffStatus.FAILED
        else:
            execution.status = HandoffStatus.COMPLETED
            execution.end_time = time.time()
        self.active_handoffs.pop(execution.execution_id, None)
        self.handoff_history[execution.execution_id] = execution

    def get_handoff_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Return tracking information for a handoff execution."""
        execution = self.active_handoffs.get(execution_id)
        if not execution:
            execution = self.handoff_history.get(execution_id)
        if not execution:
            return None
        return {
            "execution_id": execution.execution_id,
            "status": execution.status.value,
            "current_step": execution.current_step,
            "steps_completed": execution.steps_completed,
            "steps_failed": execution.steps_failed,
        }

    def add_handoff_procedure(self, procedure: HandoffProcedure) -> None:
        """Register a new handoff procedure."""
        self.handoff_procedures[procedure.procedure_id] = procedure

    def remove_handoff_procedure(self, procedure_id: str) -> None:
        """Remove a handoff procedure if not required."""
        self.handoff_procedures.pop(procedure_id, None)


# Global instance for system-wide access
smooth_handoff_system = SmoothHandoffSystem()


def get_smooth_handoff_system() -> SmoothHandoffSystem:
    """Return the global smooth handoff system instance."""
    return smooth_handoff_system
