"""Shared orchestration dataclasses for AI/ML systems."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class OrchestrationTask:
    """AI/ML orchestration task representation."""

    task_id: str
    task_type: str
    priority: int
    data: Dict[str, Any]
    created_at: datetime
    status: str = "pending"
    assigned_agent: Optional[str] = None
    result: Optional[Any] = None


@dataclass
class SystemHealth:
    """AI/ML system health status."""

    overall_health: str
    models_health: str
    agents_health: str
    api_keys_health: str
    workflows_health: str
    last_check: datetime
    issues: List[str] = field(default_factory=list)
