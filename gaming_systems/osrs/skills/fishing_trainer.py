#!/usr/bin/env python3
"""
OSRS Fishing Trainer - Agent Cellphone V2
========================================

Fishing skill training implementation.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import List, Dict, Optional
from datetime import datetime

from ..core.enums import OSRSSkill, OSRSLocation
from ..core.data_models import OSRSResourceSpot
from .base_trainer import OSRSSkillTrainer

logger = logging.getLogger(__name__)


class OSRSFishingTrainer(OSRSSkillTrainer):
    """
    Fishing skill trainer.
    
    Single responsibility: Fishing training operations only.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """
    
    def __init__(self, player_stats):
        """Initialize fishing trainer"""
        super().__init__(OSRSSkill.FISHING, player_stats)
        self.current_spot: Optional[OSRSResourceSpot] = None
        self.available_spots: Dict[str, OSRSResourceSpot] = self._initialize_fishing_spots()
        self.inventory_slots = 28
        self.current_fish = 0
        self.fishing_rod_equipped = True
        
        logger.info(f"Initialized fishing trainer for {player_stats.username}")
    
    def _initialize_fishing_spots(self) -> Dict[str, OSRSResourceSpot]:
        """Initialize available fishing spots"""
        from ..core.data_models import OSRSResourceSpot
        
        spots = {
            "shrimp": OSRSResourceSpot(
                spot_id="fishing_shrimp",
                name="Shrimp Spot",
                location=OSRSLocation.LUMBRIDGE,
                resource_type="shrimp",
                skill_required=OSRSSkill.FISHING,
                level_required=1,
                respawn_time=15
            ),
            "anchovy": OSRSResourceSpot(
                spot_id="fishing_anchovy",
                name="Anchovy Spot",
                location=OSRSLocation.LUMBRIDGE,
                resource_type="anchovy",
                skill_required=OSRSSkill.FISHING,
                level_required=15,
                respawn_time=20
            ),
            "trout": OSRSResourceSpot(
                spot_id="fishing_trout",
                name="Trout Spot",
                location=OSRSLocation.LUMBRIDGE,
                resource_type="trout",
                skill_required=OSRSSkill.FISHING,
                level_required=20,
                respawn_time=25
            ),
            "salmon": OSRSResourceSpot(
                spot_id="fishing_salmon",
                name="Salmon Spot",
                location=OSRSLocation.LUMBRIDGE,
                resource_type="salmon",
                skill_required=OSRSSkill.FISHING,
                level_required=30,
                respawn_time=30
            ),
            "tuna": OSRSResourceSpot(
                spot_id="fishing_tuna",
                name="Tuna Spot",
                location=OSRSLocation.CATHERBY,
                resource_type="tuna",
                skill_required=OSRSSkill.FISHING,
                level_required=35,
                respawn_time=35
            ),
            "lobster": OSRSResourceSpot(
                spot_id="fishing_lobster",
                name="Lobster Spot",
                location=OSRSLocation.CATHERBY,
                resource_type="lobster",
                skill_required=OSRSSkill.FISHING,
                level_required=40,
                respawn_time=40
            ),
            "swordfish": OSRSResourceSpot(
                spot_id="fishing_swordfish",
                name="Swordfish Spot",
                location=OSRSLocation.CATHERBY,
                resource_type="swordfish",
                skill_required=OSRSSkill.FISHING,
                level_required=50,
                respawn_time=45
            ),
            "monkfish": OSRSResourceSpot(
                spot_id="fishing_monkfish",
                name="Monkfish Spot",
                location=OSRSLocation.PISCATORIS,
                resource_type="monkfish",
                skill_required=OSRSSkill.FISHING,
                level_required=62,
                respawn_time=50
            ),
            "shark": OSRSResourceSpot(
                spot_id="fishing_shark",
                name="Shark Spot",
                location=OSRSLocation.CATHERBY,
                resource_type="shark",
                skill_required=OSRSSkill.FISHING,
                level_required=76,
                respawn_time=60
            )
        }
        
        return spots
    
    def can_train_at_location(self, location: OSRSLocation) -> bool:
        """Check if fishing can be trained at location"""
        # Check if any fishing spots are available at this location
        for spot in self.available_spots.values():
            if spot.location == location and spot.is_active:
                return True
        return False
    
    def get_training_locations(self) -> List[OSRSLocation]:
        """Get available fishing locations"""
        locations = set()
        for spot in self.available_spots.values():
            if spot.is_active:
                locations.add(spot.location)
        return list(locations)
    
    def start_training(self, location: OSRSLocation) -> bool:
        """Start fishing training at specified location"""
        if not self.can_train_at_location(location):
            self._log_training_action("start_training", False, f"No available spots at {location.value}")
            return False
        
        if not self.fishing_rod_equipped:
            self._log_training_action("start_training", False, "Fishing rod not equipped")
            return False
        
        self.current_location = location
        self.is_training = True
        self.training_start_time = datetime.now()
        self.actions_completed = 0
        self.experience_gained = 0
        
        self._log_training_action("start_training", True, f"Started at {location.value}")
        return True
    
    def stop_training(self) -> bool:
        """Stop current fishing session"""
        if not self.is_training:
            return False
        
        self.is_training = False
        self.current_spot = None
        self._log_training_action("stop_training", True, "Fishing session stopped")
        return True
    
    def perform_training_action(self) -> bool:
        """Perform a single fishing action"""
        if not self.is_training:
            return False
        
        # Find available fishing spot at current location
        spot = self._find_available_spot()
        if not spot:
            self._log_training_action("find_spot", False, "No available spots")
            return False
        
        # Check if inventory is full
        if self.current_fish >= self.inventory_slots:
            self._log_training_action("inventory_full", False, "Inventory is full")
            return False
        
        # Perform fishing
        success = self._fish_at_spot(spot)
        if success:
            self._update_training_stats(action_completed=True, xp_gained=self._get_xp_for_fish(spot))
            self.current_fish += 1
        
        return success
    
    def _find_available_spot(self) -> Optional[OSRSResourceSpot]:
        """Find an available fishing spot at current location"""
        for spot in self.available_spots.values():
            if (spot.location == self.current_location and 
                spot.is_active and 
                self._check_skill_requirements(spot.level_required)):
                return spot
        return None
    
    def _fish_at_spot(self, spot: OSRSResourceSpot) -> bool:
        """Fish at a specific spot"""
        try:
            # Simulate fishing action
            time.sleep(0.2)  # Simulate fishing time
            
            # Mark spot as harvested
            spot.harvest()
            self.current_spot = spot
            
            self._log_training_action("fish_spot", True, f"Caught fish at {spot.name}")
            return True
            
        except Exception as e:
            self._log_training_action("fish_spot", False, f"Error: {str(e)}")
            return False
    
    def _get_xp_for_fish(self, spot: OSRSResourceSpot) -> int:
        """Get experience gained for catching specific fish"""
        xp_map = {
            "Shrimp Spot": 10,
            "Anchovy Spot": 40,
            "Trout Spot": 50,
            "Salmon Spot": 70,
            "Tuna Spot": 100,
            "Lobster Spot": 90,
            "Swordfish Spot": 100,
            "Monkfish Spot": 120,
            "Shark Spot": 110
        }
        return xp_map.get(spot.name, 10)
    
    def get_available_spots(self) -> List[Dict]:
        """Get list of available fishing spots with requirements"""
        spots = []
        for spot in self.available_spots.values():
            spots.append({
                "name": spot.name,
                "location": spot.location.value,
                "level_required": spot.level_required,
                "xp_gained": self._get_xp_for_fish(spot),
                "can_fish": self._check_skill_requirements(spot.level_required),
                "is_active": spot.is_active
            })
        return spots
    
    def get_inventory_status(self) -> Dict:
        """Get current inventory status"""
        return {
            "current_fish": self.current_fish,
            "max_slots": self.inventory_slots,
            "available_slots": self.inventory_slots - self.current_fish,
            "is_full": self.current_fish >= self.inventory_slots
        }
    
    def equip_fishing_rod(self) -> bool:
        """Equip fishing rod"""
        self.fishing_rod_equipped = True
        self._log_training_action("equip_rod", True, "Fishing rod equipped")
        return True
    
    def unequip_fishing_rod(self) -> bool:
        """Unequip fishing rod"""
        self.fishing_rod_equipped = False
        self._log_training_action("unequip_rod", True, "Fishing rod unequipped")
        return True
