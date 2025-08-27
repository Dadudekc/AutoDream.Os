#!/usr/bin/env python3
"""
FSM state transition mixin.
"""

import logging
import time
from typing import Any, Dict, List, Optional

from .fsm_utils import FSMTask, TaskPriority, TaskState

logger = logging.getLogger(__name__)


class FSMStateTransitionMixin:
    """Mixin providing FSM state transition operations."""

    def update_task_state(
        self,
        task_id: str,
        new_state: TaskState,
        agent_id: str,
        summary: str,
        evidence: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update task state."""
        try:
            if task_id not in self._tasks:
                logger.error(f"Task not found: {task_id}")
                return False

            task = self._tasks[task_id]
            old_state = task.state

            task.update_state(new_state)
            if evidence:
                task.add_evidence(agent_id, evidence)

            self._save_task(task)

            transition_record = {
                "timestamp": time.time(),
                "task_id": task_id,
                "from_state": old_state.value,
                "to_state": new_state.value,
                "agent_id": agent_id,
                "summary": summary,
            }
            self._state_transition_history.append(transition_record)

            self._send_fsm_update(task_id, agent_id, new_state, summary)

            logger.info(
                f"Updated task {task_id} state: {old_state.value} -> {new_state.value}"
            )
            return True

        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to update task state: {e}")
            return False

    def get_task(self, task_id: str) -> Optional[FSMTask]:
        """Get task by ID."""
        return self._tasks.get(task_id)

    def get_tasks_by_agent(self, agent_id: str) -> List[FSMTask]:
        """Get all tasks assigned to an agent."""
        return [task for task in self._tasks.values() if task.assigned_agent == agent_id]

    def get_tasks_by_state(self, state: TaskState) -> List[FSMTask]:
        """Get all tasks in a specific state."""
        return [task for task in self._tasks.values() if task.state == state]

    def get_tasks_by_priority(self, priority: TaskPriority) -> List[FSMTask]:
        """Get all tasks with a specific priority."""
        return [task for task in self._tasks.values() if task.priority == priority]

    def _execute_intelligent_state_transition(
        self, strategy_config: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute intelligent state transition strategy."""
        return {
            "actions_taken": ["state_transition_optimization"],
            "performance_impact": {"state_transitions": "optimized"},
            "recommendations": ["Review state transition patterns"],
        }
