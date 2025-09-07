from typing import Any, Callable, Dict, List, Optional

from . import execution as execution_module
from . import postprocess as postprocess_module
from . import setup as setup_module
from .common import (
from __future__ import annotations
from core.managers.base_manager import BaseManager

"""Automated refactoring workflow package."""




    WorkflowExecution,
    WorkflowStatus,
    WorkflowStep,
    WorkflowType,
    logger,
)


class AutomatedRefactoringWorkflows(BaseManager):
    """Automated refactoring workflows implementation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config or {})
        self.workflows: Dict[str, WorkflowExecution] = {}
        self.workflow_templates: Dict[WorkflowType, List[Dict[str, Any]]] = {}
        self.validation_rules: Dict[str, Callable] = {}
        self.reliability_metrics: Dict[str, float] = {}

        setup_module.initialize_workflow_templates(self)
        setup_module.initialize_validation_rules(self)
        setup_module.setup_logging()

    # Setup
    create_workflow = setup_module.create_workflow

    # Execution
    execute_workflow = execution_module.execute_workflow
    _execute_workflow_step = execution_module.execute_workflow_step

    # Post-processing
    validate_workflow = postprocess_module.validate_workflow
    get_workflow_status = postprocess_module.get_workflow_status
    list_workflows = postprocess_module.list_workflows
    get_reliability_metrics = postprocess_module.get_reliability_metrics
    cleanup_completed_workflows = postprocess_module.cleanup_completed_workflows
    export_workflow_report = postprocess_module.export_workflow_report


__all__ = [
    "AutomatedRefactoringWorkflows",
    "WorkflowExecution",
    "WorkflowStatus",
    "WorkflowStep",
    "WorkflowType",
    "logger",
]
