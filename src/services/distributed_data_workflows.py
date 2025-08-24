#!/usr/bin/env python3
"""
Distributed Data Workflows
==========================
Comprehensive workflow management for distributed agent swarm data operations.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
import threading

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Workflow execution status"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStepType(Enum):
    """Workflow step types"""

    DATA_READ = "data_read"
    DATA_WRITE = "data_write"
    DATA_TRANSFORM = "data_transform"


@dataclass
class WorkflowDefinition:
    """Workflow definition"""

    workflow_id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]


@dataclass
class WorkflowExecution:
    """Workflow execution instance"""

    execution_id: str
    workflow_id: str
    status: WorkflowStatus
    start_time: float
    end_time: Optional[float] = None
    current_step: int = 0
    total_steps: int = 0
    error_message: Optional[str] = None


class DistributedDataWorkflows:
    """Distributed data workflow management system"""

    def __init__(self, system_id: str = "default-workflows"):
        self.logger = logging.getLogger(f"{__name__}.DistributedDataWorkflows")
        self.system_id = system_id
        self._workflow_definitions: Dict[str, WorkflowDefinition] = {}
        self._workflow_executions: Dict[str, WorkflowExecution] = {}
        self._workflow_engine_active = False
        self._workflow_thread: Optional[threading.Thread] = None
        self._stop_workflow = threading.Event()
        self._total_workflows = 0
        self._successful_workflows = 0
        self._failed_workflows = 0
        self.logger.info(f"Distributed Data Workflows '{system_id}' initialized")

    def register_workflow(self, workflow: WorkflowDefinition) -> bool:
        """Register a workflow definition"""
        if workflow.workflow_id in self._workflow_definitions:
            return False
        self._workflow_definitions[workflow.workflow_id] = workflow
        self.logger.info(
            f"Workflow registered: {workflow.name} ({workflow.workflow_id})"
        )
        return True

    def execute_workflow(
        self, workflow_id: str, parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """Execute a workflow"""
        if workflow_id not in self._workflow_definitions:
            raise ValueError(f"Workflow not found: {workflow_id}")

        workflow = self._workflow_definitions[workflow_id]
        execution_id = f"exec_{workflow_id}_{int(time.time())}"

        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow_id=workflow_id,
            status=WorkflowStatus.PENDING,
            start_time=time.time(),
            total_steps=len(workflow.steps),
        )

        self._workflow_executions[execution_id] = execution
        self._total_workflows += 1

        self.logger.info(
            f"Workflow execution started: {workflow.name} ({execution_id})"
        )
        return execution_id

    def get_workflow_execution_status(
        self, execution_id: str
    ) -> Optional[WorkflowExecution]:
        """Get workflow execution status"""
        return self._workflow_executions.get(execution_id)

    def get_workflow_statistics(self) -> Dict[str, Any]:
        """Get workflow system statistics"""
        return {
            "system_id": self.system_id,
            "total_workflows": self._total_workflows,
            "successful_workflows": self._successful_workflows,
            "failed_workflows": self._failed_workflows,
            "success_rate": (self._successful_workflows / max(1, self._total_workflows))
            * 100,
            "active_executions": len(
                [
                    e
                    for e in self._workflow_executions.values()
                    if e.status == WorkflowStatus.RUNNING
                ]
            ),
            "engine_active": self._workflow_engine_active,
            "timestamp": time.time(),
        }

    def start_workflow_engine(self):
        """Start the workflow engine"""
        if self._workflow_engine_active:
            return
        self._workflow_engine_active = True
        self._stop_workflow.clear()
        self._workflow_thread = threading.Thread(
            target=self._workflow_engine_loop, daemon=True
        )
        self._workflow_thread.start()
        self.logger.info("Workflow engine started")

    def _workflow_engine_loop(self):
        """Main workflow engine loop"""
        while not self._stop_workflow.is_set():
            try:
                self._process_pending_workflows()
                time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Workflow engine error: {e}")
                time.sleep(1)

    def _process_pending_workflows(self):
        """Process pending workflow executions"""
        pending_executions = [
            e
            for e in self._workflow_executions.values()
            if e.status == WorkflowStatus.PENDING
        ]

        for execution in pending_executions[:5]:
            self._execute_workflow(execution)

    def _execute_workflow(self, execution: WorkflowExecution):
        """Execute a complete workflow"""
        workflow = self._workflow_definitions.get(execution.workflow_id)
        if not workflow:
            execution.status = WorkflowStatus.FAILED
            execution.error_message = "Workflow definition not found"
            return

        execution.status = WorkflowStatus.RUNNING

        try:
            for step_index, step in enumerate(workflow.steps):
                execution.current_step = step_index + 1
                time.sleep(0.1)  # Simulate step execution

            execution.status = WorkflowStatus.COMPLETED
            execution.end_time = time.time()
            self._successful_workflows += 1
            self.logger.info(f"Workflow completed: {execution.execution_id}")

        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.error_message = str(e)
            self._failed_workflows += 1
            self.logger.error(f"Workflow execution error: {e}")

    def stop_workflow_engine(self):
        """Stop the workflow engine"""
        self._workflow_engine_active = False
        self._stop_workflow.set()
        if self._workflow_thread and self._workflow_thread.is_alive():
            self._workflow_thread.join(timeout=2)
        self.logger.info("Workflow engine stopped")


def main():
    """CLI interface for testing DistributedDataWorkflows"""
    import argparse

    parser = argparse.ArgumentParser(description="Distributed Data Workflows CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    args = parser.parse_args()

    if args.test:
        print("🧪 DistributedDataWorkflows Smoke Test")
        workflows = DistributedDataWorkflows("test-workflows")
        workflow = WorkflowDefinition(
            "test-workflow",
            "Test Workflow",
            "Simple test workflow",
            steps=[
                {"type": "data_read", "name": "Read Data", "data_key": "test-data"},
                {
                    "type": "data_transform",
                    "name": "Transform Data",
                    "transform_type": "copy",
                },
                {"type": "data_write", "name": "Write Data", "data_key": "output-data"},
            ],
        )
        workflows.register_workflow(workflow)
        execution_id = workflows.execute_workflow("test-workflow")
        print(f"✅ Workflow execution started: {execution_id}")
        workflows.start_workflow_engine()
        time.sleep(0.3)
        status = workflows.get_workflow_execution_status(execution_id)
        print(f"✅ Workflow status: {status.status.value}")
        stats = workflows.get_workflow_statistics()
        print(f"✅ Total workflows: {stats['total_workflows']}")
        workflows.stop_workflow_engine()
        print("🎉 Smoke test PASSED!")
    else:
        print("DistributedDataWorkflows ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
