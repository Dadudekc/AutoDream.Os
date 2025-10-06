#!/usr/bin/env python3
"""
Workflow Automation - Task Assignment
=====================================

Handles task assignment automation for agent workflows.
V2 Compliant: ≤400 lines, focused task assignment.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class TaskAssignmentAutomation:
    """Handles task assignment automation."""

    def __init__(self, workflow_log_path: Path):
        """Initialize task assignment automation."""
        self.workflow_log_path = workflow_log_path

    def assign_task(
        self,
        task_id: str,
        title: str,
        description: str,
        assigned_to: str,
        assigned_by: str,
        priority: str = "normal",
    ) -> bool:
        """Automatically assign task to agent."""
        try:
            # Create working task file
            agent_dir = Path(f"agent_workspaces/{assigned_to}")
            agent_dir.mkdir(parents=True, exist_ok=True)

            working_task = {
                "task_id": task_id,
                "title": title,
                "description": description,
                "assigned_to": assigned_to,
                "assigned_by": assigned_by,
                "priority": priority,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
            }

            task_file = agent_dir / f"working_task_{task_id}.json"
            with open(task_file, "w") as f:
                json.dump(working_task, f, indent=2)

            # Create inbox notification
            inbox_dir = agent_dir / "inbox"
            inbox_dir.mkdir(exist_ok=True)

            notification = {
                "type": "task_assignment",
                "task_id": task_id,
                "title": title,
                "assigned_by": assigned_by,
                "priority": priority,
                "timestamp": datetime.now().isoformat(),
            }

            notification_file = inbox_dir / f"task_assignment_{task_id}.json"
            with open(notification_file, "w") as f:
                json.dump(notification, f, indent=2)

            # Log workflow
            self._log_workflow(
                "task_assignment",
                {
                    "task_id": task_id,
                    "assigned_to": assigned_to,
                    "assigned_by": assigned_by,
                    "priority": priority,
                    "status": "success",
                },
            )

            logger.info(f"Task {task_id} assigned to {assigned_to} by {assigned_by}")
            return True

        except Exception as e:
            logger.error(f"Task assignment failed: {e}")
            return False

    def update_task_status(self, task_id: str, assigned_to: str, status: str) -> bool:
        """Update task status."""
        try:
            task_file = Path(f"agent_workspaces/{assigned_to}/working_task_{task_id}.json")
            
            if not task_file.exists():
                logger.error(f"Task file not found: {task_file}")
                return False

            # Load existing task
            with open(task_file, "r") as f:
                task_data = json.load(f)

            # Update status
            task_data["status"] = status
            task_data["updated_at"] = datetime.now().isoformat()

            # Save updated task
            with open(task_file, "w") as f:
                json.dump(task_data, f, indent=2)

            # Log workflow
            self._log_workflow(
                "task_status_update",
                {
                    "task_id": task_id,
                    "assigned_to": assigned_to,
                    "status": status,
                    "status": "success",
                },
            )

            logger.info(f"Task {task_id} status updated to {status}")
            return True

        except Exception as e:
            logger.error(f"Task status update failed: {e}")
            return False

    def get_task_status(self, task_id: str, assigned_to: str) -> Dict[str, Any]:
        """Get task status."""
        try:
            task_file = Path(f"agent_workspaces/{assigned_to}/working_task_{task_id}.json")
            
            if not task_file.exists():
                return {"error": "Task not found"}

            with open(task_file, "r") as f:
                task_data = json.load(f)

            return task_data

        except Exception as e:
            logger.error(f"Failed to get task status: {e}")
            return {"error": str(e)}

    def list_agent_tasks(self, assigned_to: str) -> list:
        """List all tasks for an agent."""
        try:
            agent_dir = Path(f"agent_workspaces/{assigned_to}")
            
            if not agent_dir.exists():
                return []

            tasks = []
            for task_file in agent_dir.glob("working_task_*.json"):
                try:
                    with open(task_file, "r") as f:
                        task_data = json.load(f)
                        tasks.append(task_data)
                except Exception as e:
                    logger.error(f"Failed to load task file {task_file}: {e}")

            return tasks

        except Exception as e:
            logger.error(f"Failed to list agent tasks: {e}")
            return []

    def _log_workflow(self, action: str, details: Dict[str, Any]) -> None:
        """Log workflow action."""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "details": details,
            }

            # Load existing log
            if self.workflow_log_path.exists():
                with open(self.workflow_log_path, "r") as f:
                    log_data = json.load(f)
            else:
                log_data = {"workflows": []}

            # Add new entry
            log_data["workflows"].append(log_entry)

            # Save updated log
            with open(self.workflow_log_path, "w") as f:
                json.dump(log_data, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to log workflow: {e}")


def create_task_assignment_automation(workflow_log_path: Path) -> TaskAssignmentAutomation:
    """Create task assignment automation."""
    return TaskAssignmentAutomation(workflow_log_path)

