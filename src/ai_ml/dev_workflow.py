"""Orchestrator coordinating AI development workflow modules."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

from .dev_workflow_config import load_workflow_config, WorkflowConfig
from .dev_workflow_ai_processor import AIProcessor, ProjectAnalysis
from .dev_workflow_manager import (
    DevWorkflowManager,
    WorkflowResult,
    WorkflowStep,
)
from .dev_workflow_coordinator import WorkflowCoordinator


class AIDevWorkflow:
    """High-level API for executing development workflows."""

    def __init__(self, project_path: str = "."):
        self.config: WorkflowConfig = load_workflow_config(project_path)
        self.processor = AIProcessor(self.config)
        self.coordinator = WorkflowCoordinator()
        self.manager = DevWorkflowManager(
            self.config.project_path, self.processor, self.coordinator
        )

    # Public API -------------------------------------------------------
    def get_available_workflows(self) -> list[str]:
        return self.coordinator.get_available_workflows()

    def execute_workflow(self, workflow_name: str, **kwargs) -> Dict[str, WorkflowResult]:
        return self.manager.execute_workflow(workflow_name, **kwargs)

    def analyze_project(self) -> ProjectAnalysis:
        return self.processor.analyze_project(self.config.project_path)

    def is_configured(self) -> bool:
        return bool(self.config.openai_key or self.config.anthropic_key)


def get_ai_dev_workflow(project_path: str = ".") -> AIDevWorkflow:
    """Get a singleton instance of the AI Dev Workflow orchestrator."""
    if not hasattr(get_ai_dev_workflow, "_instance"):
        get_ai_dev_workflow._instance = AIDevWorkflow(project_path)
    return get_ai_dev_workflow._instance


__all__ = [
    "AIDevWorkflow",
    "WorkflowStep",
    "WorkflowResult",
    "ProjectAnalysis",
    "get_ai_dev_workflow",
]
