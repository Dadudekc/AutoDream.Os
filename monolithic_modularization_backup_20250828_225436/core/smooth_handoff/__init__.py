"""Smooth handoff workflow components.

This package hosts specialized modules for managing handoff execution including
initiation, monitoring, and completion utilities. The
:class:`~src.core.smooth_handoff.manager.SmoothHandoffManager` provides a thin
façade orchestrating these pieces.
"""

from .initiation import (
    HandoffContext as LegacyHandoffContext,
    HandoffRecord,
    HandoffInitiator,
)
from .monitoring import HandoffMonitor
from .completion import HandoffCompleter
from .manager import SmoothHandoffManager
from .models import (
    HandoffStatus,
    HandoffType,
    HandoffContext,
    HandoffProcedure,
    HandoffExecution,
)
from .system import SmoothHandoffSystem, get_smooth_handoff_system

__all__ = [
    "LegacyHandoffContext",
    "HandoffRecord",
    "HandoffInitiator",
    "HandoffMonitor",
    "HandoffCompleter",
    "SmoothHandoffManager",
    "HandoffStatus",
    "HandoffType",
    "HandoffContext",
    "HandoffProcedure",
    "HandoffExecution",
    "SmoothHandoffSystem",
    "get_smooth_handoff_system",
]
