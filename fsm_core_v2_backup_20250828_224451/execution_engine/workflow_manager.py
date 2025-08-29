#!/usr/bin/env python3
"""Workflow management mixin for FSM core."""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from .common import WorkflowPriority, WorkflowInstance, StateStatus


class WorkflowManager:
    """Provides workflow lifecycle operations."""

    def create_workflow(
        self,
        workflow_name: str,
        initial_state: str,
        priority: WorkflowPriority = WorkflowPriority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Create a new workflow instance."""
        try:
            if initial_state not in self.states:
                self.logger.error(f"Initial state {initial_state} not found")
                return None

            workflow_id = f"{workflow_name}_{int(time.time())}_{hash(workflow_name)}"

            workflow = WorkflowInstance(
                workflow_id=workflow_id,
                workflow_name=workflow_name,
                current_state=initial_state,
                state_history=[],
                start_time=datetime.now(),
                last_update=datetime.now(),
                status=StateStatus.PENDING,
                priority=priority,
                metadata=metadata or {},
                error_count=0,
                retry_count=0,
            )

            self.workflows[workflow_id] = workflow
            self.workflow_queue.append(workflow_id)

            self.logger.info(
                f"✅ Created workflow: {workflow_id} starting at {initial_state}"
            )
            return workflow_id

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to create workflow: {e}")
            return None

    def start_workflow(self, workflow_id: str) -> bool:
        """Start a workflow execution."""
        try:
            if workflow_id not in self.workflows:
                self.logger.error(f"Workflow {workflow_id} not found")
                return False

            workflow = self.workflows[workflow_id]

            if workflow.status != StateStatus.PENDING:
                self.logger.warning(f"Workflow {workflow_id} is not in pending state")
                return False

            if len(self.active_workflows) >= self.max_concurrent_workflows:
                self.logger.warning(
                    f"Maximum concurrent workflows reached, queuing {workflow_id}"
                )
                return False

            workflow.status = StateStatus.ACTIVE
            workflow.last_update = datetime.now()
            self.active_workflows.add(workflow_id)

            self._execute_state(workflow_id, workflow.current_state)

            self.logger.info(f"✅ Started workflow: {workflow_id}")
            return True

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to start workflow {workflow_id}: {e}")
            return False

    def stop_workflow(self, workflow_id: str) -> bool:
        """Stop a workflow execution."""
        try:
            if workflow_id not in self.workflows:
                return False

            workflow = self.workflows[workflow_id]

            if workflow.status not in [StateStatus.ACTIVE, StateStatus.PENDING]:
                return False

            workflow.status = StateStatus.FAILED
            workflow.last_update = datetime.now()

            if workflow_id in self.active_workflows:
                self.active_workflows.remove(workflow_id)

            self.logger.info(f"✅ Stopped workflow: {workflow_id}")
            return True

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to stop workflow {workflow_id}: {e}")
            return False

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """Get workflow instance by ID."""
        return self.workflows.get(workflow_id)

    def list_workflows(
        self, status: Optional[StateStatus] = None
    ) -> List[WorkflowInstance]:
        """List workflows with optional status filter."""
        if status is None:
            return list(self.workflows.values())

        return [w for w in self.workflows.values() if w.status == status]


__all__ = ["WorkflowManager"]
