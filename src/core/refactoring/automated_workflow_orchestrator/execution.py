"""Execution stage for the automated workflow orchestrator."""

from __future__ import annotations

import logging
from datetime import datetime

from .utils import WorkflowStep


def execute_step(step: WorkflowStep, logger: logging.Logger) -> None:
    """Execute a single workflow step.

    The associated callable is invoked and the result is stored on the step.
    Any raised exception is caught and stored as an error message.
    """
    logger.info("Executing step %s", step.name)
    step.status = "running"
    step.started_at = datetime.utcnow()
    try:
        step.result = step.action()
        step.status = "completed"
    except Exception as exc:  # noqa: BLE001 - broad for workflow safety
        step.error = str(exc)
        step.status = "failed"
    finally:
        step.completed_at = datetime.utcnow()
