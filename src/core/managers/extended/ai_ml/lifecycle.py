"""Agent lifecycle management for extended AI/ML managers."""

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .constants import (
    WORKFLOW_STATUS_COMPLETED,
    WORKFLOW_STATUS_CREATED,
    WORKFLOW_STATUS_FAILED,
    WORKFLOW_STATUS_RUNNING,
)
from .metrics import MetricsCollector

EventEmitter = Callable[[str, Dict[str, Any]], None]


class AgentLifecycle:
    """Manage models and workflows with metric tracking."""

    def __init__(
        self, metrics: MetricsCollector, emit_event: Optional[EventEmitter] = None
    ) -> None:
        self.metrics = metrics
        self.emit_event = emit_event
        self.models: Dict[str, Any] = {}
        self.workflows: Dict[str, Dict[str, Any]] = {}

    def register_model(self, model: Any) -> bool:
        """Register an AI model."""
        try:
            model_name = getattr(model, "name", str(id(model)))
            self.models[model_name] = model
            self.metrics.record_success()
            if self.emit_event:
                self.emit_event(
                    "model_registered",
                    {"model_name": model_name, "total_models": len(self.models)},
                )
            return True
        except Exception:
            self.metrics.record_failure()
            return False

    def get_model(self, model_name: str) -> Optional[Any]:
        """Retrieve a registered model by name."""
        model = self.models.get(model_name)
        if model:
            self.metrics.record_success()
            if self.emit_event:
                self.emit_event("model_retrieved", {"model_name": model_name})
        return model

    def list_models(self) -> List[str]:
        """List all registered model names."""
        return list(self.models.keys())

    def create_workflow(self, name: str, description: str) -> Dict[str, Any]:
        """Create a new workflow definition."""
        workflow = {
            "name": name,
            "description": description,
            "status": WORKFLOW_STATUS_CREATED,
            "steps": [],
            "created_at": datetime.utcnow().isoformat(),
        }
        self.workflows[name] = workflow
        self.metrics.record_success()
        if self.emit_event:
            self.emit_event(
                "workflow_created",
                {"workflow_name": name, "total_workflows": len(self.workflows)},
            )
        return workflow

    def get_workflow(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a workflow by name."""
        return self.workflows.get(name)

    def list_workflows(self) -> List[str]:
        """List all workflow names."""
        return list(self.workflows.keys())

    def add_workflow_step(
        self, workflow_name: str, step_name: str, step_type: str = "task"
    ) -> bool:
        """Add a step to an existing workflow."""
        workflow = self.get_workflow(workflow_name)
        if not workflow:
            return False
        step = {"name": step_name, "type": step_type, "status": "pending"}
        workflow.setdefault("steps", []).append(step)
        self.metrics.record_success()
        if self.emit_event:
            self.emit_event(
                "workflow_step_added",
                {"workflow_name": workflow_name, "step_name": step_name},
            )
        return True

    def execute_workflow(self, workflow_name: str) -> bool:
        """Execute the steps in a workflow."""
        workflow = self.get_workflow(workflow_name)
        if not workflow:
            return False
        try:
            workflow["status"] = WORKFLOW_STATUS_RUNNING
            if self.emit_event:
                self.emit_event(
                    "workflow_execution_started", {"workflow_name": workflow_name}
                )
            for step in workflow.get("steps", []):
                if step.get("status") == "pending":
                    step["status"] = WORKFLOW_STATUS_RUNNING
                    step["status"] = WORKFLOW_STATUS_COMPLETED
            workflow["status"] = WORKFLOW_STATUS_COMPLETED
            self.metrics.record_success()
            if self.emit_event:
                self.emit_event(
                    "workflow_execution_completed",
                    {
                        "workflow_name": workflow_name,
                        "status": WORKFLOW_STATUS_COMPLETED,
                    },
                )
            return True
        except Exception as exc:  # pragma: no cover - defensive
            workflow["status"] = WORKFLOW_STATUS_FAILED
            self.metrics.record_failure()
            if self.emit_event:
                self.emit_event(
                    "workflow_execution_failed",
                    {"workflow_name": workflow_name, "error": str(exc)},
                )
            return False
