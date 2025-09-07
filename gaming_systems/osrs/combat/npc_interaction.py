#!/usr/bin/env python3
"""
OSRS NPC Interaction - Agent Cellphone V2
========================================

NPC interaction and dialogue systems.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..core.enums import OSRSLocation
from ..core.data_models import OSRSPlayerStats

logger = logging.getLogger(__name__)


class OSRSNPCInteraction:
    """
    OSRS NPC Interaction System.
    
    Single responsibility: NPC interaction operations only.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """
    
    def __init__(self, player_stats: OSRSPlayerStats):
        """Initialize NPC interaction system"""
        self.player_stats = player_stats
        self.current_npc = None
        self.interaction_history = []
        self.dialogue_options = {}
        
        logger.info(f"Initialized NPC interaction system for {player_stats.username}")
    
    def start_interaction(self, npc_name: str, npc_location: OSRSLocation) -> bool:
        """Start interaction with an NPC"""
        if self.current_npc:
            logger.warning("Already interacting with an NPC")
            return False
        
        self.current_npc = {
            "name": npc_name,
            "location": npc_location,
            "start_time": datetime.now(),
            "dialogue_state": "greeting"
        }
        
        self.interaction_history.append({
            "action": "start_interaction",
            "npc": npc_name,
            "timestamp": datetime.now()
        })
        
        logger.info(f"Started interaction with {npc_name} at {npc_location.value}")
        return True
    
    def end_interaction(self) -> bool:
        """End current NPC interaction"""
        if not self.current_npc:
            return False
        
        npc_name = self.current_npc["name"]
        self.current_npc = None
        
        self.interaction_history.append({
            "action": "end_interaction",
            "npc": npc_name,
            "timestamp": datetime.now()
        })
        
        logger.info(f"Ended interaction with {npc_name}")
        return True
    
    def get_dialogue_options(self) -> List[str]:
        """Get available dialogue options for current NPC"""
        if not self.current_npc:
            return []
        
        npc_name = self.current_npc["name"]
        state = self.current_npc["dialogue_state"]
        
        # Return dialogue options based on NPC and state
        options = self._get_npc_dialogue_options(npc_name, state)
        return options
    
    def select_dialogue_option(self, option_index: int) -> Dict:
        """Select a dialogue option"""
        if not self.current_npc:
            return {"success": False, "reason": "No active interaction"}
        
        options = self.get_dialogue_options()
        if option_index < 0 or option_index >= len(options):
            return {"success": False, "reason": "Invalid option index"}
        
        selected_option = options[option_index]
        response = self._process_dialogue_selection(selected_option)
        
        self.interaction_history.append({
            "action": "select_dialogue",
            "option": selected_option,
            "response": response,
            "timestamp": datetime.now()
        })
        
        return {
            "success": True,
            "option": selected_option,
            "response": response
        }
    
    def _get_npc_dialogue_options(self, npc_name: str, state: str) -> List[str]:
        """Get dialogue options for specific NPC and state"""
        # Simplified dialogue system
        if state == "greeting":
            return [
                "Hello, how are you?",
                "What can you tell me about this place?",
                "Do you have any quests?",
                "Goodbye"
            ]
        elif state == "quest":
            return [
                "Tell me more about the quest",
                "I'll help you",
                "Not interested",
                "Go back"
            ]
        else:
            return ["Go back"]
    
    def _process_dialogue_selection(self, option: str) -> str:
        """Process dialogue selection and return response"""
        if "Hello" in option:
            return "Hello there, adventurer! Welcome to our lands."
        elif "place" in option:
            return "This is a peaceful village where travelers rest and trade."
        elif "quest" in option:
            self.current_npc["dialogue_state"] = "quest"
            return "Ah yes! I do have a quest that needs a brave adventurer like yourself."
        elif "help" in option:
            return "Excellent! I need you to gather some herbs from the nearby forest."
        elif "not interested" in option:
            self.current_npc["dialogue_state"] = "greeting"
            return "Very well, perhaps another time then."
        elif "go back" in option:
            self.current_npc["dialogue_state"] = "greeting"
            return "Of course, what else would you like to know?"
        elif "goodbye" in option:
            return "Farewell, adventurer! May your journey be safe."
        else:
            return "I'm not sure I understand. Could you repeat that?"
    
    def get_interaction_status(self) -> Dict:
        """Get current interaction status"""
        if not self.current_npc:
            return {"status": "no_interaction"}
        
        duration = datetime.now() - self.current_npc["start_time"]
        
        return {
            "status": "interacting",
            "npc": self.current_npc["name"],
            "location": self.current_npc["location"].value,
            "dialogue_state": self.current_npc["dialogue_state"],
            "duration_seconds": int(duration.total_seconds())
        }
    
    def get_interaction_history(self) -> List[Dict]:
        """Get interaction history"""
        return self.interaction_history.copy()
    
    def clear_interaction_history(self):
        """Clear interaction history"""
        self.interaction_history.clear()
        logger.info("Interaction history cleared")
