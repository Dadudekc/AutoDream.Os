#!/usr/bin/env python3
"""
Agent Coordination Module - V2 Compliant
========================================

Modular agent coordination system for Discord bot.
V2 Compliance: ≤100 lines, single responsibility, KISS principle.
"""

from .core import AgentCoordinationCore

# Legacy compatibility - maintain original class name
AgentCoordination = AgentCoordinationCore

__all__ = [
    "AgentCoordinationCore",
    "AgentCoordination"
]
