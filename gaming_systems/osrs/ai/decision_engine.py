#!/usr/bin/env python3
"""
OSRS Decision Engine - Agent Cellphone V2
========================================

OSRS AI decision making and strategy system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from ..core.enums import OSRSSkill, OSRSLocation, OSRSGameState
from ..core.data_models import OSRSPlayerStats


class DecisionType(Enum):
    """Types of AI decisions"""
    SKILL_TRAINING = "skill_training"
    COMBAT = "combat"
    QUESTING = "questing"
    TRADING = "trading"
    EXPLORATION = "exploration"
    REST = "rest"


class DecisionPriority(Enum):
    """Decision priority levels"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINIMAL = 1


@dataclass
class DecisionContext:
    """Context for decision making"""
    player_stats: OSRSPlayerStats
    current_location: OSRSLocation
    game_state: OSRSGameState
    available_resources: List[str]
    current_goals: List[str]
    time_of_day: float
    energy_level: int


@dataclass
class Decision:
    """AI decision result"""
    decision_type: DecisionType
    priority: DecisionPriority
    target_location: OSRSLocation
    action_description: str
    expected_duration: int
    confidence: float
    reasoning: str


class OSRSDecisionEngine:
    """OSRS AI decision making engine"""
    
    def __init__(self):
        self.decision_history: List[Decision] = []
        self.current_goals: List[str] = []
        self.personality_traits: Dict[str, float] = {
            "risk_tolerance": 0.5,
            "efficiency_focus": 0.8,
            "exploration_desire": 0.6,
            "social_interaction": 0.4
        }
        self._initialize_decision_rules()
    
    def _initialize_decision_rules(self):
        """Initialize decision making rules"""
        self.skill_priorities = {
            OSRSSkill.ATTACK: 0.9,
            OSRSSkill.STRENGTH: 0.9,
            OSRSSkill.DEFENCE: 0.8,
            OSRSSkill.HITPOINTS: 0.7,
            OSRSSkill.WOODCUTTING: 0.6,
            OSRSSkill.FISHING: 0.5,
            OSRSSkill.MINING: 0.6,
            OSRSSkill.CRAFTING: 0.4
        }
        
        self.location_preferences = {
            OSRSLocation.LUMBRIDGE: 0.8,
            OSRSLocation.VARROCK: 0.9,
            OSRSLocation.FALADOR: 0.7,
            OSRSLocation.AL_KHARID: 0.6,
            OSRSLocation.DRAYNOR: 0.5
        }
    
    def analyze_situation(self, context: DecisionContext) -> Decision:
        """Analyze current situation and make decision"""
        # Evaluate different decision types
        decisions = []
        
        # Skill training decision
        skill_decision = self._evaluate_skill_training(context)
        if skill_decision:
            decisions.append(skill_decision)
        
        # Combat decision
        combat_decision = self._evaluate_combat(context)
        if combat_decision:
            decisions.append(combat_decision)
        
        # Questing decision
        quest_decision = self._evaluate_questing(context)
        if quest_decision:
            decisions.append(quest_decision)
        
        # Trading decision
        trade_decision = self._evaluate_trading(context)
        if trade_decision:
            decisions.append(trade_decision)
        
        # Select best decision
        if not decisions:
            return self._create_rest_decision(context)
        
        best_decision = max(decisions, key=lambda d: d.priority.value * d.confidence)
        self.decision_history.append(best_decision)
        
        return best_decision
    
    def _evaluate_skill_training(self, context: DecisionContext) -> Optional[Decision]:
        """Evaluate skill training opportunities"""
        if context.game_state != OSRSGameState.IDLE:
            return None
        
        # Find best skill to train
        best_skill = None
        best_priority = 0
        
        for skill, priority in self.skill_priorities.items():
            current_level = context.player_stats.get_skill_level(skill)
            if current_level < 99:  # Not maxed
                skill_priority = priority * (99 - current_level) / 99
                if skill_priority > best_priority:
                    best_priority = skill_priority
                    best_skill = skill
        
        if not best_skill:
            return None
        
        # Find best location for training
        best_location = self._find_best_training_location(best_skill, context)
        
        return Decision(
            decision_type=DecisionType.SKILL_TRAINING,
            priority=DecisionPriority.HIGH if best_priority > 0.7 else DecisionPriority.MEDIUM,
            target_location=best_location,
            action_description=f"Train {best_skill.value} at {best_location.value}",
            expected_duration=1800,  # 30 minutes
            confidence=best_priority,
            reasoning=f"Skill {best_skill.value} needs training, best location is {best_location.value}"
        )
    
    def _evaluate_combat(self, context: DecisionContext) -> Optional[Decision]:
        """Evaluate combat opportunities"""
        if context.game_state != OSRSGameState.IDLE:
            return None
        
        # Check if player needs combat training
        combat_skills = [OSRSSkill.ATTACK, OSRSSkill.STRENGTH, OSRSSkill.DEFENCE]
        combat_levels = [context.player_stats.get_skill_level(skill) for skill in combat_skills]
        avg_combat_level = sum(combat_levels) / len(combat_levels)
        
        if avg_combat_level < 50:  # Low combat level
            best_location = self._find_best_combat_location(context)
            
            return Decision(
                decision_type=DecisionType.COMBAT,
                priority=DecisionPriority.HIGH,
                target_location=best_location,
                action_description=f"Train combat at {best_location.value}",
                expected_duration=3600,  # 1 hour
                confidence=0.8,
                reasoning=f"Combat level {avg_combat_level:.1f} is low, need training"
            )
        
        return None
    
    def _evaluate_questing(self, context: DecisionContext) -> Optional[Decision]:
        """Evaluate questing opportunities"""
        if context.game_state != OSRSGameState.IDLE:
            return None
        
        # Simple quest evaluation (in real system, would check quest log)
        if context.player_stats.get_skill_level(OSRSSkill.ATTACK) > 30:
            return Decision(
                decision_type=DecisionType.QUESTING,
                priority=DecisionPriority.MEDIUM,
                target_location=OSRSLocation.VARROCK,
                action_description="Complete available quests in Varrock",
                expected_duration=2700,  # 45 minutes
                confidence=0.6,
                reasoning="Player has sufficient combat level for quests"
            )
        
        return None
    
    def _evaluate_trading(self, context: DecisionContext) -> Optional[Decision]:
        """Evaluate trading opportunities"""
        if context.game_state != OSRSGameState.IDLE:
            return None
        
        # Check if player has items to sell or needs to buy
        if "dragon_bones" in context.available_resources:
            return Decision(
                decision_type=DecisionType.TRADING,
                priority=DecisionPriority.MEDIUM,
                target_location=OSRSLocation.VARROCK,
                action_description="Sell dragon bones at Grand Exchange",
                expected_duration=900,  # 15 minutes
                confidence=0.7,
                reasoning="Player has valuable items to sell"
            )
        
        return None
    
    def _find_best_training_location(self, skill: OSRSSkill, context: DecisionContext) -> OSRSLocation:
        """Find best location for training a skill"""
        # Simple location selection based on skill
        if skill in [OSRSSkill.ATTACK, OSRSSkill.STRENGTH, OSRSSkill.DEFENCE]:
            return OSRSLocation.LUMBRIDGE
        elif skill == OSRSSkill.WOODCUTTING:
            return OSRSLocation.DRAYNOR
        elif skill == OSRSSkill.FISHING:
            return OSRSLocation.LUMBRIDGE
        else:
            return OSRSLocation.VARROCK
    
    def _find_best_combat_location(self, context: DecisionContext) -> OSRSLocation:
        """Find best location for combat training"""
        combat_level = context.player_stats.get_skill_level(OSRSSkill.ATTACK)
        
        if combat_level < 20:
            return OSRSLocation.LUMBRIDGE
        elif combat_level < 40:
            return OSRSLocation.VARROCK
        else:
            return OSRSLocation.FALADOR
    
    def _create_rest_decision(self, context: DecisionContext) -> Decision:
        """Create a rest decision when no other options available"""
        return Decision(
            decision_type=DecisionType.REST,
            priority=DecisionPriority.MINIMAL,
            target_location=context.current_location,
            action_description="Rest and wait for opportunities",
            expected_duration=300,  # 5 minutes
            confidence=1.0,
            reasoning="No immediate actions available, resting"
        )
    
    def update_personality(self, trait: str, value: float):
        """Update personality trait"""
        if trait in self.personality_traits:
            self.personality_traits[trait] = max(0.0, min(1.0, value))
    
    def get_decision_history(self, limit: int = 10) -> List[Decision]:
        """Get recent decision history"""
        return self.decision_history[-limit:]
    
    def get_decision_statistics(self) -> Dict[str, Any]:
        """Get decision making statistics"""
        if not self.decision_history:
            return {}
        
        decision_types = [d.decision_type.value for d in self.decision_history]
        priorities = [d.priority.value for d in self.decision_history]
        confidences = [d.confidence for d in self.decision_history]
        
        return {
            "total_decisions": len(self.decision_history),
            "most_common_decision": max(set(decision_types), key=decision_types.count),
            "average_priority": sum(priorities) / len(priorities),
            "average_confidence": sum(confidences) / len(confidences),
            "personality_traits": self.personality_traits.copy()
        }
