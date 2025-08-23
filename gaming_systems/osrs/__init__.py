#!/usr/bin/env python3
"""
OSRS Module - Agent Cellphone V2
================================

Main OSRS gaming system module.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .core import (
    OSRSSkill, OSRSLocation, OSRSGameState, OSRSActionType,
    OSRSPlayerStats, OSRSInventoryItem, OSRSGameData, OSRSResourceSpot, OSRSRecipe
)

from .skills import (
    OSRSSkillTrainer, OSRSWoodcuttingTrainer, OSRSFishingTrainer, OSRSCombatTrainer
)

from .combat import (
    OSRSCombatSystem, OSRSNPCInteraction
)

from .trading import (
    OSRSMarketSystem, OSRSTradeManager, OSRSPriceTracker
)

from .ai import (
    OSRSDecisionEngine, OSRSTaskPlanner, OSRSBehaviorTree
)

__all__ = [
    # Core enums and data models
    'OSRSSkill', 'OSRSLocation', 'OSRSGameState', 'OSRSActionType',
    'OSRSPlayerStats', 'OSRSInventoryItem', 'OSRSGameData', 'OSRSResourceSpot', 'OSRSRecipe',
    
    # Skill trainers
    'OSRSSkillTrainer', 'OSRSWoodcuttingTrainer', 'OSRSFishingTrainer', 'OSRSCombatTrainer',
    
    # Combat systems
    'OSRSCombatSystem', 'OSRSNPCInteraction',
    
    # Trading systems
    'OSRSMarketSystem', 'OSRSTradeManager', 'OSRSPriceTracker',
    
    # AI systems
    'OSRSDecisionEngine', 'OSRSTaskPlanner', 'OSRSBehaviorTree'
]
