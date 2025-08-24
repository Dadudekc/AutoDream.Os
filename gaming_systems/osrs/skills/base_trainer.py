#!/usr/bin/env python3
"""
OSRS Base Skill Trainer - Agent Cellphone V2
===========================================

Base class for OSRS skill training.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

from ..core.enums import OSRSSkill, OSRSLocation
from ..core.data_models import OSRSPlayerStats, OSRSResourceSpot

logger = logging.getLogger(__name__)


class OSRSSkillTrainer(ABC):
    """
    Base class for OSRS skill training.
    
    Single responsibility: Skill training operations only.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """
    
    def __init__(self, skill: OSRSSkill, player_stats: OSRSPlayerStats):
        """Initialize skill trainer"""
        self.skill = skill
        self.player_stats = player_stats
        self.current_location: Optional[OSRSLocation] = None
        self.target_location: Optional[OSRSLocation] = None
        self.is_training = False
        self.training_start_time: Optional[datetime] = None
        self.last_action_time: Optional[datetime] = None
        self.actions_completed = 0
        self.experience_gained = 0
        
        logger.info(f"Initialized {skill.value} trainer for {player_stats.username}")
    
    @abstractmethod
    def can_train_at_location(self, location: OSRSLocation) -> bool:
        """Check if skill can be trained at location"""
        pass
    
    @abstractmethod
    def get_training_locations(self) -> List[OSRSLocation]:
        """Get available training locations for skill"""
        pass
    
    @abstractmethod
    def start_training(self, location: OSRSLocation) -> bool:
        """Start training at specified location"""
        pass
    
    @abstractmethod
    def stop_training(self) -> bool:
        """Stop current training session"""
        pass
    
    @abstractmethod
    def perform_training_action(self) -> bool:
        """Perform a single training action"""
        pass
    
    def get_training_progress(self) -> Dict[str, Any]:
        """Get current training progress"""
        if not self.is_training:
            return {"status": "not_training"}
        
        duration = datetime.now() - self.training_start_time if self.training_start_time else timedelta(0)
        
        return {
            "status": "training",
            "skill": self.skill.value,
            "location": self.current_location.value if self.current_location else None,
            "duration_seconds": int(duration.total_seconds()),
            "actions_completed": self.actions_completed,
            "experience_gained": self.experience_gained,
            "actions_per_hour": self._calculate_actions_per_hour(duration),
            "xp_per_hour": self._calculate_xp_per_hour(duration)
        }
    
    def _calculate_actions_per_hour(self, duration: timedelta) -> float:
        """Calculate actions per hour"""
        if duration.total_seconds() == 0:
            return 0.0
        
        hours = duration.total_seconds() / 3600
        return self.actions_completed / hours if hours > 0 else 0.0
    
    def _calculate_xp_per_hour(self, duration: timedelta) -> float:
        """Calculate experience per hour"""
        if duration.total_seconds() == 0:
            return 0.0
        
        hours = duration.total_seconds() / 3600
        return self.experience_gained / hours if hours > 0 else 0.0
    
    def _update_training_stats(self, action_completed: bool = True, xp_gained: int = 0):
        """Update training statistics"""
        if action_completed:
            self.actions_completed += 1
        
        if xp_gained > 0:
            self.experience_gained += xp_gained
            # Update player stats
            current_xp = self.player_stats.get_skill_experience(self.skill)
            self.player_stats.update_skill(self.skill, 
                                        self.player_stats.get_skill_level(self.skill),
                                        current_xp + xp_gained)
        
        self.last_action_time = datetime.now()
    
    def _check_skill_requirements(self, required_level: int) -> bool:
        """Check if player meets skill requirements"""
        current_level = self.player_stats.get_skill_level(self.skill)
        return current_level >= required_level
    
    def _log_training_action(self, action: str, success: bool, details: str = ""):
        """Log training action"""
        status = "✅" if success else "❌"
        logger.info(f"{status} {self.skill.value} training: {action} - {details}")
    
    def get_skill_info(self) -> Dict[str, Any]:
        """Get current skill information"""
        return {
            "skill": self.skill.value,
            "current_level": self.player_stats.get_skill_level(self.skill),
            "current_experience": self.player_stats.get_skill_experience(self.skill),
            "next_level_xp": self._get_next_level_xp(),
            "progress_to_next": self._get_progress_to_next_level()
        }
    
    def _get_next_level_xp(self) -> int:
        """Get experience required for next level"""
        current_level = self.player_stats.get_skill_level(self.skill)
        # Simplified XP calculation (OSRS uses complex formula)
        return int(current_level * 1000 * 1.5)
    
    def _get_progress_to_next_level(self) -> float:
        """Get progress to next level as percentage"""
        current_xp = self.player_stats.get_skill_experience(self.skill)
        next_level_xp = self._get_next_level_xp()
        
        if next_level_xp == 0:
            return 0.0
        
        return min(100.0, (current_xp / next_level_xp) * 100)
