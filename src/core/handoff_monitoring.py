from typing import Dict, Optional
from .handoff_initiation import HandoffRecord


class HandoffMonitor:
    """Monitor active handoffs and provide status information."""
    def __init__(self, active_handoffs: Dict[str, HandoffRecord]):
        self.active_handoffs = active_handoffs

    def get_status(self, execution_id: str) -> Optional[str]:
        record = self.active_handoffs.get(execution_id)
        if record:
            return record.status
        return None
