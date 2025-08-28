from typing import Dict, List, Optional

from .handoff_initiation import HandoffInitiator, HandoffContext, HandoffRecord
from .handoff_monitoring import HandoffMonitor
from .handoff_completion import HandoffCompleter


class SmoothHandoffManager:
    """Coordinate handoff initiation, monitoring, and completion."""
    def __init__(self):
        self.active_handoffs: Dict[str, HandoffRecord] = {}
        self.handoff_history: List[HandoffRecord] = []
        self.initiator = HandoffInitiator(self.active_handoffs)
        self.monitor = HandoffMonitor(self.active_handoffs)
        self.completer = HandoffCompleter(self.active_handoffs, self.handoff_history)

    def initiate_handoff(self, context: HandoffContext) -> str:
        return self.initiator.initiate(context)

    def get_handoff_status(self, execution_id: str) -> Optional[str]:
        return self.monitor.get_status(execution_id)

    def complete_handoff(self, execution_id: str, success: bool = True) -> bool:
        return self.completer.complete(execution_id, success)
