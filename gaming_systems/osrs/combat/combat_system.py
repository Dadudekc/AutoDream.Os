#!/usr/bin/env python3
"""
OSRS Combat System - Agent Cellphone V2
======================================

Core combat mechanics and calculations.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time
import logging
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from ..core.enums import OSRSSkill, OSRSLocation
from ..core.data_models import OSRSPlayerStats

logger = logging.getLogger(__name__)


class OSRSCombatSystem:
    """
    OSRS Combat System.
    
    Single responsibility: Combat mechanics and calculations only.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """
    
    def __init__(self, player_stats: OSRSPlayerStats):
        """Initialize combat system"""
        self.player_stats = player_stats
        self.combat_level = self._calculate_combat_level()
        self.current_target = None
        self.is_in_combat = False
        self.combat_start_time = None
        self.last_attack_time = None
        self.attack_speed = 4  # ticks between attacks
        self.auto_retaliate = True
        
        logger.info(f"Initialized combat system for {player_stats.username}")
    
    def _calculate_combat_level(self) -> int:
        """Calculate player combat level"""
        attack = self.player_stats.get_skill_level(OSRSSkill.ATTACK)
        strength = self.player_stats.get_skill_level(OSRSSkill.STRENGTH)
        defence = self.player_stats.get_skill_level(OSRSSkill.DEFENCE)
        hitpoints = self.player_stats.get_skill_level(OSRSSkill.HITPOINTS)
        prayer = self.player_stats.get_skill_level(OSRSSkill.PRAYER)
        magic = self.player_stats.get_skill_level(OSRSSkill.MAGIC)
        ranged = self.player_stats.get_skill_level(OSRSSkill.RANGED)
        
        # OSRS combat level formula
        melee = (attack + strength) * 0.325
        ranged = ranged * 0.325
        magic = magic * 0.325
        
        highest = max(melee, ranged, magic)
        combat_level = int(highest + defence * 0.25 + hitpoints * 0.25 + prayer * 0.125)
        
        return max(3, combat_level)
    
    def start_combat(self, target_name: str, target_level: int) -> bool:
        """Start combat with a target"""
        if self.is_in_combat:
            logger.warning("Already in combat")
            return False
        
        self.current_target = {
            "name": target_name,
            "level": target_level,
            "hp": self._calculate_target_hp(target_level),
            "max_hp": self._calculate_target_hp(target_level)
        }
        
        self.is_in_combat = True
        self.combat_start_time = datetime.now()
        self.last_attack_time = datetime.now()
        
        logger.info(f"Started combat with {target_name} (Level {target_level})")
        return True
    
    def stop_combat(self) -> bool:
        """Stop current combat"""
        if not self.is_in_combat:
            return False
        
        self.is_in_combat = False
        self.current_target = None
        self.combat_start_time = None
        self.last_attack_time = None
        
        logger.info("Combat stopped")
        return True
    
    def perform_attack(self) -> Dict:
        """Perform a single attack"""
        if not self.is_in_combat or not self.current_target:
            return {"success": False, "reason": "Not in combat"}
        
        # Check attack timing
        if not self._can_attack():
            return {"success": False, "reason": "Attack on cooldown"}
        
        # Calculate attack roll
        attack_roll = self._calculate_attack_roll()
        defence_roll = self._calculate_defence_roll()
        
        # Determine hit
        if attack_roll > defence_roll:
            damage = self._calculate_damage()
            self.current_target["hp"] = max(0, self.current_target["hp"] - damage)
            
            # Update attack time
            self.last_attack_time = datetime.now()
            
            result = {
                "success": True,
                "hit": True,
                "damage": damage,
                "target_hp": self.current_target["hp"],
                "target_dead": self.current_target["hp"] <= 0
            }
            
            if result["target_dead"]:
                self._handle_target_death()
            
            return result
        else:
            self.last_attack_time = datetime.now()
            return {
                "success": True,
                "hit": False,
                "damage": 0,
                "target_hp": self.current_target["hp"]
            }
    
    def _can_attack(self) -> bool:
        """Check if player can attack"""
        if not self.last_attack_time:
            return True
        
        time_since_last = (datetime.now() - self.last_attack_time).total_seconds()
        return time_since_last >= (self.attack_speed * 0.6)  # Convert ticks to seconds
    
    def _calculate_attack_roll(self) -> int:
        """Calculate attack roll"""
        attack_level = self.player_stats.get_skill_level(OSRSSkill.ATTACK)
        strength_level = self.player_stats.get_skill_level(OSRSSkill.STRENGTH)
        
        # Simplified attack roll calculation
        base_roll = attack_level * 8 + strength_level * 4
        random_factor = random.randint(1, 100)
        
        return base_roll + random_factor
    
    def _calculate_defence_roll(self) -> int:
        """Calculate defence roll for target"""
        target_level = self.current_target["level"]
        
        # Simplified defence roll calculation
        base_roll = target_level * 10
        random_factor = random.randint(1, 100)
        
        return base_roll + random_factor
    
    def _calculate_damage(self) -> int:
        """Calculate damage dealt"""
        strength_level = self.player_stats.get_skill_level(OSRSSkill.STRENGTH)
        
        # Simplified damage calculation
        base_damage = strength_level * 2
        random_factor = random.randint(1, 20)
        
        return max(1, base_damage + random_factor)
    
    def _calculate_target_hp(self, target_level: int) -> int:
        """Calculate target HP based on level"""
        # Simplified HP calculation
        return max(10, target_level * 5)
    
    def _handle_target_death(self):
        """Handle target death"""
        if not self.current_target:
            return
        
        # Award experience
        target_level = self.current_target["level"]
        xp_gained = target_level * 4
        
        # Update player stats
        self.player_stats.update_skill(OSRSSkill.ATTACK, 
                                     self.player_stats.get_skill_level(OSRSSkill.ATTACK),
                                     self.player_stats.get_skill_experience(OSRSSkill.ATTACK) + xp_gained)
        
        self.player_stats.update_skill(OSRSSkill.STRENGTH,
                                     self.player_stats.get_skill_level(OSRSSkill.STRENGTH),
                                     self.player_stats.get_skill_experience(OSRSSkill.STRENGTH) + xp_gained)
        
        self.player_stats.update_skill(OSRSSkill.DEFENCE,
                                     self.player_stats.get_skill_level(OSRSSkill.DEFENCE),
                                     self.player_stats.get_skill_experience(OSRSSkill.DEFENCE) + xp_gained)
        
        self.player_stats.update_skill(OSRSSkill.HITPOINTS,
                                     self.player_stats.get_skill_level(OSRSSkill.HITPOINTS),
                                     self.player_stats.get_skill_experience(OSRSSkill.HITPOINTS) + xp_gained)
        
        logger.info(f"Target defeated! Gained {xp_gained} XP")
    
    def get_combat_status(self) -> Dict:
        """Get current combat status"""
        if not self.is_in_combat:
            return {"status": "not_in_combat"}
        
        duration = datetime.now() - self.combat_start_time if self.combat_start_time else 0
        
        return {
            "status": "in_combat",
            "target": self.current_target,
            "combat_duration": int(duration.total_seconds()) if duration else 0,
            "combat_level": self.combat_level,
            "attack_speed": self.attack_speed,
            "auto_retaliate": self.auto_retaliate
        }
    
    def set_attack_speed(self, speed: int) -> bool:
        """Set attack speed in ticks"""
        if speed < 1 or speed > 10:
            return False
        
        self.attack_speed = speed
        logger.info(f"Attack speed set to {speed} ticks")
        return True
    
    def toggle_auto_retaliate(self) -> bool:
        """Toggle auto retaliate"""
        self.auto_retaliate = not self.auto_retaliate
        logger.info(f"Auto retaliate: {'ON' if self.auto_retaliate else 'OFF'}")
        return True
