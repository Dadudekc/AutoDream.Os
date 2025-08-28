"""Smooth handoff workflow components.

This package hosts specialized modules for managing handoff execution including
initiation, monitoring, and completion utilities. The
:class:`~src.core.smooth_handoff.manager.SmoothHandoffManager` provides a thin
façade orchestrating these pieces.
"""

from .initiation import HandoffContext, HandoffRecord, HandoffInitiator
from .monitoring import HandoffMonitor
from .completion import HandoffCompleter
from .manager import SmoothHandoffManager

__all__ = [
    "HandoffContext",
    "HandoffRecord",
    "HandoffInitiator",
    "HandoffMonitor",
    "HandoffCompleter",
    "SmoothHandoffManager",
]
