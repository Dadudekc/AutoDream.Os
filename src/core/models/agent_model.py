"""Data model describing an AI agent."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .model_utils import AgentType


@dataclass
class AIAgent:
    """Representation of an AI agent with its capabilities."""

    agent_id: str
    name: str
    agent_type: AgentType
    skills: List[str]
    workload_capacity: int
    current_workload: int = 0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Normalise enum values."""
        if isinstance(self.agent_type, str):
            self.agent_type = AgentType(self.agent_type)
