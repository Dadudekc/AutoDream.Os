#!/usr/bin/env python3
"""
Status Monitor
==============

Comprehensive status monitoring for messaging system and project health.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class StatusMonitor:
    """Status monitoring for messaging system and project health."""

    def __init__(self, messaging_service):
        """Initialize status monitor with messaging service reference."""
        self.messaging_service = messaging_service

    def get_comprehensive_status(self) -> dict[str, Any]:
        """Get comprehensive system status."""
        return {
            "status": "operational",
            "agent_count": len(self.messaging_service.loader.get_agent_ids()),
            "agents": self.messaging_service.loader.get_agent_ids(),
            "project_scanner": self._get_project_scanner_status(),
            "fsm_status": self._get_fsm_status(),
            "agent_tasks": self._get_agent_task_statuses(),
            "system_health": self._get_system_health(),
        }

    def _get_project_scanner_status(self) -> dict[str, Any]:
        """Get project scanner status."""
        try:
            # Check if project analysis files exist
            project_analysis = Path("project_analysis.json")
            chatgpt_context = Path("chatgpt_project_context.json")

            status = {
                "project_analysis_exists": project_analysis.exists(),
                "chatgpt_context_exists": chatgpt_context.exists(),
                "last_scan": "unknown",
            }

            if project_analysis.exists():
                try:
                    with open(project_analysis) as f:
                        data = json.load(f)
                        status["last_scan"] = data.get("scan_timestamp", "unknown")
                        status["total_files"] = data.get("total_files", 0)
                        status["v2_compliance"] = data.get("v2_compliance_percentage", 0)
                except Exception as e:
                    logger.warning(f"Error reading project analysis: {e}")

            return status

        except Exception as e:
            logger.error(f"Error getting project scanner status: {e}")
            return {"error": str(e)}

    def _get_fsm_status(self) -> dict[str, Any]:
        """Get FSM state machine status."""
        try:
            fsm_dir = Path("data/semantic_seed/status")
            if not fsm_dir.exists():
                return {"status": "not_found", "agents": []}

            agent_statuses = {}
            for agent_file in fsm_dir.glob("Agent-*.json"):
                try:
                    with open(agent_file) as f:
                        data = json.load(f)
                        agent_id = agent_file.stem
                        agent_statuses[agent_id] = {
                            "current_state": data.get("current_state", "unknown"),
                            "phase": data.get("phase", "unknown"),
                            "last_update": data.get("last_update", "unknown"),
                        }
                except Exception as e:
                    logger.warning(f"Error reading FSM status for {agent_file}: {e}")

            return {
                "status": "operational",
                "agents": agent_statuses,
                "total_agents": len(agent_statuses),
            }

        except Exception as e:
            logger.error(f"Error getting FSM status: {e}")
            return {"error": str(e)}

    def _get_agent_task_statuses(self) -> dict[str, Any]:
        """Get agent task statuses."""
        try:
            agent_workspaces = Path("agent_workspaces")
            if not agent_workspaces.exists():
                return {"status": "not_found", "agents": []}

            agent_tasks = {}
            for agent_dir in agent_workspaces.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agent_id = agent_dir.name

                    # Check working tasks
                    working_tasks_file = agent_dir / "working_tasks.json"
                    future_tasks_file = agent_dir / "future_tasks.json"

                    tasks_info = {"working_tasks": 0, "future_tasks": 0, "current_task": None}

                    if working_tasks_file.exists():
                        try:
                            with open(working_tasks_file) as f:
                                data = json.load(f)
                                tasks_info["working_tasks"] = len(data.get("tasks", []))
                                tasks_info["current_task"] = data.get("current_task")
                        except Exception as e:
                            logger.warning(f"Error reading working tasks for {agent_id}: {e}")

                    if future_tasks_file.exists():
                        try:
                            with open(future_tasks_file) as f:
                                data = json.load(f)
                                tasks_info["future_tasks"] = len(data.get("tasks", []))
                        except Exception as e:
                            logger.warning(f"Error reading future tasks for {agent_id}: {e}")

                    agent_tasks[agent_id] = tasks_info

            return {
                "status": "operational",
                "agents": agent_tasks,
                "total_agents": len(agent_tasks),
            }

        except Exception as e:
            logger.error(f"Error getting agent task statuses: {e}")
            return {"error": str(e)}

    def _get_system_health(self) -> dict[str, Any]:
        """Get overall system health."""
        try:
            # Check coordinate validation
            coord_health = self.messaging_service.validation_report.is_all_ok()

            # Check PyAutoGUI availability
            pyautogui_available = self.messaging_service.loader is not None

            # Check agent count
            agent_count = len(self.messaging_service.loader.get_agent_ids())

            return {
                "coordinates_valid": coord_health,
                "pyautogui_available": pyautogui_available,
                "agent_count": agent_count,
                "overall_status": "healthy" if coord_health and pyautogui_available else "degraded",
            }

        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return {"error": str(e), "overall_status": "error"}
