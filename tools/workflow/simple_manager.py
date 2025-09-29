#!/usr/bin/env python3
"""
Simple Workflow Manager
=======================

Simplified version of the workflow manager with essential functionality only.
V2 Compliance: ≤400 lines, focused on core features.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SimpleWorkflowStep:
    """Simple workflow step with minimal features."""

    def __init__(self, step_id: str, agent_id: str, task: str, dependencies: list[str] = None):
        self.step_id = step_id
        self.agent_id = agent_id
        self.task = task
        self.dependencies = dependencies or []
        self.status = "pending"
        self.result = None
        self.created_at = datetime.now()
        self.completed_at = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "step_id": self.step_id,
            "agent_id": self.agent_id,
            "task": self.task,
            "dependencies": self.dependencies,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SimpleWorkflowStep":
        """Create from dictionary."""
        step = cls(
            step_id=data["step_id"],
            agent_id=data["agent_id"],
            task=data["task"],
            dependencies=data.get("dependencies", []),
        )
        step.status = data.get("status", "pending")
        step.result = data.get("result")

        if data.get("created_at"):
            step.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("completed_at"):
            step.completed_at = datetime.fromisoformat(data["completed_at"])

        return step


class SimpleWorkflow:
    """Simple workflow with minimal features."""

    def __init__(self, workflow_id: str, name: str, steps: list[SimpleWorkflowStep]):
        self.workflow_id = workflow_id
        self.name = name
        self.steps = steps
        self.status = "pending"
        self.created_at = datetime.now()
        self.completed_at = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "steps": [step.to_dict() for step in self.steps],
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SimpleWorkflow":
        """Create from dictionary."""
        steps = [SimpleWorkflowStep.from_dict(step_data) for step_data in data["steps"]]
        workflow = cls(workflow_id=data["workflow_id"], name=data["name"], steps=steps)
        workflow.status = data.get("status", "pending")

        if data.get("created_at"):
            workflow.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("completed_at"):
            workflow.completed_at = datetime.fromisoformat(data["completed_at"])

        return workflow


class SimpleWorkflowManager:
    """Simple workflow manager with essential functionality."""

    def __init__(self, workflows_dir: str = "workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.workflows_dir.mkdir(exist_ok=True)
        self.workflows: dict[str, SimpleWorkflow] = {}
        self._load_workflows()

    def _load_workflows(self):
        """Load existing workflows from disk."""
        try:
            for workflow_file in self.workflows_dir.glob("*.json"):
                try:
                    with open(workflow_file) as f:
                        data = json.load(f)
                    workflow = SimpleWorkflow.from_dict(data)
                    self.workflows[workflow.workflow_id] = workflow
                except Exception as e:
                    logger.error(f"Failed to load workflow {workflow_file}: {e}")
        except Exception as e:
            logger.error(f"Failed to load workflows: {e}")

    def create_workflow(
        self, workflow_id: str, name: str, steps_data: list[dict[str, Any]]
    ) -> SimpleWorkflow:
        """Create a new workflow."""
        steps = []
        for step_data in steps_data:
            step = SimpleWorkflowStep(
                step_id=step_data["step_id"],
                agent_id=step_data["agent_id"],
                task=step_data["task"],
                dependencies=step_data.get("dependencies", []),
            )
            steps.append(step)

        workflow = SimpleWorkflow(workflow_id, name, steps)
        self.workflows[workflow_id] = workflow
        return workflow

    def save_workflow(self, workflow: SimpleWorkflow) -> bool:
        """Save workflow to disk."""
        try:
            workflow_file = self.workflows_dir / f"{workflow.workflow_id}.json"
            with open(workflow_file, "w") as f:
                json.dump(workflow.to_dict(), f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save workflow {workflow.workflow_id}: {e}")
            return False

    def load_workflow(self, workflow_id: str) -> SimpleWorkflow | None:
        """Load workflow from disk."""
        if workflow_id in self.workflows:
            return self.workflows[workflow_id]

        workflow_file = self.workflows_dir / f"{workflow_id}.json"
        if workflow_file.exists():
            try:
                with open(workflow_file) as f:
                    data = json.load(f)
                workflow = SimpleWorkflow.from_dict(data)
                self.workflows[workflow_id] = workflow
                return workflow
            except Exception as e:
                logger.error(f"Failed to load workflow {workflow_id}: {e}")

        return None

    def list_workflows(self) -> list[dict[str, Any]]:
        """List all workflows."""
        workflows = []
        for workflow in self.workflows.values():
            workflows.append(
                {
                    "workflow_id": workflow.workflow_id,
                    "name": workflow.name,
                    "status": workflow.status,
                    "step_count": len(workflow.steps),
                    "created_at": workflow.created_at.isoformat(),
                }
            )
        return workflows

    def execute_workflow(self, workflow: SimpleWorkflow) -> dict[str, Any]:
        """Execute workflow with simple sequential processing."""
        try:
            workflow.status = "running"
            results = {}

            # Simple sequential execution
            for step in workflow.steps:
                step.status = "running"
                result = self._execute_step(step)
                step.result = result
                step.status = "completed" if result.get("success") else "failed"
                step.completed_at = datetime.now()
                results[step.step_id] = result

            # Check if all steps completed successfully
            all_success = all(step.status == "completed" for step in workflow.steps)
            workflow.status = "completed" if all_success else "failed"
            workflow.completed_at = datetime.now()

            return {"success": all_success, "results": results, "workflow_status": workflow.status}

        except Exception as e:
            workflow.status = "failed"
            logger.error(f"Workflow execution failed: {e}")
            return {"success": False, "error": str(e), "workflow_status": workflow.status}

    def _execute_step(self, step: SimpleWorkflowStep) -> dict[str, Any]:
        """Execute a single step."""
        try:
            # Simple step execution - just log the task
            logger.info(f"Executing step {step.step_id}: {step.task}")

            # Simulate task execution
            import time

            time.sleep(0.1)  # Small delay to simulate work

            return {
                "success": True,
                "result": f"Task '{step.task}' completed by {step.agent_id}",
                "execution_time": 0.1,
            }

        except Exception as e:
            logger.error(f"Step execution failed: {e}")
            return {"success": False, "error": str(e)}

    def get_workflow_status(self, workflow_id: str) -> str | None:
        """Get workflow status."""
        workflow = self.load_workflow(workflow_id)
        return workflow.status if workflow else None

    def delete_workflow(self, workflow_id: str) -> bool:
        """Delete workflow."""
        try:
            # Remove from memory
            if workflow_id in self.workflows:
                del self.workflows[workflow_id]

            # Remove from disk
            workflow_file = self.workflows_dir / f"{workflow_id}.json"
            if workflow_file.exists():
                workflow_file.unlink()

            return True
        except Exception as e:
            logger.error(f"Failed to delete workflow {workflow_id}: {e}")
            return False


def main():
    """Simple CLI for workflow management."""
    import argparse

    parser = argparse.ArgumentParser(description="Simple Workflow Manager")
    parser.add_argument("--workflows-dir", default="workflows", help="Workflows directory")
    parser.add_argument(
        "--action",
        choices=["create", "list", "execute", "status"],
        required=True,
        help="Action to perform",
    )
    parser.add_argument("--workflow-id", help="Workflow ID")
    parser.add_argument("--name", help="Workflow name")
    parser.add_argument("--steps", help="Steps JSON file")

    args = parser.parse_args()

    manager = SimpleWorkflowManager(args.workflows_dir)

    if args.action == "list":
        workflows = manager.list_workflows()
        print("Workflows:")
        for workflow in workflows:
            print(f"  {workflow['workflow_id']}: {workflow['name']} ({workflow['status']})")

    elif args.action == "create":
        if not args.workflow_id or not args.name or not args.steps:
            print("Error: --workflow-id, --name, and --steps are required for create")
            return 1

        with open(args.steps) as f:
            steps_data = json.load(f)

        workflow = manager.create_workflow(args.workflow_id, args.name, steps_data)
        manager.save_workflow(workflow)
        print(f"Created workflow: {workflow.workflow_id}")

    elif args.action == "execute":
        if not args.workflow_id:
            print("Error: --workflow-id is required for execute")
            return 1

        workflow = manager.load_workflow(args.workflow_id)
        if not workflow:
            print(f"Error: Workflow {args.workflow_id} not found")
            return 1

        result = manager.execute_workflow(workflow)
        manager.save_workflow(workflow)

        if result["success"]:
            print(f"Workflow {args.workflow_id} executed successfully")
        else:
            print(f"Workflow {args.workflow_id} failed: {result.get('error')}")

    elif args.action == "status":
        if not args.workflow_id:
            print("Error: --workflow-id is required for status")
            return 1

        status = manager.get_workflow_status(args.workflow_id)
        if status:
            print(f"Workflow {args.workflow_id} status: {status}")
        else:
            print(f"Workflow {args.workflow_id} not found")

    return 0


if __name__ == "__main__":
    exit(main())
