from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from src.core.models import Workflow


class WorkflowManagerInterface(ABC):
    """Interface for managing AI/ML development workflows."""

    @abstractmethod
    def create_workflow(
        self,
        name: str,
        description: str,
        workflow_type: str,
        steps: List[Dict[str, Any]],
    ) -> str:
        """Create a new workflow and return its identifier."""

    @abstractmethod
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Retrieve workflow details by ID."""

    @abstractmethod
    def list_workflows(self, workflow_type: Optional[str] = None) -> List[Workflow]:
        """List available workflows with optional filtering."""
