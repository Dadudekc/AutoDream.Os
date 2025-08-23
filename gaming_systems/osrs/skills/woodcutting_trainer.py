#!/usr/bin/env python3
"""
OSRS Woodcutting Trainer - Agent Cellphone V2
============================================

Woodcutting skill training implementation.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time
import logging
from typing import List, Dict, Optional
from datetime import datetime

from ..core.enums import OSRSSkill, OSRSLocation
from ..core.data_models import OSRSResourceSpot
from .base_trainer import OSRSSkillTrainer

logger = logging.getLogger(__name__)


class OSRSWoodcuttingTrainer(OSRSSkillTrainer):
    """
    Woodcutting skill trainer.
    
    Single responsibility: Woodcutting training operations only.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """
    
    def __init__(self, player_stats):
        """Initialize woodcutting trainer"""
        super().__init__(OSRSSkill.WOODCUTTING, player_stats)
        self.current_tree: Optional[OSRSResourceSpot] = None
        self.available_trees: Dict[str, OSRSResourceSpot] = self._initialize_trees()
        self.inventory_slots = 28
        self.current_logs = 0
        
        logger.info(f"Initialized woodcutting trainer for {player_stats.username}")
    
    def _initialize_trees(self) -> Dict[str, OSRSResourceSpot]:
        """Initialize available woodcutting trees"""
        from ..core.data_models import OSRSResourceSpot
        
        trees = {
            "regular": OSRSResourceSpot(
                spot_id="tree_regular",
                name="Regular Tree",
                location=OSRSLocation.LUMBRIDGE,
                resource_type="wood",
                skill_required=OSRSSkill.WOODCUTTING,
                level_required=1,
                respawn_time=30
            ),
            "oak": OSRSResourceSpot(
                spot_id="tree_oak",
                name="Oak Tree",
                location=OSRSLocation.VARROCK,
                resource_type="oak_logs",
                skill_required=OSRSSkill.WOODCUTTING,
                level_required=15,
                respawn_time=45
            ),
            "willow": OSRSResourceSpot(
                spot_id="tree_willow",
                name="Willow Tree",
                location=OSRSLocation.DRAYNOR,
                resource_type="willow_logs",
                skill_required=OSRSSkill.WOODCUTTING,
                level_required=30,
                respawn_time=60
            ),
            "maple": OSRSResourceSpot(
                spot_id="tree_maple",
                name="Maple Tree",
                location=OSRSLocation.SEERS_VILLAGE,
                resource_type="maple_logs",
                skill_required=OSRSSkill.WOODCUTTING,
                level_required=45,
                respawn_time=90
            ),
            "yew": OSRSResourceSpot(
                spot_id="tree_yew",
                name="Yew Tree",
                location=OSRSLocation.VARROCK,
                resource_type="yew_logs",
                skill_required=OSRSSkill.WOODCUTTING,
                level_required=60,
                respawn_time=120
            ),
            "magic": OSRSResourceSpot(
                spot_id="tree_magic",
                name="Magic Tree",
                location=OSRSLocation.SEERS_VILLAGE,
                resource_type="magic_logs",
                skill_required=OSRSSkill.WOODCUTTING,
                level_required=75,
                respawn_time=180
            )
        }
        
        return trees
    
    def can_train_at_location(self, location: OSRSLocation) -> bool:
        """Check if woodcutting can be trained at location"""
        # Check if any trees are available at this location
        for tree in self.available_trees.values():
            if tree.location == location and tree.is_active:
                return True
        return False
    
    def get_training_locations(self) -> List[OSRSLocation]:
        """Get available woodcutting locations"""
        locations = set()
        for tree in self.available_trees.values():
            if tree.is_active:
                locations.add(tree.location)
        return list(locations)
    
    def start_training(self, location: OSRSLocation) -> bool:
        """Start woodcutting training at specified location"""
        if not self.can_train_at_location(location):
            self._log_training_action("start_training", False, f"No available trees at {location.value}")
            return False
        
        self.current_location = location
        self.is_training = True
        self.training_start_time = datetime.now()
        self.actions_completed = 0
        self.experience_gained = 0
        
        self._log_training_action("start_training", True, f"Started at {location.value}")
        return True
    
    def stop_training(self) -> bool:
        """Stop current woodcutting session"""
        if not self.is_training:
            return False
        
        self.is_training = False
        self.current_tree = None
        self._log_training_action("stop_training", True, "Training session stopped")
        return True
    
    def perform_training_action(self) -> bool:
        """Perform a single woodcutting action"""
        if not self.is_training:
            return False
        
        # Find available tree at current location
        tree = self._find_available_tree()
        if not tree:
            self._log_training_action("find_tree", False, "No available trees")
            return False
        
        # Check if inventory is full
        if self.current_logs >= self.inventory_slots:
            self._log_training_action("inventory_full", False, "Inventory is full")
            return False
        
        # Perform woodcutting
        success = self._chop_tree(tree)
        if success:
            self._update_training_stats(action_completed=True, xp_gained=self._get_xp_for_tree(tree))
            self.current_logs += 1
        
        return success
    
    def _find_available_tree(self) -> Optional[OSRSResourceSpot]:
        """Find an available tree at current location"""
        for tree in self.available_trees.values():
            if (tree.location == self.current_location and 
                tree.is_active and 
                self._check_skill_requirements(tree.level_required)):
                return tree
        return None
    
    def _chop_tree(self, tree: OSRSResourceSpot) -> bool:
        """Chop down a specific tree"""
        try:
            # Simulate woodcutting action
            time.sleep(0.1)  # Simulate chopping time
            
            # Mark tree as harvested
            tree.harvest()
            self.current_tree = tree
            
            self._log_training_action("chop_tree", True, f"Chopped {tree.name}")
            return True
            
        except Exception as e:
            self._log_training_action("chop_tree", False, f"Error: {str(e)}")
            return False
    
    def _get_xp_for_tree(self, tree: OSRSResourceSpot) -> int:
        """Get experience gained for chopping specific tree"""
        xp_map = {
            "Regular Tree": 25,
            "Oak Tree": 37,
            "Willow Tree": 67,
            "Maple Tree": 100,
            "Yew Tree": 175,
            "Magic Tree": 250
        }
        return xp_map.get(tree.name, 25)
    
    def get_available_trees(self) -> List[Dict]:
        """Get list of available trees with requirements"""
        trees = []
        for tree in self.available_trees.values():
            trees.append({
                "name": tree.name,
                "location": tree.location.value,
                "level_required": tree.level_required,
                "xp_gained": self._get_xp_for_tree(tree),
                "can_chop": self._check_skill_requirements(tree.level_required),
                "is_active": tree.is_active
            })
        return trees
    
    def get_inventory_status(self) -> Dict:
        """Get current inventory status"""
        return {
            "current_logs": self.current_logs,
            "max_slots": self.inventory_slots,
            "available_slots": self.inventory_slots - self.current_logs,
            "is_full": self.current_logs >= self.inventory_slots
        }
