"""Workflow setup utilities."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from .common import (
    DEFAULT_WORKFLOW_TEMPLATES,
    WorkflowExecution,
    WorkflowStep,
    WorkflowType,
    logger,
)
from .execution import get_step_action
from .postprocess import (
    validate_complexity_reduction,
    validate_file_size_reduction,
    validate_function_count_optimization,
    validate_functionality_preservation,
    validate_test_coverage_maintenance,
)


def setup_logging() -> None:
    """Placeholder for logging configuration (handled in common)."""
    # Logging is configured in common; function provided for interface parity.
    _ = logger


def initialize_workflow_templates(self) -> None:
    """Initialize predefined workflow templates."""
    self.workflow_templates = DEFAULT_WORKFLOW_TEMPLATES.copy()


def initialize_validation_rules(self) -> None:
    """Initialize validation rules for workflow reliability."""
    self.validation_rules = {
        "file_size_reduction": validate_file_size_reduction,
        "function_count_optimization": validate_function_count_optimization,
        "complexity_reduction": validate_complexity_reduction,
        "test_coverage_maintenance": validate_test_coverage_maintenance,
        "functionality_preservation": validate_functionality_preservation,
    }


def create_workflow(
    self,
    workflow_type: WorkflowType,
    target_files: List[str],
    custom_steps: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Create a new automated refactoring workflow."""
    workflow_id = (
        f"workflow_{workflow_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    template_steps = self.workflow_templates.get(workflow_type, [])
    steps_data = custom_steps if custom_steps else template_steps

    steps = []
    for step_data in steps_data:
        step = WorkflowStep(
            step_id=step_data["step_id"],
            name=step_data["name"],
            description=step_data["description"],
            action=get_step_action(step_data["step_id"]),
            estimated_time=step_data["estimated_time"],
        )
        steps.append(step)

    workflow = WorkflowExecution(
        workflow_id=workflow_id,
        workflow_type=workflow_type,
        target_files=target_files,
        steps=steps,
    )
    self.workflows[workflow_id] = workflow
    logger.info(f"Created workflow {workflow_id} for {workflow_type.value}")
    return workflow_id
