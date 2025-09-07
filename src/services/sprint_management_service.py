#!/usr/bin/env python3
"""
Sprint Management Service - Agent Cellphone V2
=============================================

Integrates ai-task-organizer sprint system with V2 architecture.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import uuid


class SprintStatus(Enum):
    """Sprint status states."""

    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Sprint:
    """Sprint data structure with 10-task limit."""

    sprint_id: str
    name: str
    description: str
    status: SprintStatus
    start_date: str
    end_date: str
    max_tasks: int = 10
    tasks: List[str] = None  # List of task IDs
    created_at: str = None
    completed_at: Optional[str] = None

    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class SprintManagementService:
    """
    Sprint Management Service - Single responsibility: Sprint lifecycle management.

    This service manages:
    - Sprint creation and planning
    - 10-task per sprint enforcement
    - Sprint status transitions
    - Sprint completion and retrospective
    """

    def __init__(self, workspace_manager, task_manager):
        """Initialize Sprint Management Service."""
        self.workspace_manager = workspace_manager
        self.task_manager = task_manager
        self.logger = self._setup_logging()
        self.sprints: Dict[str, Sprint] = {}
        self.status = "initialized"

        # Load existing sprints
        self._load_sprints()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("SprintManagementService")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_sprints(self):
        """Load existing sprints from workspace."""
        try:
            sprints_path = self.workspace_manager.get_sprints_path()
            if sprints_path.exists():
                for sprint_file in sprints_path.glob("*.json"):
                    try:
                        with open(sprint_file, "r") as f:
                            sprint_data = json.load(f)
                            sprint = Sprint(**sprint_data)
                            self.sprints[sprint.sprint_id] = sprint
                    except Exception as e:
                        self.logger.error(f"Failed to load sprint {sprint_file}: {e}")
        except Exception as e:
            self.logger.error(f"Failed to load sprints: {e}")

    def create_sprint(
        self, name: str, description: str, duration_days: int = 14
    ) -> Sprint:
        """Create a new sprint with 10-task limit."""
        try:
            sprint_id = str(uuid.uuid4())
            start_date = datetime.now()
            end_date = start_date + timedelta(days=duration_days)

            sprint = Sprint(
                sprint_id=sprint_id,
                name=name,
                description=description,
                status=SprintStatus.PLANNING,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
            )

            self.sprints[sprint_id] = sprint
            self._save_sprint(sprint)
            self.logger.info(f"Created sprint: {name} (ID: {sprint_id})")

            return sprint
        except Exception as e:
            self.logger.error(f"Failed to create sprint: {e}")
            raise

    def add_task_to_sprint(self, sprint_id: str, task_id: str) -> bool:
        """Add task to sprint if under 10-task limit."""
        try:
            if sprint_id not in self.sprints:
                self.logger.error(f"Sprint {sprint_id} not found")
                return False

            sprint = self.sprints[sprint_id]

            if len(sprint.tasks) >= sprint.max_tasks:
                self.logger.warning(
                    f"Sprint {sprint.name} already has {sprint.max_tasks} tasks"
                )
                return False

            if task_id not in sprint.tasks:
                sprint.tasks.append(task_id)
                self._save_sprint(sprint)
                self.logger.info(f"Added task {task_id} to sprint {sprint.name}")
                return True

            return False
        except Exception as e:
            self.logger.error(f"Failed to add task to sprint: {e}")
            return False

    def start_sprint(self, sprint_id: str) -> bool:
        """Start an active sprint."""
        try:
            if sprint_id not in self.sprints:
                return False

            sprint = self.sprints[sprint_id]
            if sprint.status != SprintStatus.PLANNING:
                self.logger.warning(
                    f"Sprint {sprint.name} cannot be started from {sprint.status}"
                )
                return False

            sprint.status = SprintStatus.ACTIVE
            self._save_sprint(sprint)
            self.logger.info(f"Started sprint: {sprint.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start sprint: {e}")
            return False

    def complete_sprint(self, sprint_id: str) -> bool:
        """Complete an active sprint."""
        try:
            if sprint_id not in self.sprints:
                return False

            sprint = self.sprints[sprint_id]
            if sprint.status != SprintStatus.ACTIVE:
                self.logger.warning(
                    f"Sprint {sprint.name} cannot be completed from {sprint.status}"
                )
                return False

            sprint.status = SprintStatus.COMPLETED
            sprint.completed_at = datetime.now().isoformat()
            self._save_sprint(sprint)
            self.logger.info(f"Completed sprint: {sprint.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to complete sprint: {e}")
            return False

    def get_sprint_tasks(self, sprint_id: str) -> List[Dict[str, Any]]:
        """Get all tasks in a sprint with full details."""
        try:
            if sprint_id not in self.sprints:
                return []

            sprint = self.sprints[sprint_id]
            tasks = []

            for task_id in sprint.tasks:
                task = self.task_manager.get_task(task_id)
                if task:
                    tasks.append(asdict(task))

            return tasks
        except Exception as e:
            self.logger.error(f"Failed to get sprint tasks: {e}")
            return []

    def get_active_sprint(self) -> Optional[Sprint]:
        """Get the currently active sprint."""
        try:
            for sprint in self.sprints.values():
                if sprint.status == SprintStatus.ACTIVE:
                    return sprint
            return None
        except Exception as e:
            self.logger.error(f"Failed to get active sprint: {e}")
            return None

    def _save_sprint(self, sprint: Sprint):
        """Save sprint to workspace."""
        try:
            sprints_path = self.workspace_manager.get_sprints_path()
            sprints_path.mkdir(parents=True, exist_ok=True)

            # Convert enum to string for JSON serialization
            sprint_data = asdict(sprint)
            sprint_data["status"] = sprint.status.value

            sprint_file = sprints_path / f"{sprint.sprint_id}.json"
            with open(sprint_file, "w") as f:
                json.dump(sprint_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save sprint: {e}")
            raise
