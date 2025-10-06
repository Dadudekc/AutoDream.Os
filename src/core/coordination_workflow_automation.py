"""
Coordination Workflow Automation - V2 Compliant
===============================================

Automated coordination workflow management for V2_SWARM agents.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .system_integration_coordinator import SystemIntegrationCoordinator


class WorkflowStatus(Enum):
    """Workflow status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(Enum):
    """Task type enumeration."""

    INTEGRATION_CHECK = "integration_check"
    SERVICE_RESTART = "service_restart"
    DEPENDENCY_FIX = "dependency_fix"
    COORDINATION_SYNC = "coordination_sync"
    HEALTH_MONITOR = "health_monitor"


@dataclass
class WorkflowTask:
    """Workflow task data structure."""

    task_id: str
    task_type: TaskType
    description: str
    command: str
    dependencies: list[str]
    timeout: int = 30
    retry_count: int = 0
    max_retries: int = 3
    status: WorkflowStatus = WorkflowStatus.PENDING


@dataclass
class WorkflowExecution:
    """Workflow execution data structure."""

    workflow_id: str
    tasks: list[WorkflowTask]
    status: WorkflowStatus
    start_time: datetime
    end_time: datetime | None = None
    results: dict[str, str] = None


class CoordinationWorkflowAutomation:
    """Automated coordination workflow management."""

    def __init__(self):
        """Initialize workflow automation."""
        self.integration_coordinator = SystemIntegrationCoordinator()
        self.active_workflows: dict[str, WorkflowExecution] = {}
        self.workflow_templates = self._load_workflow_templates()

    def _load_workflow_templates(self) -> dict[str, list[WorkflowTask]]:
        """Load predefined workflow templates."""
        return {
            "system_health_check": [
                WorkflowTask(
                    task_id="check_messaging",
                    task_type=TaskType.INTEGRATION_CHECK,
                    description="Check messaging service health",
                    command="python -m src.services.consolidated_messaging_service status",
                    dependencies=[],
                ),
                WorkflowTask(
                    task_id="check_thea",
                    task_type=TaskType.INTEGRATION_CHECK,
                    description="Check THEA service health",
                    command="python -c 'from src.services.thea.thea_communication_core import TheaCommunicationCore'",
                    dependencies=["check_messaging"],
                ),
                WorkflowTask(
                    task_id="check_coordination",
                    task_type=TaskType.INTEGRATION_CHECK,
                    description="Check swarm coordination",
                    command="python tools/swarm_coordination_tool.py status",
                    dependencies=["check_messaging"],
                ),
            ],
            "service_recovery": [
                WorkflowTask(
                    task_id="fix_thea_deps",
                    task_type=TaskType.DEPENDENCY_FIX,
                    description="Fix THEA dependencies",
                    command="python src/core/system_integration_coordinator.py --fix-deps thea",
                    dependencies=[],
                ),
                WorkflowTask(
                    task_id="restart_messaging",
                    task_type=TaskType.SERVICE_RESTART,
                    description="Restart messaging service",
                    command="python -m src.services.consolidated_messaging_service status",
                    dependencies=["fix_thea_deps"],
                ),
            ],
        }

    def create_workflow(self, workflow_name: str, template_name: str | None = None) -> str:
        """Create a new workflow."""
        workflow_id = f"{workflow_name}_{int(time.time())}"

        if template_name and template_name in self.workflow_templates:
            tasks = self.workflow_templates[template_name].copy()
        else:
            tasks = []

        execution = WorkflowExecution(
            workflow_id=workflow_id,
            tasks=tasks,
            status=WorkflowStatus.PENDING,
            start_time=datetime.now(),
        )

        self.active_workflows[workflow_id] = execution
        return workflow_id

    def execute_workflow(self, workflow_id: str) -> bool:
        """Execute a workflow."""
        if workflow_id not in self.active_workflows:
            return False

        execution = self.active_workflows[workflow_id]
        execution.status = WorkflowStatus.RUNNING
        execution.results = {}

        try:
            for task in execution.tasks:
                if not self._execute_task(task, execution):
                    execution.status = WorkflowStatus.FAILED
                    return False

            execution.status = WorkflowStatus.COMPLETED
            execution.end_time = datetime.now()
            return True

        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.results["error"] = str(e)
            return False

    def _execute_task(self, task: WorkflowTask, execution: WorkflowExecution) -> bool:
        """Execute a single workflow task."""
        # Check dependencies
        for dep_id in task.dependencies:
            if dep_id not in execution.results or execution.results[dep_id] != "success":
                return False

        # Execute task
        try:
            import subprocess

            result = subprocess.run(
                task.command.split(), capture_output=True, text=True, timeout=task.timeout
            )

            if result.returncode == 0:
                execution.results[task.task_id] = "success"
                return True
            else:
                execution.results[task.task_id] = f"failed: {result.stderr}"
                return False

        except subprocess.TimeoutExpired:
            execution.results[task.task_id] = "timeout"
            return False
        except Exception as e:
            execution.results[task.task_id] = f"error: {str(e)}"
            return False

    def get_workflow_status(self, workflow_id: str) -> WorkflowExecution | None:
        """Get workflow execution status."""
        return self.active_workflows.get(workflow_id)

    def list_active_workflows(self) -> dict[str, WorkflowStatus]:
        """List all active workflows."""
        return {
            workflow_id: execution.status
            for workflow_id, execution in self.active_workflows.items()
        }

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a workflow."""
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id].status = WorkflowStatus.CANCELLED
            return True
        return False

    def generate_coordination_report(self) -> dict:
        """Generate coordination workflow report."""
        total_workflows = len(self.active_workflows)
        completed = sum(
            1 for w in self.active_workflows.values() if w.status == WorkflowStatus.COMPLETED
        )
        failed = sum(1 for w in self.active_workflows.values() if w.status == WorkflowStatus.FAILED)
        running = sum(
            1 for w in self.active_workflows.values() if w.status == WorkflowStatus.RUNNING
        )

        return {
            "total_workflows": total_workflows,
            "completed": completed,
            "failed": failed,
            "running": running,
            "success_rate": (completed / total_workflows * 100) if total_workflows > 0 else 0,
            "workflows": {
                workflow_id: {
                    "status": execution.status.value,
                    "start_time": execution.start_time.isoformat(),
                    "end_time": execution.end_time.isoformat() if execution.end_time else None,
                    "task_count": len(execution.tasks),
                }
                for workflow_id, execution in self.active_workflows.items()
            },
        }


def main():
    """CLI entry point for coordination workflow automation."""
    import argparse

    parser = argparse.ArgumentParser(description="Coordination Workflow Automation")
    parser.add_argument("--create", help="Create workflow from template")
    parser.add_argument("--execute", help="Execute workflow by ID")
    parser.add_argument("--status", help="Get workflow status")
    parser.add_argument("--list", action="store_true", help="List active workflows")
    parser.add_argument("--report", action="store_true", help="Generate coordination report")

    args = parser.parse_args()

    automation = CoordinationWorkflowAutomation()

    if args.create:
        workflow_id = automation.create_workflow(args.create, "system_health_check")
        print(f"Created workflow: {workflow_id}")

    elif args.execute:
        success = automation.execute_workflow(args.execute)
        print(f"Workflow execution: {'Success' if success else 'Failed'}")

    elif args.status:
        execution = automation.get_workflow_status(args.status)
        if execution:
            print(f"Status: {execution.status.value}")
            print(f"Tasks: {len(execution.tasks)}")
        else:
            print("Workflow not found")

    elif args.list:
        workflows = automation.list_active_workflows()
        for workflow_id, status in workflows.items():
            print(f"{workflow_id}: {status.value}")

    elif args.report:
        report = automation.generate_coordination_report()
        print("Coordination Report:")
        print(f"  Total Workflows: {report['total_workflows']}")
        print(f"  Success Rate: {report['success_rate']:.1f}%")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

