"""Utility classes and functions for the automated workflow orchestrator."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, List, Optional
import uuid


@dataclass
class WorkflowStep:
    """A single step in an automated workflow."""

    step_id: str
    name: str
    description: str
    action: Callable[[], Any]
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class WorkflowExecution:
    """Tracking information for a workflow run."""

    execution_id: str
    workflow_name: str
    steps: List[WorkflowStep] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    success_rate: float = 0.0


def generate_execution_id(prefix: str = "EXEC") -> str:
    """Generate a unique workflow execution identifier."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
