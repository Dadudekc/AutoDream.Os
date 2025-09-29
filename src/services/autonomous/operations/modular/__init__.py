#!/usr/bin/env python3
"""
Autonomous Operations Modular - V2 Compliant
===========================================

Modular autonomous operations system.
V2 Compliance: ≤100 lines, single responsibility, KISS principle.
"""

from .core import AutonomousOperationsCore

# Legacy compatibility - maintain original class name
AutonomousOperations = AutonomousOperationsCore

__all__ = [
    "AutonomousOperationsCore",
    "AutonomousOperations"
]
