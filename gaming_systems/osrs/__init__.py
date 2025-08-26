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
    OSRSMarketSystem
)

from .ai import (
    OSRSDecisionEngine,
    OSRSBehaviorTree,
    OSRSBehaviorNode,
    OSRSBehaviorNodeType,
    OSRSActionNode,
    OSRSConditionNode,
    OSRSSequenceNode,
    OSRSSelectorNode,
    OSRSDecoratorNode,
)

# Factory function for backward compatibility
def create_osrs_ai_agent(config: dict = None):
    """Create an OSRS AI agent instance for backward compatibility"""
    from .ai.decision_engine import OSRSDecisionEngine
    from .skills.woodcutting_trainer import OSRSWoodcuttingTrainer
    from .combat.combat_system import OSRSCombatSystem
    from .trading.market_system import OSRSMarketSystem
    from .core.data_models import OSRSPlayerStats
    
    # Create a player stats instance for the trainer
    player_stats = OSRSPlayerStats(
        player_id="ai_agent",
        username="osrs_ai_agent",
        combat_level=3,
        total_level=32
    )
    
    # Create a simple agent instance with the new modular components
    agent = {
        'decision_engine': OSRSDecisionEngine(),
        'skill_trainer': OSRSWoodcuttingTrainer(player_stats),
        'combat_system': OSRSCombatSystem(player_stats),
        'market_system': OSRSMarketSystem()
    }
    
    return agent

__all__ = [
    # Core enums and data models
    'OSRSSkill', 'OSRSLocation', 'OSRSGameState', 'OSRSActionType',
    'OSRSPlayerStats', 'OSRSInventoryItem', 'OSRSGameData', 'OSRSResourceSpot', 'OSRSRecipe',
    
    # Skill trainers
    'OSRSSkillTrainer', 'OSRSWoodcuttingTrainer', 'OSRSFishingTrainer', 'OSRSCombatTrainer',
    
    # Combat systems
    'OSRSCombatSystem', 'OSRSNPCInteraction',
    
    # Trading systems
    'OSRSMarketSystem',
    
    # AI systems
    'OSRSDecisionEngine',
    'OSRSBehaviorTree',
    'OSRSBehaviorNode',
    'OSRSBehaviorNodeType',
    'OSRSActionNode',
    'OSRSConditionNode',
    'OSRSSequenceNode',
    'OSRSSelectorNode',
    'OSRSDecoratorNode',
    
    # Factory function for backward compatibility
    'create_osrs_ai_agent'
]
