"""Automated workflow orchestrator package."""

from __future__ import annotations

import logging
from typing import Iterable

from ...base_manager import BaseManager
from . import execution, monitoring, planning, settings
from .utils import WorkflowExecution, WorkflowStep, generate_execution_id

__all__ = [
    "AutomatedWorkflowOrchestrator",
    "WorkflowExecution",
    "WorkflowStep",
]


class AutomatedWorkflowOrchestrator(BaseManager):
    """Coordinate planning, execution and monitoring of workflow steps."""

    def __init__(
        self,
        workflow_name: str = settings.DEFAULT_WORKFLOW_NAME,
    ) -> None:
        super().__init__()
        self.workflow_name = workflow_name
        self.logger = logging.getLogger(__name__)

    def run(self, steps: Iterable[WorkflowStep]) -> WorkflowExecution:
        """Run a sequence of workflow steps."""
        steps = list(steps)
        planning.plan_steps(steps, self.logger)
        execution_record = WorkflowExecution(
            execution_id=generate_execution_id(),
            workflow_name=self.workflow_name,
            steps=steps,
        )
        for step in execution_record.steps:
            execution.execute_step(step, self.logger)
        return monitoring.summarize_execution(execution_record, self.logger)
