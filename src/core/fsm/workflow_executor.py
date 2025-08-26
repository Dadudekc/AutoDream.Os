#!/usr/bin/env python3
"""
Workflow Executor - V2 Modular Architecture
===========================================

Workflow execution and monitoring functionality.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4I - FSM System Modularization
License: MIT
"""

import logging
import time
import threading
from typing import Dict, List, Optional, Any, Set
from collections import deque
from datetime import datetime

from .models import (
    WorkflowInstance,
    StateDefinition,
    TransitionDefinition,
    StateStatus,
    StateExecutionResult,
    StateHandler,
)
from .types import FSMConfig


logger = logging.getLogger(__name__)


class WorkflowExecutor:
    """
    Workflow Executor - Workflow Lifecycle Management

    Single responsibility: Execute workflows, manage state transitions,
    and monitor workflow progress following V2 architecture standards.
    """

    def __init__(self, config: Optional[FSMConfig] = None):
        """Initialize workflow executor."""
        self.logger = logging.getLogger(f"{__name__}.WorkflowExecutor")

        # Configuration
        self.config = config or FSMConfig()

        # Workflow execution state
        self.active_workflows: Set[str] = set()
        # Store queued workflows with their execution context
        self.workflow_queue: deque = deque()

        # Monitoring
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active = False

        # Statistics
        self.total_workflows_executed = 0
        self.successful_workflows = 0
        self.failed_workflows = 0
        self.total_state_transitions = 0

        self.logger.info("✅ Workflow Executor initialized successfully")

    # ============================================================================
    # WORKFLOW EXECUTION
    # ============================================================================

    def start_workflow(
        self,
        workflow_id: str,
        workflow: WorkflowInstance,
        states: Dict[str, StateDefinition],
        transitions: Dict[str, List[TransitionDefinition]],
        state_handlers: Dict[str, StateHandler],
    ) -> bool:
        """Start a workflow execution."""
        try:
            if workflow.status != StateStatus.PENDING:
                self.logger.warning(f"Workflow {workflow_id} is not in pending state")
                return False

            # Check concurrent workflow limit
            if len(self.active_workflows) >= self.config.max_concurrent_workflows:
                self.logger.warning(
                    f"Maximum concurrent workflows reached, queuing {workflow_id}"
                )
                # Store full execution context so the workflow can be started later
                self.workflow_queue.append(
                    {
                        "workflow_id": workflow_id,
                        "workflow": workflow,
                        "states": states,
                        "transitions": transitions,
                        "state_handlers": state_handlers,
                    }
                )
                return False

            # Start workflow
            workflow.status = StateStatus.ACTIVE
            workflow.last_update = time.time()
            self.active_workflows.add(workflow_id)

            # Execute initial state
            self._execute_state(
                workflow_id,
                workflow,
                workflow.current_state,
                states,
                transitions,
                state_handlers,
            )

            self.logger.info(f"✅ Started workflow: {workflow_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start workflow {workflow_id}: {e}")
            return False

    def stop_workflow(self, workflow_id: str, workflow: WorkflowInstance) -> bool:
        """Stop a workflow execution."""
        try:
            if workflow.status not in [StateStatus.ACTIVE, StateStatus.PENDING]:
                return False

            # Stop workflow
            workflow.status = StateStatus.FAILED
            workflow.last_update = time.time()

            if workflow_id in self.active_workflows:
                self.active_workflows.remove(workflow_id)

            self.logger.info(f"✅ Stopped workflow: {workflow_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to stop workflow {workflow_id}: {e}")
            return False

    def _execute_state(
        self,
        workflow_id: str,
        workflow: WorkflowInstance,
        state_name: str,
        states: Dict[str, StateDefinition],
        transitions: Dict[str, List[TransitionDefinition]],
        state_handlers: Dict[str, StateHandler],
    ) -> bool:
        """Execute a specific state in a workflow."""
        try:
            state_def = states.get(state_name)
            if not state_def:
                self.logger.error(f"State {state_name} not found")
                return False

            # Update workflow state
            workflow.current_state = state_name
            workflow.last_update = time.time()

            # Execute entry actions
            self._execute_actions(workflow_id, state_def.entry_actions, "entry")

            # Execute state logic if handler exists
            if state_name in state_handlers:
                handler = state_handlers[state_name]
                context = self._build_context(workflow)

                start_time = time.time()
                result = handler.execute(context)
                execution_time = time.time() - start_time

                # Update state history
                workflow.state_history.append(
                    {
                        "state": state_name,
                        "execution_time": execution_time,
                        "status": result.status.value,
                        "output": result.output,
                        "error_message": result.error_message,
                        "timestamp": result.timestamp.isoformat(),
                    }
                )

                # Handle execution result
                if result.status == StateStatus.COMPLETED:
                    self._handle_state_completion(
                        workflow_id, workflow, state_name, result, states, transitions
                    )
                elif result.status == StateStatus.FAILED:
                    self._handle_state_failure(
                        workflow_id, workflow, state_name, result, state_def
                    )
                elif result.status == StateStatus.TIMEOUT:
                    self._handle_state_timeout(
                        workflow_id, workflow, state_name, result
                    )

            else:
                # No handler, mark as completed
                self._handle_state_completion(
                    workflow_id, workflow, state_name, None, states, transitions
                )

            return True

        except Exception as e:
            self.logger.error(
                f"Failed to execute state {state_name} in workflow {workflow_id}: {e}"
            )
            return False

    def _execute_actions(
        self, workflow_id: str, actions: List[str], action_type: str
    ) -> None:
        """Execute a list of actions."""
        for action in actions:
            try:
                self.logger.debug(
                    f"Executing {action_type} action: {action} for workflow {workflow_id}"
                )
                # Action execution logic can be extended here

            except Exception as e:
                self.logger.error(
                    f"Failed to execute {action_type} action {action}: {e}"
                )

    def _build_context(self, workflow: WorkflowInstance) -> Dict[str, Any]:
        """Build execution context for state handlers."""
        return {
            "workflow_id": workflow.workflow_id,
            "workflow_name": workflow.workflow_name,
            "current_state": workflow.current_state,
            "state_history": workflow.state_history,
            "metadata": workflow.metadata,
            "start_time": workflow.start_time,
            "priority": workflow.priority.value,
        }

    def _handle_state_completion(
        self,
        workflow_id: str,
        workflow: WorkflowInstance,
        state_name: str,
        result: Optional[StateExecutionResult],
        states: Dict[str, StateDefinition],
        transitions: Dict[str, List[TransitionDefinition]],
    ) -> None:
        """Handle successful state completion."""
        try:
            # Find available transitions
            available_transitions = self._get_available_transitions(
                state_name, self._build_context(workflow), transitions
            )

            if available_transitions:
                # Execute automatic transition
                next_transition = available_transitions[0]  # Highest priority
                self._execute_transition(
                    workflow_id, workflow, next_transition, states, transitions
                )
            else:
                # No transitions available, workflow completed
                workflow.status = StateStatus.COMPLETED
                workflow.last_update = time.time()
                self.active_workflows.discard(workflow_id)

                self.successful_workflows += 1
                self.logger.info(f"✅ Workflow {workflow_id} completed successfully")

        except Exception as e:
            self.logger.error(f"Failed to handle state completion: {e}")

    def _handle_state_failure(
        self,
        workflow_id: str,
        workflow: WorkflowInstance,
        state_name: str,
        result: StateExecutionResult,
        state_def: StateDefinition,
    ) -> None:
        """Handle state execution failure."""
        try:
            workflow.error_count += 1

            # Check retry policy
            if workflow.retry_count < state_def.retry_count:
                workflow.retry_count += 1
                self.logger.info(
                    f"Retrying state {state_name} in workflow {workflow_id} (attempt {workflow.retry_count})"
                )

                # Schedule retry
                threading.Timer(
                    state_def.retry_delay,
                    lambda: self._execute_state(
                        workflow_id, workflow, state_name, {}, {}, {}
                    ),
                ).start()
            else:
                # Max retries exceeded
                workflow.status = StateStatus.FAILED
                workflow.last_update = time.time()
                self.active_workflows.discard(workflow_id)

                self.failed_workflows += 1
                self.logger.error(
                    f"❌ Workflow {workflow_id} failed after {workflow.retry_count} retries"
                )

        except Exception as e:
            self.logger.error(f"Failed to handle state failure: {e}")

    def _handle_state_timeout(
        self,
        workflow_id: str,
        workflow: WorkflowInstance,
        state_name: str,
        result: StateExecutionResult,
    ) -> None:
        """Handle state execution timeout."""
        try:
            workflow.status = StateStatus.TIMEOUT
            workflow.last_update = time.time()
            self.active_workflows.discard(workflow_id)

            self.failed_workflows += 1
            self.logger.error(
                f"⏰ Workflow {workflow_id} timed out in state {state_name}"
            )

        except Exception as e:
            self.logger.error(f"Failed to handle state timeout: {e}")

    def _execute_transition(
        self,
        workflow_id: str,
        workflow: WorkflowInstance,
        transition: TransitionDefinition,
        states: Dict[str, StateDefinition],
        transitions: Dict[str, List[TransitionDefinition]],
    ) -> bool:
        """Execute a state transition."""
        try:
            # Execute transition actions
            self._execute_actions(workflow_id, transition.actions, "transition")

            # Update workflow state
            old_state = workflow.current_state
            workflow.current_state = transition.to_state
            workflow.last_update = time.time()

            # Execute exit actions for old state
            old_state_def = states.get(old_state)
            if old_state_def:
                self._execute_actions(workflow_id, old_state_def.exit_actions, "exit")

            # Execute new state
            self._execute_state(
                workflow_id, workflow, transition.to_state, states, transitions, {}
            )

            self.total_state_transitions += 1
            self.logger.info(
                f"✅ Transition: {old_state} -> {transition.to_state} in workflow {workflow_id}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to execute transition: {e}")
            return False

    def _get_available_transitions(
        self,
        current_state: str,
        context: Dict[str, Any],
        transitions: Dict[str, List[TransitionDefinition]],
    ) -> List[TransitionDefinition]:
        """Get available transitions from current state."""
        available = []

        for transition in transitions.get(current_state, []):
            # Check if transition is available
            if self._can_execute_transition(transition, context):
                available.append(transition)

        # Sort by priority
        available.sort(key=lambda t: t.priority, reverse=True)
        return available

    def _can_execute_transition(
        self, transition: TransitionDefinition, context: Dict[str, Any]
    ) -> bool:
        """Check if a transition can be executed."""
        try:
            # Check condition if specified
            if transition.condition:
                # Simple condition evaluation (can be extended)
                return self._evaluate_condition(transition.condition, context)

            return True

        except Exception as e:
            self.logger.error(f"Failed to evaluate transition condition: {e}")
            return False

    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a transition condition."""
        try:
            # Simple condition evaluation (can be extended with more complex logic)
            if "==" in condition:
                key, value = condition.split("==")
                return str(context.get(key.strip())) == value.strip()
            elif "!=" in condition:
                key, value = condition.split("!=")
                return str(context.get(key.strip())) != value.strip()
            elif ">" in condition:
                key, value = condition.split(">")
                return float(context.get(key.strip(), 0)) > float(value.strip())
            elif "<" in condition:
                key, value = condition.split("<")
                return float(context.get(key.strip(), 0)) < float(value.strip())
            else:
                # Simple key existence check
                return condition.strip() in context

        except Exception as e:
            self.logger.error(f"Failed to evaluate condition '{condition}': {e}")
            return False

    # ============================================================================
    # MONITORING AND CONTROL
    # ============================================================================

    def start_monitoring(self) -> bool:
        """Start workflow monitoring."""
        try:
            if self.monitoring_active:
                return True

            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(
                target=self._monitoring_loop, daemon=True
            )
            self.monitoring_thread.start()
            self.logger.info("✅ Workflow monitoring started")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            return False

    def stop_monitoring(self) -> bool:
        """Stop workflow monitoring."""
        try:
            self.monitoring_active = False
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=5.0)
            self.logger.info("✅ Workflow monitoring stopped")
            return True

        except Exception as e:
            self.logger.error(f"Failed to stop monitoring: {e}")
            return False

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                # Process workflow queue
                self._process_workflow_queue()

                # Sleep for monitoring interval
                interval = self.config.monitoring.get("interval", 1.0)
                time.sleep(interval)

            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(1.0)

    def _process_workflow_queue(self) -> None:
        """Process pending workflows in queue."""
        try:
            while (
                self.workflow_queue
                and len(self.active_workflows) < self.config.max_concurrent_workflows
            ):
                item = self.workflow_queue.popleft()

                # Support both legacy queue items (workflow_id) and new dict context
                if isinstance(item, dict):
                    workflow_id = item["workflow_id"]
                    workflow = item["workflow"]
                    states = item["states"]
                    transitions = item["transitions"]
                    state_handlers = item["state_handlers"]
                else:  # Fallback to simple workflow_id if provided
                    workflow_id = item
                    self.logger.debug(
                        "Workflow %s lacks execution context; skipping", workflow_id
                    )
                    continue

                # Start the queued workflow
                workflow.status = StateStatus.ACTIVE
                workflow.last_update = time.time()
                self.active_workflows.add(workflow_id)
                self._execute_state(
                    workflow_id,
                    workflow,
                    workflow.current_state,
                    states,
                    transitions,
                    state_handlers,
                )

                self.logger.info(f"✅ Started queued workflow: {workflow_id}")

        except Exception as e:
            self.logger.error(f"Failed to process workflow queue: {e}")

    # ============================================================================
    # STATISTICS AND REPORTING
    # ============================================================================

    def get_execution_stats(self) -> Dict[str, Any]:
        """Get workflow execution statistics."""
        return {
            "active_workflows": len(self.active_workflows),
            "queued_workflows": len(self.workflow_queue),
            "total_workflows_executed": self.total_workflows_executed,
            "successful_workflows": self.successful_workflows,
            "failed_workflows": self.failed_workflows,
            "total_state_transitions": self.total_state_transitions,
            "monitoring_active": self.monitoring_active,
            "last_updated": time.time(),
        }
