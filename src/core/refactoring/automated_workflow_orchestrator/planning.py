"""Planning stage for the automated workflow orchestrator."""

from __future__ import annotations

import logging
from typing import Iterable

from .utils import WorkflowStep


def plan_steps(steps: Iterable[WorkflowStep], logger: logging.Logger) -> None:
    """Prepare workflow steps before execution.

    Each step is marked as planned and its start time is recorded when
    execution begins.
    """
    for step in steps:
        logger.info("Planning step %s", step.name)
        step.status = "planned"
