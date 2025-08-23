#!/usr/bin/env python3
"""
Workflow Service - Agent Cellphone V2
====================================

Workflow coordination and task management service.
Follows V2 standards: ≤ 200 LOC, SRP, OOP design, CLI interface.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import argparse


@dataclass
class WorkflowTask:
    """Workflow task data structure."""

    task_id: str
    workflow_type: str
    agent_id: str
    status: str  # pending, running, completed, failed
    message: str
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error: Optional[str]


@dataclass
class WorkflowDefinition:
    """Workflow definition data structure."""

    workflow_type: str
    description: str
    required_agents: List[str]
    task_sequence: List[str]
    estimated_duration: int
    priority: str  # low, medium, high, critical


class WorkflowService:
    """
    Workflow Service - Single responsibility: Workflow coordination and task management.

    This service manages:
    - Workflow definition and execution
    - Task assignment and tracking
    - Agent workflow coordination
    - Workflow status monitoring
    """

    def __init__(self, workflows_dir: str = "agent_workspaces/workflows"):
        """Initialize Workflow Service."""
        self.workflows_dir = Path(workflows_dir)
        self.workflows_dir.mkdir(exist_ok=True)
        self.logger = self._setup_logging()
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.active_tasks: Dict[str, WorkflowTask] = {}
        self.task_counter = 0

        # Initialize default workflows
        self._initialize_default_workflows()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("WorkflowService")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_default_workflows(self):
        """Initialize default workflow definitions."""
        default_workflows = {
            "strategic_coordination": WorkflowDefinition(
                workflow_type="strategic_coordination",
                description="Strategic coordination and planning workflow",
                required_agents=["Agent-1"],
                task_sequence=["planning", "coordination", "reporting"],
                estimated_duration=1800,
                priority="high",
            ),
            "task_management": WorkflowDefinition(
                workflow_type="task_management",
                description="Task breakdown and resource allocation workflow",
                required_agents=["Agent-2"],
                task_sequence=["analysis", "breakdown", "allocation"],
                estimated_duration=1200,
                priority="medium",
            ),
            "technical_implementation": WorkflowDefinition(
                workflow_type="technical_implementation",
                description="Technical implementation and development workflow",
                required_agents=["Agent-3"],
                task_sequence=["development", "testing", "deployment"],
                estimated_duration=3600,
                priority="high",
            ),
            "security_protocols": WorkflowDefinition(
                workflow_type="security_protocols",
                description="Security protocols and communication standards workflow",
                required_agents=["Agent-4"],
                task_sequence=["assessment", "implementation", "validation"],
                estimated_duration=2400,
                priority="critical",
            ),
        }

        self.workflows.update(default_workflows)
        self.logger.info(f"Initialized {len(default_workflows)} default workflows")

    def create_workflow_task(
        self, workflow_type: str, agent_id: str, message: str
    ) -> Optional[str]:
        """Create a new workflow task."""
        try:
            if workflow_type not in self.workflows:
                self.logger.error(f"Unknown workflow type: {workflow_type}")
                return None

            workflow = self.workflows[workflow_type]

            if agent_id not in workflow.required_agents:
                self.logger.error(
                    f"Agent {agent_id} not required for workflow {workflow_type}"
                )
                return None

            # Generate task ID
            self.task_counter += 1
            task_id = f"task_{workflow_type}_{agent_id}_{self.task_counter}"

            # Create task
            task = WorkflowTask(
                task_id=task_id,
                workflow_type=workflow_type,
                agent_id=agent_id,
                status="pending",
                message=message,
                created_at=datetime.now(),
                started_at=None,
                completed_at=None,
                error=None,
            )

            self.active_tasks[task_id] = task
            self.logger.info(f"Created workflow task {task_id} for {agent_id}")
            return task_id

        except Exception as e:
            self.logger.error(f"Error creating workflow task: {e}")
            return None

    def start_workflow_task(self, task_id: str) -> bool:
        """Start a workflow task."""
        try:
            if task_id not in self.active_tasks:
                self.logger.error(f"Task {task_id} not found")
                return False

            task = self.active_tasks[task_id]
            if task.status != "pending":
                self.logger.error(
                    f"Task {task_id} is not pending (current: {task.status})"
                )
                return False

            task.status = "running"
            task.started_at = datetime.now()

            self.logger.info(f"Started workflow task {task_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error starting workflow task {task_id}: {e}")
            return False

    def complete_workflow_task(self, task_id: str, error: Optional[str] = None) -> bool:
        """Complete a workflow task."""
        try:
            if task_id not in self.active_tasks:
                self.logger.error(f"Task {task_id} not found")
                return False

            task = self.active_tasks[task_id]
            if task.status != "running":
                self.logger.error(
                    f"Task {task_id} is not running (current: {task.status})"
                )
                return False

            task.status = "completed" if not error else "failed"
            task.completed_at = datetime.now()
            task.error = error

            self.logger.info(
                f"Completed workflow task {task_id} with status: {task.status}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Error completing workflow task {task_id}: {e}")
            return False

    def get_workflow_status(self, workflow_type: str) -> Dict[str, Any]:
        """Get status for a specific workflow type."""
        workflow = self.workflows.get(workflow_type)
        if not workflow:
            return {}

        # Get tasks for this workflow
        workflow_tasks = [
            task
            for task in self.active_tasks.values()
            if task.workflow_type == workflow_type
        ]

        status_counts = {
            "pending": len([t for t in workflow_tasks if t.status == "pending"]),
            "running": len([t for t in workflow_tasks if t.status == "running"]),
            "completed": len([t for t in workflow_tasks if t.status == "completed"]),
            "failed": len([t for t in workflow_tasks if t.status == "failed"]),
        }

        return {
            "workflow_type": workflow_type,
            "description": workflow.description,
            "required_agents": workflow.required_agents,
            "priority": workflow.priority,
            "estimated_duration": workflow.estimated_duration,
            "total_tasks": len(workflow_tasks),
            "task_status": status_counts,
        }

    def get_agent_workflows(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get workflows assigned to a specific agent."""
        agent_tasks = [
            task for task in self.active_tasks.values() if task.agent_id == agent_id
        ]

        workflows = []
        for task in agent_tasks:
            workflow = self.workflows.get(task.workflow_type)
            if workflow:
                workflows.append(
                    {
                        "task_id": task.task_id,
                        "workflow_type": task.workflow_type,
                        "status": task.status,
                        "message": task.message,
                        "created_at": task.created_at.isoformat(),
                        "started_at": task.started_at.isoformat()
                        if task.started_at
                        else None,
                        "completed_at": task.completed_at.isoformat()
                        if task.completed_at
                        else None,
                        "error": task.error,
                        "workflow_description": workflow.description,
                        "priority": workflow.priority,
                    }
                )

        return workflows

    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get overall workflow system summary."""
        total_tasks = len(self.active_tasks)
        completed_tasks = len(
            [t for t in self.active_tasks.values() if t.status == "completed"]
        )
        failed_tasks = len(
            [t for t in self.active_tasks.values() if t.status == "failed"]
        )
        active_tasks = len(
            [
                t
                for t in self.active_tasks.values()
                if t.status in ["pending", "running"]
            ]
        )

        return {
            "total_workflows": len(self.workflows),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "active_tasks": active_tasks,
            "success_rate": (completed_tasks / total_tasks * 100)
            if total_tasks > 0
            else 0,
        }


def main():
    """CLI interface for Workflow Service."""
    parser = argparse.ArgumentParser(description="Workflow Service CLI")
    parser.add_argument(
        "--create",
        type=str,
        help="Create workflow task (format: workflow_type:agent_id:message)",
    )
    parser.add_argument("--start", type=str, help="Start workflow task by ID")
    parser.add_argument("--complete", type=str, help="Complete workflow task by ID")
    parser.add_argument(
        "--error",
        type=str,
        help="Complete workflow task with error (format: task_id:error_message)",
    )
    parser.add_argument(
        "--status", type=str, help="Show workflow status for specific type"
    )
    parser.add_argument("--agent", type=str, help="Show workflows for specific agent")
    parser.add_argument(
        "--summary", action="store_true", help="Show workflow system summary"
    )

    args = parser.parse_args()

    # Initialize service
    workflow_service = WorkflowService()

    if args.create:
        try:
            workflow_type, agent_id, message = args.create.split(":", 2)
            task_id = workflow_service.create_workflow_task(
                workflow_type, agent_id, message
            )
            if task_id:
                print(f"✅ Created workflow task: {task_id}")
            else:
                print("❌ Failed to create workflow task")
        except ValueError:
            print("❌ Invalid format. Use: workflow_type:agent_id:message")

    elif args.start:
        success = workflow_service.start_workflow_task(args.start)
        print(f"Task start: {'✅ Success' if success else '❌ Failed'}")

    elif args.complete:
        success = workflow_service.complete_workflow_task(args.complete)
        print(f"Task completion: {'✅ Success' if success else '❌ Failed'}")

    elif args.error:
        try:
            task_id, error_message = args.error.split(":", 1)
            success = workflow_service.complete_workflow_task(task_id, error_message)
            print(
                f"Task completion with error: {'✅ Success' if success else '❌ Failed'}"
            )
        except ValueError:
            print("❌ Invalid format. Use: task_id:error_message")

    elif args.status:
        status = workflow_service.get_workflow_status(args.status)
        if status:
            print(f"📊 Workflow Status for {args.status}:")
            for key, value in status.items():
                print(f"  {key}: {value}")
        else:
            print(f"❌ Workflow type {args.status} not found")

    elif args.agent:
        workflows = workflow_service.get_agent_workflows(args.agent)
        if workflows:
            print(f"🤖 Workflows for {args.agent}:")
            for workflow in workflows:
                print(
                    f"  Task: {workflow['task_id']} - {workflow['workflow_type']} ({workflow['status']})"
                )
        else:
            print(f"❌ No workflows found for {args.agent}")

    elif args.summary:
        summary = workflow_service.get_workflow_summary()
        print("📊 Workflow System Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")

    else:
        print("🔄 Workflow Service - Use --help for available commands")


if __name__ == "__main__":
    main()
