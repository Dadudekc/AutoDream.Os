from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class SwarmStatus:
    """Represents the current swarm status."""

    active_agents: List[str] = field(default_factory=list)
    total_agents: int = 8
    current_cycle: int = 1
    active_missions: List[str] = field(default_factory=list)
    system_health: str = "HEALTHY"
    last_update: Optional[datetime] = None
    efficiency_rating: float = 8.0
    pending_tasks: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Initialize default values after dataclass creation."""
        if not self.active_agents:
            self.active_agents = [f"Agent-{i}" for i in range(1, 9)]
        if self.last_update is None:
            self.last_update = datetime.utcnow()
