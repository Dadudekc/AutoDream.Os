#!/usr/bin/env python3
"""
Sprint Workflow Service - Agent Cellphone V2
===========================================

Manages simple sprint workflow stages for planning and task estimation.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from src.utils.stability_improvements import stability_manager, safe_import


class WorkflowStage(Enum):
    """Workflow stages for a sprint."""

    NOT_STARTED = "not_started"
    SPRINT_PLANNING = "sprint_planning"
    TASK_ESTIMATION = "task_estimation"
    EXECUTION = "execution"
    RETROSPECTIVE = "retrospective"


@dataclass
class SprintWorkflow:
    """Workflow state container for a sprint."""

    sprint_id: str
    stage: WorkflowStage = WorkflowStage.NOT_STARTED
    planned_tasks: List[str] = field(default_factory=list)


class SprintWorkflowService:
    """Service for managing sprint workflows."""

    def __init__(self, sprint_manager, task_manager):
        """Initialize workflow service with managers."""
        self.sprint_manager = sprint_manager
        self.task_manager = task_manager
        self.logger = self._setup_logging()
        self.workflows: Dict[str, SprintWorkflow] = {}
        self.status = "initialized"

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("SprintWorkflowService")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def start_sprint_planning(self, sprint_id: str) -> SprintWorkflow:
        """Begin planning stage for a sprint."""
        workflow = self.workflows.get(sprint_id)
        if not workflow:
            workflow = SprintWorkflow(sprint_id=sprint_id)
            self.workflows[sprint_id] = workflow

        workflow.stage = WorkflowStage.SPRINT_PLANNING
        self.logger.info(f"Started planning for sprint {sprint_id}")
        return workflow

    def plan_sprint_tasks(self, sprint_id: str, task_ids: List[str]) -> bool:
        """Plan tasks for a sprint and move to estimation."""
        if sprint_id not in self.workflows:
            self.logger.error(f"No workflow for sprint {sprint_id}")
            return False

        workflow = self.workflows[sprint_id]
        success = True

        for task_id in task_ids:
            if not self.sprint_manager.add_task_to_sprint(sprint_id, task_id):
                success = False

        if success:
            workflow.planned_tasks.extend(task_ids)
            workflow.stage = WorkflowStage.TASK_ESTIMATION
            self.logger.info(f"Planned tasks for sprint {sprint_id}")

        return success

    def get_workflow(self, sprint_id: str) -> Optional[SprintWorkflow]:
        """Retrieve workflow for a sprint."""
        return self.workflows.get(sprint_id)
