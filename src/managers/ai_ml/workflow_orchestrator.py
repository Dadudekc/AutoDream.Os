from typing import Any, Dict, List, Optional

from src.core.managers.unified_ai_ml_manager import UnifiedAIMLManager
from src.core.models import Workflow

from .interfaces.workflow import WorkflowManagerInterface


class WorkflowOrchestrator(WorkflowManagerInterface):
    """Orchestration layer for AI/ML workflow operations."""

    def __init__(self, manager: Optional[UnifiedAIMLManager] = None) -> None:
        self.manager = manager or UnifiedAIMLManager()

    def create_workflow(
        self,
        name: str,
        description: str,
        workflow_type: str,
        steps: List[Dict[str, Any]],
    ) -> str:
        return self.manager.create_workflow(name, description, workflow_type, steps)

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        return self.manager.get_workflow(workflow_id)

    def list_workflows(self, workflow_type: Optional[str] = None) -> List[Workflow]:
        return self.manager.list_workflows(workflow_type=workflow_type)
