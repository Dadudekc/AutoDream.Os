"""Workflow configuration data model."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .model_utils import WorkflowType


@dataclass
class Workflow:
    """Representation of an operational workflow."""

    workflow_id: str
    name: str
    description: str
    workflow_type: WorkflowType
    steps: List[Dict[str, Any]]
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_executed: Optional[datetime] = None
    execution_count: int = 0

    def __post_init__(self) -> None:
        """Normalise enum fields."""
        if isinstance(self.workflow_type, str):
            self.workflow_type = WorkflowType(self.workflow_type)
