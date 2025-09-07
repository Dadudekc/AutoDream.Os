"""Handoff completion utilities.

Responsibilities:
- Finalize handoff executions.
- Persist completed records in history.
"""

import time
from typing import Dict, List
from .initiation import HandoffRecord


class HandoffCompleter:
    """Finalize handoffs and maintain history."""
    def __init__(self, active_handoffs: Dict[str, HandoffRecord], history: List[HandoffRecord]):
        self.active_handoffs = active_handoffs
        self.history = history

    def complete(self, execution_id: str, success: bool = True) -> bool:
        record = self.active_handoffs.get(execution_id)
        if not record:
            return False
        record.status = "completed" if success else "failed"
        record.end_time = time.time()
        self.history.append(record)
        del self.active_handoffs[execution_id]
        return True
