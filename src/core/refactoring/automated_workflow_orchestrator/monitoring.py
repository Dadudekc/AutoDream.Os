"""Monitoring stage for the automated workflow orchestrator."""

from __future__ import annotations

import logging
from datetime import datetime
from statistics import mean
from typing import Iterable

from .utils import WorkflowExecution, WorkflowStep


def summarize_execution(
    execution: WorkflowExecution, logger: logging.Logger
) -> WorkflowExecution:
    """Finalize and log execution results."""
    execution.completed_at = datetime.utcnow()
    statuses = [step.status for step in execution.steps]
    success = [status == "completed" for status in statuses]
    execution.success_rate = mean(success) * 100 if success else 0.0
    logger.info(
        "Workflow %s finished with %.1f%% success",
        execution.workflow_name,
        execution.success_rate,
    )
    return execution


def iter_failed_steps(steps: Iterable[WorkflowStep]) -> Iterable[WorkflowStep]:
    """Yield steps that failed during execution."""
    return (step for step in steps if step.status == "failed")
