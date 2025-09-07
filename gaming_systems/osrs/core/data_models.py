#!/usr/bin/env python3
"""
OSRS Data Models - Agent Cellphone V2
=====================================

OSRS game data structures and models.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from .enums import OSRSSkill, OSRSLocation


@dataclass
class OSRSPlayerStats:
    """OSRS Player Statistics"""
    player_id: str
    username: str
    combat_level: int = 3
    total_level: int = 32
    experience: Dict[OSRSSkill, int] = field(default_factory=dict)
    skill_levels: Dict[OSRSSkill, int] = field(default_factory=dict)
    quest_points: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
    
    def get_skill_level(self, skill: OSRSSkill) -> int:
        """Get level for a specific skill"""
        return self.skill_levels.get(skill, 1)
    
    def get_skill_experience(self, skill: OSRSSkill) -> int:
        """Get experience for a specific skill"""
        return self.experience.get(skill, 0)
    
    def update_skill(self, skill: OSRSSkill, level: int, experience: int):
        """Update skill level and experience"""
        self.skill_levels[skill] = level
        self.experience[skill] = experience
        self.last_updated = datetime.now()


@dataclass
class OSRSInventoryItem:
    """OSRS Inventory Item"""
    item_id: int
    name: str
    quantity: int = 1
    stackable: bool = False
    tradeable: bool = True
    high_alch: int = 0
    low_alch: int = 0
    ge_price: int = 0
    item_type: str = "misc"
    requirements: Dict[str, int] = field(default_factory=dict)
    
    def is_stackable(self) -> bool:
        """Check if item is stackable"""
        return self.stackable
    
    def can_trade(self) -> bool:
        """Check if item can be traded"""
        return self.tradeable
    
    def get_total_value(self) -> int:
        """Get total value of item stack"""
        return self.ge_price * self.quantity


@dataclass
class OSRSGameData:
    """OSRS Game Data"""
    game_state: str = "idle"
    current_location: Optional[OSRSLocation] = None
    target_location: Optional[OSRSLocation] = None
    current_action: Optional[str] = None
    action_start_time: Optional[datetime] = None
    action_duration: Optional[int] = None
    last_action: Optional[str] = None
    last_action_time: Optional[datetime] = None
    
    def start_action(self, action: str, duration: Optional[int] = None):
        """Start a new action"""
        self.current_action = action
        self.action_start_time = datetime.now()
        self.action_duration = duration
        self.game_state = "active"
    
    def complete_action(self):
        """Complete current action"""
        if self.current_action:
            self.last_action = self.current_action
            self.last_action_time = datetime.now()
            self.current_action = None
            self.action_start_time = None
            self.action_duration = None
            self.game_state = "idle"


@dataclass
class OSRSResourceSpot:
    """OSRS Resource Spot"""
    spot_id: str
    name: str
    location: OSRSLocation
    resource_type: str
    skill_required: OSRSSkill
    level_required: int
    respawn_time: int = 0
    is_active: bool = True
    last_harvested: Optional[datetime] = None
    
    def can_harvest(self, player_level: int) -> bool:
        """Check if player can harvest this spot"""
        return player_level >= self.level_required and self.is_active
    
    def harvest(self):
        """Mark spot as harvested"""
        self.last_harvested = datetime.now()
        self.is_active = False
    
    def respawn(self):
        """Mark spot as respawned"""
        self.is_active = True


@dataclass
class OSRSRecipe:
    """OSRS Crafting Recipe"""
    recipe_id: str
    name: str
    skill_required: OSRSSkill
    level_required: int
    ingredients: Dict[str, int] = field(default_factory=dict)
    products: Dict[str, int] = field(default_factory=dict)
    experience_gained: int = 0
    category: str = "misc"
    
    def can_craft(self, player_level: int, inventory: Dict[str, int]) -> bool:
        """Check if player can craft this recipe"""
        if player_level < self.level_required:
            return False
        
        for ingredient, required_qty in self.ingredients.items():
            if inventory.get(ingredient, 0) < required_qty:
                return False
        
        return True
    
    def get_ingredient_cost(self, prices: Dict[str, int]) -> int:
        """Calculate total ingredient cost"""
        total_cost = 0
        for ingredient, qty in self.ingredients.items():
            total_cost += prices.get(ingredient, 0) * qty
        return total_cost
