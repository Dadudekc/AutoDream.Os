#!/usr/bin/env python3
"""
Workflow Automation - Project Coordination
===========================================

Handles project coordination automation for agent workflows.
V2 Compliant: ≤400 lines, focused project coordination.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ProjectCoordinationAutomation:
    """Handles project coordination automation."""

    def __init__(self, workflow_log_path: Path):
        """Initialize project coordination automation."""
        self.workflow_log_path = workflow_log_path

    def coordinate_project(
        self,
        project_name: str,
        coordinator: str,
        participating_agents: List[str],
        tasks: List[Dict[str, Any]],
    ) -> bool:
        """Coordinate project across multiple agents."""
        try:
            timestamp = datetime.now()
            project_id = f"PROJECT_{project_name.upper()}_{timestamp.strftime('%Y%m%d_%H%M%S')}"

            # Create project directory
            project_dir = Path(f"projects/{project_name}")
            project_dir.mkdir(parents=True, exist_ok=True)

            # Create project coordination file
            coord_data = {
                "project_id": project_id,
                "project_name": project_name,
                "coordinator": coordinator,
                "participating_agents": participating_agents,
                "tasks": tasks,
                "status": "active",
                "created_at": timestamp.isoformat(),
            }

            coord_file = project_dir / "coordination.json"
            with open(coord_file, "w") as f:
                json.dump(coord_data, f, indent=2)

            # Notify all participating agents
            for agent_id in participating_agents:
                self._create_project_notification(agent_id, project_name, coordinator, project_id)

            # Log workflow
            self._log_workflow(
                "project_coordination",
                {
                    "project_id": project_id,
                    "project_name": project_name,
                    "coordinator": coordinator,
                    "participating_agents": participating_agents,
                    "status": "success",
                },
            )

            logger.info(
                f"Project coordinated: {project_name} with {len(participating_agents)} agents"
            )
            return True

        except Exception as e:
            logger.error(f"Project coordination failed: {e}")
            return False

    def update_project_status(self, project_name: str, status: str) -> bool:
        """Update project status."""
        try:
            project_dir = Path(f"projects/{project_name}")
            coord_file = project_dir / "coordination.json"
            
            if not coord_file.exists():
                logger.error(f"Project coordination file not found: {coord_file}")
                return False

            # Load existing coordination data
            with open(coord_file, "r") as f:
                coord_data = json.load(f)

            # Update status
            coord_data["status"] = status
            coord_data["updated_at"] = datetime.now().isoformat()

            # Save updated coordination data
            with open(coord_file, "w") as f:
                json.dump(coord_data, f, indent=2)

            # Log workflow
            self._log_workflow(
                "project_status_update",
                {
                    "project_name": project_name,
                    "status": status,
                    "status": "success",
                },
            )

            logger.info(f"Project {project_name} status updated to {status}")
            return True

        except Exception as e:
            logger.error(f"Project status update failed: {e}")
            return False

    def get_project_info(self, project_name: str) -> Dict[str, Any]:
        """Get project information."""
        try:
            project_dir = Path(f"projects/{project_name}")
            coord_file = project_dir / "coordination.json"
            
            if not coord_file.exists():
                return {"error": "Project not found"}

            with open(coord_file, "r") as f:
                coord_data = json.load(f)

            return coord_data

        except Exception as e:
            logger.error(f"Failed to get project info: {e}")
            return {"error": str(e)}

    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects."""
        try:
            projects_dir = Path("projects")
            
            if not projects_dir.exists():
                return []

            projects = []
            for project_dir in projects_dir.iterdir():
                if project_dir.is_dir():
                    coord_file = project_dir / "coordination.json"
                    if coord_file.exists():
                        try:
                            with open(coord_file, "r") as f:
                                coord_data = json.load(f)
                                projects.append(coord_data)
                        except Exception as e:
                            logger.error(f"Failed to load project file {coord_file}: {e}")

            return projects

        except Exception as e:
            logger.error(f"Failed to list projects: {e}")
            return []

    def add_project_task(self, project_name: str, task: Dict[str, Any]) -> bool:
        """Add task to project."""
        try:
            project_dir = Path(f"projects/{project_name}")
            coord_file = project_dir / "coordination.json"
            
            if not coord_file.exists():
                logger.error(f"Project coordination file not found: {coord_file}")
                return False

            # Load existing coordination data
            with open(coord_file, "r") as f:
                coord_data = json.load(f)

            # Add task
            if "tasks" not in coord_data:
                coord_data["tasks"] = []
            
            coord_data["tasks"].append(task)
            coord_data["updated_at"] = datetime.now().isoformat()

            # Save updated coordination data
            with open(coord_file, "w") as f:
                json.dump(coord_data, f, indent=2)

            logger.info(f"Task added to project {project_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to add project task: {e}")
            return False

    def _create_project_notification(self, agent_id: str, project_name: str, coordinator: str, project_id: str) -> None:
        """Create project notification for agent."""
        try:
            agent_dir = Path(f"agent_workspaces/{agent_id}")
            agent_dir.mkdir(parents=True, exist_ok=True)

            inbox_dir = agent_dir / "inbox"
            inbox_dir.mkdir(exist_ok=True)

            notification = {
                "type": "project_coordination",
                "project_id": project_id,
                "project_name": project_name,
                "coordinator": coordinator,
                "timestamp": datetime.now().isoformat(),
            }

            notification_file = inbox_dir / f"project_coordination_{project_id}.json"
            with open(notification_file, "w") as f:
                json.dump(notification, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to create project notification: {e}")

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


def create_project_coordination_automation(workflow_log_path: Path) -> ProjectCoordinationAutomation:
    """Create project coordination automation."""
    return ProjectCoordinationAutomation(workflow_log_path)

