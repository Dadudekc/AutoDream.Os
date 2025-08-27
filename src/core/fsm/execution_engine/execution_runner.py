#!/usr/bin/env python3
"""State execution and transition handling for FSM core."""

import time
from datetime import datetime
from typing import Optional

from .common import (
    StateExecutionResult,
    TransitionDefinition,
    StateStatus,
    TransitionType,
    build_context,
    execute_actions,
)


class ExecutionRunner:
    """Provides state execution helpers."""

    def _execute_state(self, workflow_id: str, state_name: str) -> bool:
        """Execute a specific state in a workflow."""
        try:
            workflow = self.workflows[workflow_id]
            state_def = self.states[state_name]

            if not state_def:
                self.logger.error(f"State {state_name} not found")
                return False

            workflow.current_state = state_name
            workflow.last_update = datetime.now()

            execute_actions(workflow_id, state_def.entry_actions, "entry", self.logger)

            if state_name in self.state_handlers:
                handler = self.state_handlers[state_name]
                context = build_context(workflow)

                start_time = time.time()
                result = handler.execute(context)
                execution_time = time.time() - start_time

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

                if result.status == StateStatus.COMPLETED:
                    self._handle_state_completion(workflow_id, state_name, result)
                elif result.status == StateStatus.FAILED:
                    self._handle_state_failure(workflow_id, state_name, result)
                elif result.status == StateStatus.TIMEOUT:
                    self._handle_state_timeout(workflow_id, state_name, result)

            else:
                self._handle_state_completion(workflow_id, state_name, None)

            return True

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(
                f"Failed to execute state {state_name} in workflow {workflow_id}: {e}"
            )
            return False

    def _handle_state_completion(
        self,
        workflow_id: str,
        state_name: str,
        result: Optional[StateExecutionResult],
    ) -> None:
        """Handle successful state completion."""
        try:
            workflow = self.workflows[workflow_id]

            available_transitions = self.get_available_transitions(
                state_name, build_context(workflow)
            )

            if available_transitions:
                next_transition = available_transitions[0]
                self._execute_transition(workflow_id, next_transition)
            else:
                workflow.status = StateStatus.COMPLETED
                workflow.last_update = datetime.now()
                self.active_workflows.remove(workflow_id)
                self.successful_workflows += 1
                self.logger.info(f"✅ Workflow {workflow_id} completed")

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(
                f"Failed to handle state completion for {workflow_id}: {e}"
            )

    def _handle_state_failure(
        self,
        workflow_id: str,
        state_name: str,
        result: Optional[StateExecutionResult],
    ) -> None:
        """Handle state failure."""
        try:
            workflow = self.workflows[workflow_id]
            workflow.error_count += 1

            if workflow.retry_count < self.config.get("retry_policy", {}).get(
                "max_retries", 3
            ):
                workflow.retry_count += 1
                time.sleep(self.config.get("retry_policy", {}).get("retry_delay", 5.0))
                self._execute_state(workflow_id, state_name)
                return

            workflow.status = StateStatus.FAILED
            workflow.last_update = datetime.now()
            self.active_workflows.remove(workflow_id)
            self.failed_workflows += 1
            self.logger.error(f"❌ Workflow {workflow_id} failed")

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to handle state failure for {workflow_id}: {e}")

    def _handle_state_timeout(
        self,
        workflow_id: str,
        state_name: str,
        result: Optional[StateExecutionResult],
    ) -> None:
        """Handle state timeout."""
        try:
            workflow = self.workflows[workflow_id]

            available_transitions = self.get_transitions(state_name)
            for transition in available_transitions:
                if transition.transition_type == TransitionType.TIMEOUT:
                    self._execute_transition(workflow_id, transition)
                    return

            workflow.status = StateStatus.TIMEOUT
            workflow.last_update = datetime.now()
            self.active_workflows.remove(workflow_id)
            self.failed_workflows += 1
            self.logger.warning(f"⚠️ Workflow {workflow_id} timed out")

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to handle state timeout for {workflow_id}: {e}")

    def _execute_transition(
        self, workflow_id: str, transition: TransitionDefinition
    ) -> None:
        """Execute a state transition."""
        try:
            workflow = self.workflows[workflow_id]
            old_state = workflow.current_state

            execute_actions(workflow_id, transition.actions, "transition", self.logger)

            workflow.current_state = transition.to_state
            workflow.last_update = datetime.now()
            self.total_state_transitions += 1

            if old_state in self.states:
                old_state_def = self.states[old_state]
                execute_actions(
                    workflow_id, old_state_def.exit_actions, "exit", self.logger
                )

            self._execute_state(workflow_id, transition.to_state)

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to execute transition: {e}")


__all__ = ["ExecutionRunner"]
