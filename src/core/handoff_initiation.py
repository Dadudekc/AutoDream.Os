from dataclasses import dataclass, field
import time
from typing import Dict, Any, Optional

@dataclass
class HandoffContext:
    """Basic context information for a handoff operation."""
    handoff_id: str
    source: str
    target: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HandoffRecord:
    """Track the state of an active handoff."""
    execution_id: str
    context: HandoffContext
    status: str = "in_progress"
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    error: Optional[str] = None


class HandoffInitiator:
    """Handle creation of handoff executions."""
    def __init__(self, active_handoffs: Dict[str, HandoffRecord]):
        self.active_handoffs = active_handoffs

    def initiate(self, context: HandoffContext) -> str:
        """Create a new handoff execution and store it."""
        execution_id = f"handoff_{int(time.time()*1000)}_{context.handoff_id}"
        record = HandoffRecord(execution_id=execution_id, context=context)
        self.active_handoffs[execution_id] = record
        return execution_id
