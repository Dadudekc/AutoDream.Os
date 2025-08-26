#!/usr/bin/env python3
"""
Performance Connection Package - V2 Modular Architecture
=======================================================

Modular connection management system for performance management.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .connection_pool_manager import ConnectionPoolManager

__all__ = [
    "ConnectionPoolManager"
]
