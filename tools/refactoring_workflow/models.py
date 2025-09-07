from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .enums import WorkflowType, WorkflowState


@dataclass
class WorkflowStep:
    """Individual step in a refactoring workflow"""

    id: str
    name: str
    description: str
    action: Callable
    validation_rules: List[Dict[str, Any]]
    dependencies: List[str] = field(default_factory=list)
    timeout: int = 300  # seconds
    retry_count: int = 3


@dataclass
class WorkflowExecution:
    """Workflow execution instance"""

    id: str
    workflow_type: WorkflowType
    target_files: List[str]
    parameters: Dict[str, Any]
    state: WorkflowState
    start_time: str
    end_time: Optional[str] = None
    steps_completed: List[str] = field(default_factory=list)
    validation_results: Dict[str, Any] = field(default_factory=dict)
    error_log: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
