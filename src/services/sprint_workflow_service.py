#!/usr/bin/env python3
"""
Sprint Workflow Service - Agent Cellphone V2
===========================================

Implements 10 tasks per sprint workflow automation.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class WorkflowStage(Enum):
    """Sprint workflow stages."""

    SPRINT_PLANNING = "sprint_planning"
    TASK_ESTIMATION = "task_estimation"
    SPRINT_EXECUTION = "sprint_execution"
    DAILY_STANDUP = "daily_standup"
    SPRINT_REVIEW = "sprint_review"
    SPRINT_RETROSPECTIVE = "sprint_retrospective"


@dataclass
class SprintWorkflow:
    """Sprint workflow configuration."""

    stage: WorkflowStage
    start_date: datetime
    end_date: datetime
    tasks_planned: int
    tasks_completed: int
    tasks_in_progress: int
    blockers: List[str]
    notes: str


class SprintWorkflowService:
    """
    Sprint Workflow Service - Single responsibility: Sprint workflow automation.

    This service manages:
    - Sprint planning workflow
    - Daily standup automation
    - Progress tracking and metrics
    - Workflow stage transitions
    """

    def __init__(self, sprint_manager, task_manager):
        """Initialize Sprint Workflow Service."""
        self.sprint_manager = sprint_manager
        self.task_manager = task_manager
        self.logger = self._setup_logging()
        self.current_workflow: Optional[SprintWorkflow] = None
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
        """Start sprint planning workflow."""
        try:
            sprint = self.sprint_manager.sprints.get(sprint_id)
            if not sprint:
                raise ValueError(f"Sprint {sprint_id} not found")

            workflow = SprintWorkflow(
                stage=WorkflowStage.SPRINT_PLANNING,
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=1),
                tasks_planned=0,
                tasks_completed=0,
                tasks_in_progress=0,
                blockers=[],
                notes="Sprint planning initiated",
            )

            self.current_workflow = workflow
            self.logger.info(f"Started sprint planning for {sprint.name}")
            return workflow
        except Exception as e:
            self.logger.error(f"Failed to start sprint planning: {e}")
            raise

    def plan_sprint_tasks(self, sprint_id: str, task_ids: List[str]) -> bool:
        """Plan tasks for sprint (enforce 10-task limit)."""
        try:
            if len(task_ids) > 10:
                self.logger.warning(
                    f"Cannot plan more than 10 tasks, got {len(task_ids)}"
                )
                return False

            sprint = self.sprint_manager.sprints.get(sprint_id)
            if not sprint:
                return False

            # Clear existing tasks and add new ones
            sprint.tasks = task_ids[:10]
            self.sprint_manager._save_sprint(sprint)

            if self.current_workflow:
                self.current_workflow.tasks_planned = len(sprint.tasks)
                self.current_workflow.stage = WorkflowStage.TASK_ESTIMATION

            self.logger.info(
                f"Planned {len(sprint.tasks)} tasks for sprint {sprint.name}"
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to plan sprint tasks: {e}")
            return False

    def start_sprint_execution(self, sprint_id: str) -> bool:
        """Start sprint execution workflow."""
        try:
            sprint = self.sprint_manager.sprints.get(sprint_id)
            if not sprint:
                return False

            if len(sprint.tasks) == 0:
                self.logger.warning("Cannot start sprint with no planned tasks")
                return False

            # Start the sprint
            success = self.sprint_manager.start_sprint(sprint_id)
            if success and self.current_workflow:
                self.current_workflow.stage = WorkflowStage.SPRINT_EXECUTION
                self.logger.info(f"Started sprint execution for {sprint.name}")

            return success
        except Exception as e:
            self.logger.error(f"Failed to start sprint execution: {e}")
            return False

    def update_daily_progress(self, sprint_id: str) -> Dict[str, Any]:
        """Update daily progress and generate standup report."""
        try:
            sprint = self.sprint_manager.sprints.get(sprint_id)
            if not sprint or sprint.status.value != "active":
                return {}

            # Get current task statuses
            tasks = self.sprint_manager.get_sprint_tasks(sprint_id)
            completed = sum(1 for task in tasks if task.get("status") == "completed")
            in_progress = sum(
                1 for task in tasks if task.get("status") == "in_progress"
            )

            if self.current_workflow:
                self.current_workflow.tasks_completed = completed
                self.current_workflow.tasks_in_progress = in_progress
                self.current_workflow.stage = WorkflowStage.DAILY_STANDUP

            progress = {
                "sprint_name": sprint.name,
                "date": datetime.now().isoformat(),
                "total_tasks": len(sprint.tasks),
                "completed_tasks": completed,
                "in_progress_tasks": in_progress,
                "remaining_tasks": len(sprint.tasks) - completed - in_progress,
                "completion_percentage": (completed / len(sprint.tasks)) * 100
                if sprint.tasks
                else 0,
            }

            self.logger.info(f"Daily progress update: {progress}")
            return progress
        except Exception as e:
            self.logger.error(f"Failed to update daily progress: {e}")
            return {}

    def complete_sprint_workflow(self, sprint_id: str) -> Dict[str, Any]:
        """Complete sprint workflow and generate retrospective."""
        try:
            sprint = self.sprint_manager.sprints.get(sprint_id)
            if not sprint:
                return {}

            # Complete the sprint
            success = self.sprint_manager.complete_sprint(sprint_id)
            if not success:
                return {}

            # Generate retrospective data
            tasks = self.sprint_manager.get_sprint_tasks(sprint_id)
            completed = sum(1 for task in tasks if task.get("status") == "completed")

            retrospective = {
                "sprint_name": sprint.name,
                "completion_date": datetime.now().isoformat(),
                "total_tasks": len(sprint.tasks),
                "completed_tasks": completed,
                "success_rate": (completed / len(sprint.tasks)) * 100
                if sprint.tasks
                else 0,
                "workflow_stages": [stage.value for stage in WorkflowStage],
                "notes": "Sprint workflow completed successfully",
            }

            if self.current_workflow:
                self.current_workflow.stage = WorkflowStage.SPRINT_RETROSPECTIVE
                self.current_workflow.end_date = datetime.now()

            self.logger.info(f"Sprint workflow completed: {retrospective}")
            return retrospective
        except Exception as e:
            self.logger.error(f"Failed to complete sprint workflow: {e}")
            return {}

    def get_workflow_status(self) -> Optional[SprintWorkflow]:
        """Get current workflow status."""
        return self.current_workflow
