#!/usr/bin/env python3
"""
Sprint Management Launcher - Agent Cellphone V2
==============================================

Launches sprint management system with V2 integration.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import logging
import argparse

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import sys


@dataclass
class SprintLaunchConfig:
    """Sprint launch configuration."""

    mode: str
    sprint_id: Optional[str] = None
    action: str = "status"
    task_ids: Optional[list] = None
    duration_days: int = 14


class SprintManagementLauncher:
    """
    Sprint Management Launcher - Single responsibility: Sprint system launch.

    This launcher manages:
    - Sprint management service initialization
    - Sprint workflow service initialization
    - Command-line interface for sprint operations
    - Integration with V2 launcher system
    """

    def __init__(self, config_path: str = "config"):
        """Initialize Sprint Management Launcher."""
        self.config_path = Path(config_path)
        self.logger = self._setup_logging()
        self.status = "initialized"
        self.sprint_manager = None
        self.workflow_service = None

        # Initialize sprint services
        self._initialize_sprint_services()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("SprintManagementLauncher")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_sprint_services(self):
        """Initialize sprint management services."""
        try:

            # Add src to path for imports
            src_path = Path(__file__).parent.parent
            if str(src_path) not in sys.path:
                sys.path.insert(0, str(src_path))

            from core.workspace_manager import WorkspaceManager
            from core.task_manager import TaskManager
            from services.sprint_management_service import SprintManagementService
            from services.sprint_workflow_service import SprintWorkflowService

            # Initialize workspace and task managers
            workspace_manager = WorkspaceManager()
            task_manager = TaskManager(workspace_manager)

            # Initialize sprint services
            self.sprint_manager = SprintManagementService(
                workspace_manager, task_manager
            )
            self.workflow_service = SprintWorkflowService(
                self.sprint_manager, task_manager
            )

            self.logger.info("Sprint services initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize sprint services: {e}")
            raise

    def launch(self, config: SprintLaunchConfig) -> bool:
        """Launch sprint management system with specified configuration."""
        try:
            self.logger.info(f"Launching sprint management system: {config.mode}")

            if config.mode == "create":
                return self._create_sprint(config)
            elif config.mode == "plan":
                return self._plan_sprint(config)
            elif config.mode == "start":
                return self._start_sprint(config)
            elif config.mode == "status":
                return self._show_sprint_status(config)
            elif config.mode == "complete":
                return self._complete_sprint(config)
            elif config.mode == "progress":
                return self._update_progress(config)
            else:
                self.logger.error(f"Unknown mode: {config.mode}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to launch sprint management: {e}")
            return False

    def _create_sprint(self, config: SprintLaunchConfig) -> bool:
        """Create a new sprint."""
        try:
            if not config.sprint_id:
                config.sprint_id = "Sprint-" + datetime.now().strftime("%Y%m%d")

            sprint = self.sprint_manager.create_sprint(
                name=config.sprint_id,
                description=f"Auto-generated sprint {config.sprint_id}",
                duration_days=config.duration_days,
            )

            self.logger.info(f"Created sprint: {sprint.name} (ID: {sprint.sprint_id})")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create sprint: {e}")
            return False

    def _plan_sprint(self, config: SprintLaunchConfig) -> bool:
        """Plan tasks for a sprint."""
        try:
            if not config.sprint_id or not config.task_ids:
                self.logger.error("Sprint ID and task IDs required for planning")
                return False

            # Start planning workflow
            workflow = self.workflow_service.start_sprint_planning(config.sprint_id)

            # Plan tasks
            success = self.workflow_service.plan_sprint_tasks(
                config.sprint_id, config.task_ids
            )

            if success:
                self.logger.info(
                    f"Planned {len(config.task_ids)} tasks for sprint {config.sprint_id}"
                )
                return True
            else:
                self.logger.error("Failed to plan sprint tasks")
                return False
        except Exception as e:
            self.logger.error(f"Failed to plan sprint: {e}")
            return False

    def _start_sprint(self, config: SprintLaunchConfig) -> bool:
        """Start a sprint."""
        try:
            if not config.sprint_id:
                self.logger.error("Sprint ID required to start sprint")
                return False

            success = self.workflow_service.start_sprint_execution(config.sprint_id)

            if success:
                self.logger.info(f"Started sprint: {config.sprint_id}")
                return True
            else:
                self.logger.error("Failed to start sprint")
                return False
        except Exception as e:
            self.logger.error(f"Failed to start sprint: {e}")
            return False

    def _show_sprint_status(self, config: SprintLaunchConfig) -> bool:
        """Show sprint status."""
        try:
            if config.sprint_id:
                # Show specific sprint status
                sprint = self.sprint_manager.sprints.get(config.sprint_id)
                if sprint:
                    self.logger.info(f"Sprint: {sprint.name}")
                    self.logger.info(f"Status: {sprint.status.value}")
                    self.logger.info(f"Tasks: {len(sprint.tasks)}")
                    self.logger.info(f"Start: {sprint.start_date}")
                    self.logger.info(f"End: {sprint.end_date}")
                else:
                    self.logger.error(f"Sprint {config.sprint_id} not found")
                    return False
            else:
                # Show all sprints
                for sprint in self.sprint_manager.sprints.values():
                    self.logger.info(
                        f"{sprint.name}: {sprint.status.value} ({len(sprint.tasks)} tasks)"
                    )

            return True
        except Exception as e:
            self.logger.error(f"Failed to show sprint status: {e}")
            return False

    def _complete_sprint(self, config: SprintLaunchConfig) -> bool:
        """Complete a sprint."""
        try:
            if not config.sprint_id:
                self.logger.error("Sprint ID required to complete sprint")
                return False

            retrospective = self.workflow_service.complete_sprint_workflow(
                config.sprint_id
            )

            if retrospective:
                self.logger.info(f"Completed sprint: {config.sprint_id}")
                self.logger.info(
                    f"Success rate: {retrospective.get('success_rate', 0)}%"
                )
                return True
            else:
                self.logger.error("Failed to complete sprint")
                return False
        except Exception as e:
            self.logger.error(f"Failed to complete sprint: {e}")
            return False

    def _update_progress(self, config: SprintLaunchConfig) -> bool:
        """Update daily progress."""
        try:
            if not config.sprint_id:
                self.logger.error("Sprint ID required to update progress")
                return False

            progress = self.workflow_service.update_daily_progress(config.sprint_id)

            if progress:
                self.logger.info(f"Progress update for {progress.get('sprint_name')}")
                self.logger.info(
                    f"Completed: {progress.get('completed_tasks')}/{progress.get('total_tasks')}"
                )
                self.logger.info(
                    f"Completion: {progress.get('completion_percentage', 0):.1f}%"
                )
                return True
            else:
                self.logger.error("Failed to update progress")
                return False
        except Exception as e:
            self.logger.error(f"Failed to update progress: {e}")
            return False


def main():
    """Main entry point for sprint management launcher."""
    parser = argparse.ArgumentParser(description="Sprint Management Launcher V2")
    parser.add_argument(
        "mode", choices=["create", "plan", "start", "status", "complete", "progress"]
    )
    parser.add_argument("--sprint-id", help="Sprint ID")
    parser.add_argument("--task-ids", nargs="+", help="Task IDs for planning")
    parser.add_argument(
        "--duration", type=int, default=14, help="Sprint duration in days"
    )

    args = parser.parse_args()

    config = SprintLaunchConfig(
        mode=args.mode,
        sprint_id=args.sprint_id,
        task_ids=args.task_ids,
        duration_days=args.duration,
    )

    launcher = SprintManagementLauncher()
    success = launcher.launch(config)

    if success:
        print("Sprint management operation completed successfully")
    else:
        print("Sprint management operation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
