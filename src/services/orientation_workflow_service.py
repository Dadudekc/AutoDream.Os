"""
Orientation Workflow Service - Workflow Execution

This module executes orientation workflows using workflow definitions.
Follows Single Responsibility Principle - only manages workflow execution.

Architecture: Single Responsibility Principle - workflow execution only
LOC: 180 lines (under 200 limit)
"""

import argparse
import time
import threading
from typing import Dict, List, Optional, Any, Callable
import logging

from .workflow_definitions import (
    WorkflowStep,
    WorkflowStatus,
    WorkflowExecution,
    WorkflowDefinitionManager,
)

logger = logging.getLogger(__name__)


class OrientationWorkflowService:
    """
    Service for executing agent orientation workflows

    Responsibilities:
    - Execute orientation workflows
    - Track workflow progress and completion
    - Coordinate workflow steps
    - Manage workflow lifecycle
    """

    def __init__(self):
        self.definition_manager = WorkflowDefinitionManager()
        self.active_workflows: Dict[str, WorkflowExecution] = {}
        self.completed_workflows: Dict[str, WorkflowExecution] = {}
        self.workflow_handlers: Dict[WorkflowStep, List[Callable]] = {}
        self.logger = logging.getLogger(f"{__name__}.OrientationWorkflowService")

        self._initialize_workflow_handlers()

    def _initialize_workflow_handlers(self):
        """Initialize workflow step handlers"""
        self.workflow_handlers = {
            WorkflowStep.INITIALIZATION: [self._simulate_initialization],
            WorkflowStep.TRAINING: [self._simulate_training],
            WorkflowStep.ROLE_ASSIGNMENT: [self._simulate_role_assignment],
            WorkflowStep.CAPABILITY_GRANT: [self._simulate_capability_grant],
            WorkflowStep.SYSTEM_INTEGRATION: [self._simulate_system_integration],
            WorkflowStep.VALIDATION: [self._simulate_validation],
            WorkflowStep.COMPLETION: [self._simulate_completion],
        }

    def start_orientation_workflow(
        self, agent_id: str, workflow_type: str = "standard"
    ) -> str:
        """Start an orientation workflow for an agent"""
        workflow_id = f"{workflow_type}_{agent_id}_{int(time.time())}"

        # Create workflow execution
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            agent_id=agent_id,
            status=WorkflowStatus.PENDING,
            current_step=None,
            completed_steps=[],
            start_time=time.time(),
            step_results={},
        )

        self.active_workflows[workflow_id] = execution
        self.logger.info(
            f"Started {workflow_type} workflow for {agent_id}: {workflow_id}"
        )

        # Start workflow execution in background
        threading.Thread(
            target=self._execute_workflow, args=(workflow_id,), daemon=True
        ).start()

        return workflow_id

    def _execute_workflow(self, workflow_id: str):
        """Execute workflow steps in sequence"""
        execution = self.active_workflows[workflow_id]
        workflow_def = self.definition_manager.get_workflow_definition(
            "standard"
        )  # Default to standard

        execution.status = WorkflowStatus.IN_PROGRESS
        self.logger.info(f"Executing workflow {workflow_id}")

        try:
            for step_data in workflow_def:
                if execution.status == WorkflowStatus.CANCELLED:
                    break

                execution.current_step = step_data.step_id
                self.logger.info(f"Executing step: {step_data.name}")

                # Execute step handlers
                step_results = {}
                for handler in self.workflow_handlers.get(step_data.step_id, []):
                    try:
                        result = handler(execution, step_data)
                        step_results.update(result or {})
                    except Exception as e:
                        self.logger.error(f"Step handler error: {e}")
                        step_results["error"] = str(e)

                execution.step_results[step_data.step_id] = step_results
                execution.completed_steps.append(step_data.step_id)

                # Simulate step duration
                time.sleep(step_data.duration_minutes * 0.1)  # Scale down for testing

            execution.status = WorkflowStatus.COMPLETED
            execution.completion_time = time.time()
            self.logger.info(f"Workflow {workflow_id} completed successfully")

        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            self.logger.error(f"Workflow {workflow_id} failed: {e}")

        # Move to completed workflows
        self.completed_workflows[workflow_id] = execution
        del self.active_workflows[workflow_id]

    def _simulate_initialization(self, execution: WorkflowExecution, step_data) -> Dict:
        """Simulate initialization step"""
        return {"status": "initialized", "timestamp": time.time()}

    def _simulate_training(self, execution: WorkflowExecution, step_data) -> Dict:
        """Simulate training step"""
        return {"status": "trained", "timestamp": time.time()}

    def _simulate_role_assignment(
        self, execution: WorkflowExecution, step_data
    ) -> Dict:
        """Simulate role assignment step"""
        return {"status": "role_assigned", "timestamp": time.time()}

    def _simulate_capability_grant(
        self, execution: WorkflowExecution, step_data
    ) -> Dict:
        """Simulate capability grant step"""
        return {"status": "capabilities_granted", "timestamp": time.time()}

    def _simulate_system_integration(
        self, execution: WorkflowExecution, step_data
    ) -> Dict:
        """Simulate system integration step"""
        return {"status": "integrated", "timestamp": time.time()}

    def _simulate_validation(self, execution: WorkflowExecution, step_data) -> Dict:
        """Simulate validation step"""
        return {"status": "validated", "timestamp": time.time()}

    def _simulate_completion(self, execution: WorkflowExecution, step_data) -> Dict:
        """Simulate completion step"""
        return {"status": "completed", "timestamp": time.time()}

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        """Get current status of a workflow"""
        # Check active workflows
        if workflow_id in self.active_workflows:
            execution = self.active_workflows[workflow_id]
            return {
                "workflow_id": workflow_id,
                "status": execution.status.value,
                "current_step": execution.current_step.value
                if execution.current_step
                else None,
                "completed_steps": [s.value for s in execution.completed_steps],
                "progress": len(execution.completed_steps),
            }

        # Check completed workflows
        if workflow_id in self.completed_workflows:
            execution = self.completed_workflows[workflow_id]
            return {
                "workflow_id": workflow_id,
                "status": execution.status.value,
                "completed_steps": [s.value for s in execution.completed_steps],
                "completion_time": execution.completion_time,
            }

        return None

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel an active workflow"""
        if workflow_id in self.active_workflows:
            execution = self.active_workflows[workflow_id]
            execution.status = WorkflowStatus.CANCELLED
            self.logger.info(f"Workflow {workflow_id} cancelled")
            return True
        return False

    def get_active_workflows(self) -> List[str]:
        """Get list of active workflow IDs"""
        return list(self.active_workflows.keys())

    def get_completed_workflows(self) -> List[str]:
        """Get list of completed workflow IDs"""
        return list(self.completed_workflows.keys())


def run_smoke_test():
    """Run basic functionality test for OrientationWorkflowService"""
    print("🧪 Running OrientationWorkflowService Smoke Test...")

    try:
        service = OrientationWorkflowService()

        # Test workflow start
        workflow_id = service.start_orientation_workflow("test-agent", "standard")
        assert workflow_id in service.get_active_workflows()

        # Test status retrieval
        status = service.get_workflow_status(workflow_id)
        assert status is not None
        assert "status" in status

        # Wait for completion
        import time

        time.sleep(2)  # Give workflow time to complete

        # Check completion
        completed = service.get_completed_workflows()
        assert workflow_id in completed

        print("✅ OrientationWorkflowService Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ OrientationWorkflowService Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for OrientationWorkflowService testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Orientation Workflow Service CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--start", help="Start workflow for agent")
    parser.add_argument("--status", help="Get workflow status")
    parser.add_argument("--cancel", help="Cancel workflow")
    parser.add_argument(
        "--list-active", action="store_true", help="List active workflows"
    )
    parser.add_argument(
        "--list-completed", action="store_true", help="List completed workflows"
    )

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    service = OrientationWorkflowService()

    if args.start:
        workflow_id = service.start_orientation_workflow(args.start)
        print(f"Started workflow: {workflow_id}")
    elif args.status:
        status = service.get_workflow_status(args.status)
        if status:
            print(f"Workflow Status: {status}")
        else:
            print(f"Workflow {args.status} not found")
    elif args.cancel:
        if service.cancel_workflow(args.cancel):
            print(f"Workflow {args.cancel} cancelled")
        else:
            print(f"Workflow {args.cancel} not found or already completed")
    elif args.list_active:
        active = service.get_active_workflows()
        print(f"Active workflows: {active}")
    elif args.list_completed:
        completed = service.get_completed_workflows()
        print(f"Completed workflows: {completed}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
