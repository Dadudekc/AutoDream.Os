#!/usr/bin/env python3
"""
Swarm Workflow Orchestrator - Core
===================================

Core workflow orchestration functionality for swarm coordination.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, core workflow management
"""

import json
from datetime import datetime
from pathlib import Path


class SwarmWorkflowOrchestratorCore:
    """Core workflow orchestration functionality"""

    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.agent_workspaces = self.project_root / "agent_workspaces"
        self.devlogs = self.project_root / "devlogs"
        self.tools = self.project_root / "src" / "tools"

        # Ensure directories exist
        self.agent_workspaces.mkdir(exist_ok=True)
        self.devlogs.mkdir(exist_ok=True)
        self.tools.mkdir(exist_ok=True)

    def create_workflow(self, name: str, description: str, phases: list[dict]) -> dict:
        """Create a new workflow definition."""
        workflow = {
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "phases": phases,
            "agents": self._extract_agents_from_phases(phases),
            "progress": {
                "total_phases": len(phases),
                "completed_phases": 0,
                "current_phase": 0,
                "overall_progress": 0.0,
            },
        }

        # Save workflow
        workflow_file = self.tools / f"workflows/{name.lower().replace(' ', '_')}_workflow.json"
        workflow_file.parent.mkdir(exist_ok=True)

        with open(workflow_file, "w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=2)

        return workflow

    def execute_workflow(self, workflow_name: str, dry_run: bool = False) -> dict:
        """Execute a workflow across all agents."""
        workflow_file = (
            self.tools / f"workflows/{workflow_name.lower().replace(' ', '_')}_workflow.json"
        )

        if not workflow_file.exists():
            raise FileNotFoundError(f"Workflow not found: {workflow_file}")

        with open(workflow_file, encoding="utf-8") as f:
            workflow = json.load(f)

        results = {
            "workflow_name": workflow_name,
            "started_at": datetime.now().isoformat(),
            "phases_executed": [],
            "messages_sent": [],
            "errors": [],
            "success": True,
        }

        for i, phase in enumerate(workflow["phases"]):
            phase_result = self._execute_phase(phase, i + 1, dry_run)
            results["phases_executed"].append(phase_result)

            if not phase_result["success"]:
                results["success"] = False
                results["errors"].append(f"Phase {i + 1} failed: {phase_result['error']}")
                break

        results["completed_at"] = datetime.now().isoformat()
        results["duration"] = self._calculate_duration(
            results["started_at"], results["completed_at"]
        )

        return results

    def _execute_phase(self, phase: dict, phase_number: int, dry_run: bool) -> dict:
        """Execute a single phase of the workflow."""
        phase_result = {
            "phase_number": phase_number,
            "phase_name": phase["name"],
            "started_at": datetime.now().isoformat(),
            "tasks_executed": [],
            "messages_sent": [],
            "success": True,
            "error": None,
        }

        try:
            for task in phase.get("tasks", []):
                task_result = self._execute_task(task, dry_run)
                phase_result["tasks_executed"].append(task_result)

                if not task_result["success"]:
                    phase_result["success"] = False
                    phase_result["error"] = task_result["error"]
                    break

            phase_result["completed_at"] = datetime.now().isoformat()

        except Exception as e:
            phase_result["success"] = False
            phase_result["error"] = str(e)
            phase_result["completed_at"] = datetime.now().isoformat()

        return phase_result

    def _execute_task(self, task: dict, dry_run: bool) -> dict:
        """Execute a single task within a phase."""
        task_result = {
            "task_name": task["name"],
            "task_type": task["type"],
            "started_at": datetime.now().isoformat(),
            "success": True,
            "error": None,
            "output": None,
        }

        try:
            if dry_run:
                task_result["output"] = f"DRY RUN: Would execute {task['type']} - {task['name']}"
                return task_result

            if task["type"] == "send_message":
                result = self._send_agent_message(
                    task["agent"],
                    task["message"],
                    task.get("priority", "NORMAL"),
                    task.get("tags", []),
                )
                task_result["output"] = result

            elif task["type"] == "create_task_file":
                result = self._create_task_file(
                    task["agent"], task["tasks"], task.get("priority", "HIGH")
                )
                task_result["output"] = result

            elif task["type"] == "create_devlog":
                result = self._create_devlog(
                    task["title"], task["content"], task.get("priority", "NORMAL")
                )
                task_result["output"] = result

            elif task["type"] == "wait_for_completion":
                result = self._wait_for_agent_completion(task["agent"], task.get("timeout", 300))
                task_result["output"] = result

            else:
                task_result["success"] = False
                task_result["error"] = f"Unknown task type: {task['type']}"

            task_result["completed_at"] = datetime.now().isoformat()

        except Exception as e:
            task_result["success"] = False
            task_result["error"] = str(e)
            task_result["completed_at"] = datetime.now().isoformat()

        return task_result

    def _extract_agents_from_phases(self, phases: list[dict]) -> list[str]:
        """Extract unique agents from workflow phases."""
        agents = set()
        for phase in phases:
            for task in phase.get("tasks", []):
                if "agent" in task:
                    agents.add(task["agent"])
        return list(agents)

    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """Calculate duration between two timestamps."""
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        duration = end - start
        return str(duration)

    def list_workflows(self) -> list[dict]:
        """List all available workflows."""
        workflows_dir = self.tools / "workflows"
        if not workflows_dir.exists():
            return []

        workflows = []
        for workflow_file in workflows_dir.glob("*.json"):
            with open(workflow_file, encoding="utf-8") as f:
                workflow = json.load(f)
                workflows.append(
                    {
                        "name": workflow["name"],
                        "file": workflow_file.name,
                        "status": workflow["status"],
                        "phases": len(workflow["phases"]),
                        "agents": len(workflow["agents"]),
                    }
                )

        return workflows

    def get_workflow_status(self, workflow_name: str) -> dict:
        """Get the current status of a workflow."""
        workflow_file = (
            self.tools / f"workflows/{workflow_name.lower().replace(' ', '_')}_workflow.json"
        )

        if not workflow_file.exists():
            raise FileNotFoundError(f"Workflow not found: {workflow_file}")

        with open(workflow_file, encoding="utf-8") as f:
            workflow = json.load(f)

        return workflow["progress"]
