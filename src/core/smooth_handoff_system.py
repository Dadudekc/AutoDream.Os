"""Backward compatible imports for the smooth handoff system.

The original implementation lived in this module. It now proxies all
public interfaces to the :mod:`smooth_handoff` package where the code is
organized into smaller, single-responsibility modules.
"""

from .smooth_handoff import (
    HandoffStatus,
    HandoffType,
    HandoffContext,
    HandoffProcedure,
    HandoffExecution,
    SmoothHandoffSystem,
    get_smooth_handoff_system,
)

__all__ = [
    "HandoffStatus",
    "HandoffType",
    "HandoffContext",
    "HandoffProcedure",
    "HandoffExecution",
    "SmoothHandoffSystem",
    "get_smooth_handoff_system",
]
