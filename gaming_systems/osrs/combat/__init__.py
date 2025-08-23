#!/usr/bin/env python3
"""
OSRS Combat Module - Agent Cellphone V2
======================================

OSRS combat systems and mechanics.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .combat_system import OSRSCombatSystem
from .npc_interaction import OSRSNPCInteraction

__all__ = [
    'OSRSCombatSystem',
    'OSRSNPCInteraction'
]
