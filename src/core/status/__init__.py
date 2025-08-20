#!/usr/bin/env python3
"""
Status Package - Agent Cellphone V2
===================================

Refactored live status system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

from .status_types import (
    UpdateFrequency,
    StatusEventType,
    StatusEvent,
    StatusMetrics,
    ActivitySummary
)

from .status_core import LiveStatusSystem

# Backward compatibility
__all__ = [
    'UpdateFrequency',
    'StatusEventType',
    'StatusEvent',
    'StatusMetrics',
    'ActivitySummary',
    'LiveStatusSystem'
]
