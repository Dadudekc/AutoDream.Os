#!/usr/bin/env python3
"""
Workflow Connector - Learning System Integration

This module connects the existing unified learning system with the existing
workflow engine, providing learning-specific workflow capabilities without
duplicating existing workflow functionality.

Author: Agent-1 (Core Engine Development - Task 1B)
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import uuid

from .unified_learning_engine import UnifiedLearningEngine
from .models import LearningSession, LearningGoal, LearningStatus, LearningEngineConfig
from . import models as learning_models
from .decision_models import (
    DecisionRequest,
    DecisionResult,
    DecisionType,
    DecisionPriority,
)
from ..workflow.core.workflow_engine import WorkflowEngine, EngineConfig
from ..workflow.types.workflow_enums import WorkflowStatus, TaskStatus, WorkflowType
from ..workflow.types.workflow_models import (
    WorkflowDefinition,
    WorkflowExecution,
    WorkflowStep,
)


class LearningWorkflowConnector:
    """Connects unified learning system with existing workflow engine"""

    def __init__(
        self, learning_engine: UnifiedLearningEngine, workflow_engine: WorkflowEngine
    ):
        self.logger = logging.getLogger(f"{__name__}.LearningWorkflowConnector")
        self.learning_engine = learning_engine
        self.workflow_engine = workflow_engine

        # Learning workflow state
        self.learning_workflow_sessions: Dict[str, Dict[str, Any]] = {}

        # Integration metrics
        self.integration_metrics = {
            "total_learning_workflows": 0,
            "active_learning_workflows": 0,
            "completed_learning_workflows": 0,
            "failed_learning_workflows": 0,
        }

        # Learning workflow hooks
        self.learning_hooks: Dict[str, List[Callable]] = {
            "learning_workflow_started": [],
            "learning_workflow_step_completed": [],
            "learning_workflow_completed": [],
            "learning_workflow_failed": [],
        }

        self._setup_learning_hooks()
        self.logger.info("LearningWorkflowConnector initialized")

    def _setup_learning_hooks(self) -> None:
        """Setup default learning workflow hooks"""
        self.add_learning_hook(
            "learning_workflow_started", self._on_learning_workflow_started
        )
        self.add_learning_hook(
            "learning_workflow_step_completed",
            self._on_learning_workflow_step_completed,
        )
        self.add_learning_hook(
            "learning_workflow_completed", self._on_learning_workflow_completed
        )
        self.add_learning_hook(
            "learning_workflow_failed", self._on_learning_workflow_failed
        )

    def add_learning_hook(self, event: str, hook: Callable) -> None:
        """Add learning workflow hook"""
        if event in self.learning_hooks:
            self.learning_hooks[event].append(hook)
            self.logger.info(f"Added learning hook for event: {event}")

    def remove_learning_hook(self, event: str, hook: Callable) -> None:
        """Remove learning workflow hook"""
        if event in self.learning_hooks and hook in self.learning_hooks[event]:
            self.learning_hooks[event].remove(hook)
            self.logger.info(f"Removed learning hook for event: {event}")

    def _trigger_learning_hooks(self, event: str, data: Dict[str, Any]) -> None:
        """Trigger learning workflow hooks"""
        if event in self.learning_hooks:
            for hook in self.learning_hooks[event]:
                try:
                    hook(data)
                except Exception as e:
                    self.logger.error(f"Learning hook error for event {event}: {e}")

    def create_learning_workflow(
        self,
        workflow_name: str,
        agent_id: str,
        learning_parameters: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Create a learning workflow using existing workflow engine"""
        try:
            # Create learning session using existing unified learning engine
            session_config = {
                "agent_id": agent_id,
                "session_type": "workflow_integrated",
                "workflow_name": workflow_name,
                "learning_parameters": learning_parameters or {},
                "created_at": datetime.now().isoformat(),
            }

            # Use existing learning engine to create session
            session_id = learning_models.create_learning_session(
                self.learning_engine,
                agent_id=agent_id,
                session_type="workflow_integrated",
                initial_data=session_config,
            )

            if not session_id:
                self.logger.error(
                    "Failed to create learning session using existing engine"
                )
                return None

            # Create workflow definition using existing workflow engine
            workflow_definition = self._create_learning_workflow_definition(
                workflow_name, agent_id, learning_parameters
            )

            # Register workflow definition with existing workflow engine
            self.workflow_engine.workflow_definitions[
                workflow_definition.workflow_id
            ] = workflow_definition

            # Create workflow execution using existing workflow engine
            execution = self.workflow_engine.create_workflow_execution(
                workflow_definition.workflow_id
            )

            if not execution:
                self.logger.error(
                    "Failed to create workflow execution using existing engine"
                )
                return None

            # Track learning workflow integration
            learning_workflow_id = str(uuid.uuid4())
            self.learning_workflow_sessions[learning_workflow_id] = {
                "workflow_name": workflow_name,
                "learning_session_id": session_id,
                "workflow_execution_id": execution.execution_id,
                "agent_id": agent_id,
                "learning_parameters": learning_parameters or {},
                "start_time": datetime.now(),
                "status": "created",
            }

            # Update metrics
            self.integration_metrics["total_learning_workflows"] += 1
            self.integration_metrics["active_learning_workflows"] += 1

            self.logger.info(
                f"Created learning workflow: {learning_workflow_id} using existing engines"
            )
            return learning_workflow_id

        except Exception as e:
            self.logger.error(f"Failed to create learning workflow: {e}")
            return None

    def _create_learning_workflow_definition(
        self,
        workflow_name: str,
        agent_id: str,
        learning_parameters: Optional[Dict[str, Any]] = None,
    ) -> WorkflowDefinition:
        """Create workflow definition for learning workflow"""

        # Create learning-specific workflow steps
        steps = [
            WorkflowStep(
                step_id="learning_initiation",
                name="Learning Initiation",
                step_type="learning",
                description="Initialize learning session using existing learning engine",
                dependencies=[],
                estimated_duration=30.0,
                metadata={
                    "learning_operation": "session_initiation",
                    "integration_type": "existing_learning_engine",
                },
            ),
            WorkflowStep(
                step_id="learning_execution",
                name="Learning Execution",
                step_type="learning",
                description="Execute learning using existing unified learning engine",
                dependencies=["learning_initiation"],
                estimated_duration=300.0,
                metadata={
                    "learning_operation": "learning_execution",
                    "integration_type": "existing_learning_engine",
                },
            ),
            WorkflowStep(
                step_id="learning_evaluation",
                name="Learning Evaluation",
                step_type="learning",
                description="Evaluate learning progress using existing metrics system",
                dependencies=["learning_execution"],
                estimated_duration=60.0,
                metadata={
                    "learning_operation": "progress_evaluation",
                    "integration_type": "existing_metrics_system",
                },
            ),
        ]

        # Create workflow definition
        workflow_definition = WorkflowDefinition(
            workflow_id=f"learning_workflow_{workflow_name}_{agent_id}",
            workflow_type=WorkflowType.LEARNING,
            name=f"Learning Workflow: {workflow_name}",
            description=f"Learning workflow for agent {agent_id} using existing unified systems",
            steps=steps,
        )

        return workflow_definition

    def execute_learning_workflow(self, learning_workflow_id: str) -> bool:
        """Execute learning workflow using existing workflow engine"""
        if learning_workflow_id not in self.learning_workflow_sessions:
            self.logger.error(f"Learning workflow not found: {learning_workflow_id}")
            return False

        try:
            learning_session = self.learning_workflow_sessions[learning_workflow_id]
            workflow_execution_id = learning_session["workflow_execution_id"]

            # Use existing workflow engine to start workflow
            if not self.workflow_engine.start_workflow(workflow_execution_id):
                return False

            # Update status
            learning_session["status"] = "running"

            # Trigger learning workflow started hook
            self._trigger_learning_hooks(
                "learning_workflow_started",
                {
                    "learning_workflow_id": learning_workflow_id,
                    "workflow_execution_id": workflow_execution_id,
                    "agent_id": learning_session["agent_id"],
                },
            )

            self.logger.info(f"Started learning workflow: {learning_workflow_id}")
            return True

        except Exception as e:
            self.logger.error(
                f"Failed to execute learning workflow: {learning_workflow_id} - {e}"
            )
            return False

    def execute_learning_step(self, learning_workflow_id: str, step_id: str) -> bool:
        """Execute learning step using existing workflow engine"""
        if learning_workflow_id not in self.learning_workflow_sessions:
            self.logger.error(f"Learning workflow not found: {learning_workflow_id}")
            return False

        try:
            learning_session = self.learning_workflow_sessions[learning_workflow_id]
            workflow_execution_id = learning_session["workflow_execution_id"]
            learning_session_id = learning_session["learning_session_id"]

            # Use existing workflow engine to execute step
            if not self.workflow_engine.execute_workflow_step(
                workflow_execution_id, step_id
            ):
                return False

            # Execute learning operation using existing learning engine
            step = next(
                (
                    s
                    for s in self.workflow_engine.active_workflows[
                        workflow_execution_id
                    ].steps
                    if s.step_id == step_id
                ),
                None,
            )

            if step:
                operation_type = step.metadata.get("learning_operation", "general")

                if operation_type == "session_initiation":
                    # Use existing learning engine for session initiation
                    self.logger.info(
                        f"Learning session initiation completed for step: {step_id}"
                    )

                elif operation_type == "learning_execution":
                    # Use existing learning engine for execution
                    execution_result = self.learning_engine.execute_learning_operation(
                        session_id=learning_session_id,
                        operation_type="workflow_step_execution",
                        parameters={
                            "step_id": step_id,
                            "workflow_name": learning_session["workflow_name"],
                        },
                    )

                    if not execution_result:
                        self.logger.error(
                            f"Learning execution failed for step: {step_id}"
                        )
                        return False

                elif operation_type == "progress_evaluation":
                    # Use existing metrics system for evaluation
                    performance_summary = (
                        self.learning_engine.get_learning_performance_summary(
                            learning_session["agent_id"]
                        )
                    )

                    if performance_summary and "error" not in performance_summary:
                        self.logger.info(
                            f"Learning progress evaluation completed for step: {step_id}"
                        )
                    else:
                        self.logger.error(
                            f"Learning progress evaluation failed for step: {step_id}"
                        )
                        return False

            # Trigger step completed hook
            self._trigger_learning_hooks(
                "learning_workflow_step_completed",
                {
                    "learning_workflow_id": learning_workflow_id,
                    "step_id": step_id,
                    "workflow_execution_id": workflow_execution_id,
                    "learning_session_id": learning_session_id,
                },
            )

            self.logger.info(f"Completed learning step: {step_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to execute learning step: {step_id} - {e}")
            return False

    def get_learning_workflow_status(self, learning_workflow_id: str) -> Dict[str, Any]:
        """Get status of learning workflow"""
        if learning_workflow_id not in self.learning_workflow_sessions:
            return {"error": "Learning workflow not found"}

        learning_session = self.learning_workflow_sessions[learning_workflow_id]
        workflow_execution_id = learning_session["workflow_execution_id"]

        # Get workflow status from existing workflow engine
        workflow_status = self.workflow_engine.get_workflow_status(
            workflow_execution_id
        )

        # Get learning session status from existing learning engine
        learning_session_data = self.learning_engine.get_learning_session(
            learning_session["learning_session_id"]
        )

        return {
            "learning_workflow_id": learning_workflow_id,
            "workflow_name": learning_session["workflow_name"],
            "workflow_execution_id": workflow_execution_id,
            "learning_session_id": learning_session["learning_session_id"],
            "agent_id": learning_session["agent_id"],
            "workflow_status": workflow_status.value if workflow_status else "unknown",
            "learning_session_status": learning_session_data.get("status", "unknown")
            if learning_session_data
            else "unknown",
            "learning_parameters": learning_session["learning_parameters"],
            "start_time": learning_session["start_time"].isoformat(),
            "current_status": learning_session["status"],
        }

    def list_learning_workflows(
        self, status_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List learning workflows with optional status filter"""
        workflows = []

        for (
            learning_workflow_id,
            learning_session,
        ) in self.learning_workflow_sessions.items():
            if status_filter is None or learning_session["status"] == status_filter:
                workflows.append(
                    self.get_learning_workflow_status(learning_workflow_id)
                )

        return workflows

    def get_integration_metrics(self) -> Dict[str, Any]:
        """Get learning workflow integration metrics"""
        metrics = self.integration_metrics.copy()

        # Add existing learning engine metrics
        engine_status = self.learning_engine.get_engine_status()
        metrics["learning_engine_status"] = engine_status

        # Add existing workflow engine metrics
        workflow_stats = self.workflow_engine.get_workflow_stats()
        metrics["workflow_engine_status"] = workflow_stats

        return metrics

    def _on_learning_workflow_started(self, data: Dict[str, Any]) -> None:
        """Handle learning workflow started event"""
        learning_workflow_id = data["learning_workflow_id"]
        self.logger.info(f"Learning workflow started: {learning_workflow_id}")

        # Update workflow status
        if learning_workflow_id in self.learning_workflow_sessions:
            self.learning_workflow_sessions[learning_workflow_id]["status"] = "running"

    def _on_learning_workflow_step_completed(self, data: Dict[str, Any]) -> None:
        """Handle learning workflow step completed event"""
        learning_workflow_id = data["learning_workflow_id"]
        step_id = data["step_id"]

        self.logger.info(
            f"Learning workflow step completed: {step_id} in workflow: {learning_workflow_id}"
        )

        # Check if workflow is completed (simplified check)
        if learning_workflow_id in self.learning_workflow_sessions:
            learning_session = self.learning_workflow_sessions[learning_workflow_id]
            workflow_execution_id = learning_session["workflow_execution_id"]

            # Check workflow status using existing workflow engine
            workflow_status = self.workflow_engine.get_workflow_status(
                workflow_execution_id
            )

            if workflow_status == WorkflowStatus.COMPLETED:
                learning_session["status"] = "completed"
                self.integration_metrics["completed_learning_workflows"] += 1
                self.integration_metrics["active_learning_workflows"] -= 1

                # Trigger completion hook
                self._trigger_learning_hooks(
                    "learning_workflow_completed",
                    {
                        "learning_workflow_id": learning_workflow_id,
                        "workflow_execution_id": workflow_execution_id,
                        "completion_time": datetime.now(),
                    },
                )

    def _on_learning_workflow_completed(self, data: Dict[str, Any]) -> None:
        """Handle learning workflow completed event"""
        learning_workflow_id = data["learning_workflow_id"]
        self.logger.info(f"Learning workflow completed: {learning_workflow_id}")

    def _on_learning_workflow_failed(self, data: Dict[str, Any]) -> None:
        """Handle learning workflow failed event"""
        learning_workflow_id = data["learning_workflow_id"]
        self.logger.error(f"Learning workflow failed: {learning_workflow_id}")

        # Update metrics
        if learning_workflow_id in self.learning_workflow_sessions:
            self.learning_workflow_sessions[learning_workflow_id]["status"] = "failed"
            self.integration_metrics["failed_learning_workflows"] += 1
            self.integration_metrics["active_learning_workflows"] -= 1

    def cleanup_completed_workflows(self) -> None:
        """Clean up completed learning workflows"""
        completed_ids = []

        for (
            learning_workflow_id,
            learning_session,
        ) in self.learning_workflow_sessions.items():
            if learning_session["status"] in ["completed", "failed"]:
                completed_ids.append(learning_workflow_id)

        for learning_workflow_id in completed_ids:
            del self.learning_workflow_sessions[learning_workflow_id]
            self.logger.info(
                f"Cleaned up completed learning workflow: {learning_workflow_id}"
            )

    def run_integration_test(self) -> bool:
        """Run a test to verify integration with existing systems"""
        try:
            self.logger.info("Running learning workflow integration test")

            # Create learning workflow
            learning_workflow_id = self.create_learning_workflow(
                workflow_name="test_learning",
                agent_id="test_agent_001",
                learning_parameters={"test_mode": True},
            )

            if not learning_workflow_id:
                return False

            # Execute workflow
            if not self.execute_learning_workflow(learning_workflow_id):
                return False

            # Execute steps
            learning_session = self.learning_workflow_sessions[learning_workflow_id]
            workflow_execution_id = learning_session["workflow_execution_id"]

            workflow_execution = self.workflow_engine.active_workflows.get(
                workflow_execution_id
            )
            if workflow_execution:
                for step in workflow_execution.steps:
                    if not self.execute_learning_step(
                        learning_workflow_id, step.step_id
                    ):
                        return False

            # Verify completion
            status = self.get_learning_workflow_status(learning_workflow_id)
            if status.get("current_status") == "completed":
                self.logger.info(
                    f"Learning workflow integration test passed: {learning_workflow_id}"
                )
                return True
            else:
                self.logger.error(
                    f"Learning workflow integration test failed: {learning_workflow_id}"
                )
                return False

        except Exception as e:
            self.logger.error(f"Learning workflow integration test failed: {e}")
            return False
