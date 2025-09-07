#!/usr/bin/env python3
"""FSM persistence and setup mixin."""

import json
import logging
from dataclasses import asdict
from pathlib import Path

from .fsm_utils import FSMCommunicationEvent, FSMTask, TaskState

logger = logging.getLogger(__name__)


class FSMPersistenceMixin:
    """Mixin handling persistence and workspace setup for the FSM system."""

    def _load_manager_config(self) -> None:
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    if "fsm" in config:
                        fsm_config = config["fsm"]
                        self.max_tasks_per_agent = fsm_config.get("max_tasks_per_agent", 10)
                        self.task_timeout_hours = fsm_config.get("task_timeout_hours", 24)
                        self.auto_cleanup_completed = fsm_config.get("auto_cleanup_completed", True)
                        self.enable_discord_bridge = fsm_config.get("enable_discord_bridge", True)
            else:
                logger.warning("FSM config file not found: %s", self.config_path)
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to load FSM config: {e}")

    def _initialize_fsm_workspace(self) -> None:
        """Initialize FSM workspace"""
        self.workspace_path = Path("fsm_workspaces")
        self.workspace_path.mkdir(exist_ok=True)
        logger.info("FSM workspace initialized")

    def _load_existing_tasks(self) -> None:
        """Load existing FSM tasks from storage"""
        try:
            task_files = list(self.workspace_path.glob("task_*.json"))
            for task_file in task_files:
                try:
                    with open(task_file, "r") as f:
                        task_data = json.load(f)
                        task = FSMTask.from_dict(task_data)
                        self._tasks[task.id] = task
                except Exception as e:  # pragma: no cover - log failure path
                    logger.warning("Failed to load task from %s: %s", task_file, e)
            logger.info("Loaded %d existing FSM tasks", len(self._tasks))
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to load existing tasks: {e}")

    def _save_task(self, task: FSMTask) -> None:
        """Save task to storage"""
        try:
            task_file = self.workspace_path / f"task_{task.id}.json"
            with open(task_file, "w") as f:
                json.dump(task.to_dict(), f, indent=2)
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to save task {task.id}: {e}")

    def _save_communication_event(self, event: FSMCommunicationEvent) -> None:
        """Save communication event to storage"""
        try:
            event_file = self.workspace_path / f"event_{event.event_id}.json"
            with open(event_file, "w") as f:
                json.dump(asdict(event), f, indent=2)
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to save communication event {event.event_id}: {e}")

    def cleanup(self) -> None:
        """Cleanup FSM system manager resources"""
        try:
            if self.auto_cleanup_completed:
                completed_tasks = [t for t in self._tasks.values() if t.state == TaskState.COMPLETED]
                for task in completed_tasks:
                    del self._tasks[task.id]
                    task_file = self.workspace_path / f"task_{task.id}.json"
                    if task_file.exists():
                        task_file.unlink()
                logger.info("Cleaned up %d completed tasks", len(completed_tasks))
            logger.info("FSMSystemManager cleanup completed")
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"FSMSystemManager cleanup failed: {e}")
