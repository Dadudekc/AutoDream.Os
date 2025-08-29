"""Handoff monitoring utilities.

Responsibilities:
- Track active handoff records.
- Provide status queries for executions.
"""

from typing import Dict, Optional
from .initiation import HandoffRecord


class HandoffMonitor:
    """Monitor active handoffs and provide status information."""
    def __init__(self, active_handoffs: Dict[str, HandoffRecord]):
        self.active_handoffs = active_handoffs

    def get_status(self, execution_id: str) -> Optional[str]:
        record = self.active_handoffs.get(execution_id)
        if record:
            return record.status
        return None
