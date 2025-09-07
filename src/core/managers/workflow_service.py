"""Service for workflow management."""
from typing import Dict, List, Optional, Any

from .task_models import Workflow, TaskStatus


class WorkflowService:
    """Handle workflow creation and queries."""

    def __init__(self, manager) -> None:
        self._manager = manager

    def create(
        self,
        name: str,
        description: str,
        tasks: List[str],
        dependencies: Dict[str, List[str]],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        workflow_id = self._manager._generate_id()
        workflow = Workflow(
            id=workflow_id,
            name=name,
            description=description,
            tasks=tasks,
            dependencies=dependencies,
            status=TaskStatus.PENDING,
            created_at=self._manager._now_iso(),
            started_at=None,
            completed_at=None,
            metadata=metadata or {},
        )
        with self._manager.workflow_lock:
            self._manager.workflows[workflow_id] = workflow
        self._manager._emit_event(
            "workflow_created",
            {"workflow_id": workflow_id, "name": name, "task_count": len(tasks)},
        )
        return workflow_id

    def get_info(self, workflow_id: str) -> Optional[Workflow]:
        return self._manager.workflows.get(workflow_id)
