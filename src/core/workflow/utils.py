#!/usr/bin/env python3
"""
Workflow Utilities
==================

Shared helpers for workflow modules.
Follows V2 standards: single responsibility.

Author: Agent-3 (Workflow Unification)
License: MIT
"""

from typing import List
import logging

from .types.workflow_models import WorkflowStep


def create_workflow_step(
    step_id: str,
    name: str,
    step_type: str,
    description: str,
    dependencies: List[str],
    estimated_duration: float,
) -> WorkflowStep:
    """Create a workflow step."""
    return WorkflowStep(
        step_id=step_id,
        name=name,
        step_type=step_type,
        description=description,
        dependencies=dependencies,
        estimated_duration=estimated_duration,
    )


def get_workflow_logger(name: str) -> logging.Logger:
    """Create or retrieve a configured workflow logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
