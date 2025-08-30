#!/usr/bin/env python3
"""
YOLO Messaging - Agent Cellphone V2
===================================

Handles YOLO automatic activation and messaging operations.
Single responsibility: YOLO mode operations only.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict

from .interfaces import IYOLOMessaging
from .coordinate_manager import CoordinateManager
from .unified_pyautogui_messaging import UnifiedPyAutoGUIMessaging

logger = logging.getLogger(__name__)


class YOLOMessaging(IYOLOMessaging):
    """
    YOLO Messaging - Single responsibility: YOLO automatic activation operations
    
    This class only handles:
    - Automatic agent activation
    - YOLO mode messaging
    - FSM integration preparation
    """
    
    def __init__(self, coordinate_manager: CoordinateManager, pyautogui_messaging: UnifiedPyAutoGUIMessaging):
        """Initialize YOLO messaging with dependencies"""
        self.coordinate_manager = coordinate_manager
        self.pyautogui_messaging = pyautogui_messaging
        logger.info("YOLO Messaging initialized")
    
    def activate_yolo_mode(self, message_content: str) -> Dict[str, bool]:
        """YOLO mode: Activate and resume agents using FSM system"""
        try:
            logger.info("🚀 YOLO MODE ACTIVATED - Automatic agent activation and messaging")
            
            # Get all agents in 8-agent mode
            mode_agents = self.coordinate_manager.get_agents_in_mode("8-agent")
            results = {}
            
            for agent_id in mode_agents:
                logger.info(f"YOLO: Activating and messaging {agent_id}")
                
                # 1. Activate agent (click starter location)
                success = self.pyautogui_messaging.activate_agent(agent_id, "8-agent")
                
                if success:
                    # 2. Send message after activation
                    message_success = self.pyautogui_messaging.send_message(agent_id, message_content)
                    results[agent_id] = message_success
                    
                    logger.info(f"YOLO: {agent_id} {'✅ Activated and messaged' if message_success else '❌ Failed to message'}")
                else:
                    results[agent_id] = False
                    logger.error(f"YOLO: {agent_id} failed to activate")
                
                time.sleep(0.5)  # Delay between agents
            
            logger.info(f"🚀 YOLO MODE COMPLETE: {sum(results.values())}/{len(results)} agents processed")
            return results
            
        except Exception as e:
            logger.error(f"Error in YOLO mode: {e}")
            return {}
    
    def activate_single_agent_yolo(self, agent_id: str, message_content: str) -> bool:
        """Activate YOLO mode for a single agent"""
        try:
            logger.info(f"YOLO: Single agent activation for {agent_id}")
            
            # 1. Activate agent
            activation_success = self.pyautogui_messaging.activate_agent(agent_id, "8-agent")
            
            if activation_success:
                # 2. Send message
                message_success = self.pyautogui_messaging.send_message(agent_id, message_content)
                logger.info(f"YOLO: {agent_id} {'✅ Success' if message_success else '❌ Failed'}")
                return message_success
            else:
                logger.error(f"YOLO: {agent_id} activation failed")
                return False
                
        except Exception as e:
            logger.error(f"Error in single agent YOLO: {e}")
            return False
