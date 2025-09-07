#!/usr/bin/env python3
"""
OSRS Skills Module - Agent Cellphone V2
======================================

OSRS skill training systems.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .base_trainer import OSRSSkillTrainer
from .woodcutting_trainer import OSRSWoodcuttingTrainer
from .fishing_trainer import OSRSFishingTrainer
from .combat_trainer import OSRSCombatTrainer

__all__ = [
    'OSRSSkillTrainer',
    'OSRSWoodcuttingTrainer',
    'OSRSFishingTrainer',
    'OSRSCombatTrainer'
]
