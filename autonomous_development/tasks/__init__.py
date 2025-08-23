#!/usr/bin/env python3
"""
Autonomous Development Tasks - Agent Cellphone V2
===============================================

Task management and registry systems.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .task_manager import TaskManager
from .task_registry import TaskRegistry

__all__ = [
    'TaskManager',
    'TaskRegistry'
]
