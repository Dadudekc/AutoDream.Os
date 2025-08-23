#!/usr/bin/env python3
"""
Campaign Messaging - Agent Cellphone V2
======================================

Handles campaign messaging operations (election broadcasts, mass announcements).
Single responsibility: Campaign messaging only.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict

from .interfaces import ICampaignMessaging
from .coordinate_manager import CoordinateManager
from .pyautogui_messaging import PyAutoGUIMessaging

logger = logging.getLogger(__name__)


class CampaignMessaging(ICampaignMessaging):
    """
    Campaign Messaging - Single responsibility: Campaign messaging operations
    
    This class only handles:
    - Election broadcasts
    - Campaign announcements
    - Mass messaging campaigns
    """
    
    def __init__(self, coordinate_manager: CoordinateManager, pyautogui_messaging: PyAutoGUIMessaging):
        """Initialize campaign messaging with dependencies"""
        self.coordinate_manager = coordinate_manager
        self.pyautogui_messaging = pyautogui_messaging
        logger.info("Campaign Messaging initialized")
    
    def send_campaign_message(self, message_content: str, campaign_type: str = "election") -> Dict[str, bool]:
        """Send campaign message to all agents"""
        try:
            logger.info(f"Campaign message ({campaign_type}): {message_content[:50]}...")
            
            # Get all agents in 8-agent mode
            mode_agents = self.coordinate_manager.get_agents_in_mode("8-agent")
            messages = {agent_id: message_content for agent_id in mode_agents}
            
            # Use PyAutoGUI for campaign broadcasting
            results = self.pyautogui_messaging.send_bulk_messages(messages, "8-agent")
            
            logger.info(f"✅ Campaign message sent to {sum(results.values())}/{len(results)} agents")
            return results
            
        except Exception as e:
            logger.error(f"Error sending campaign message: {e}")
            return {}
    
    def send_election_broadcast(self, message_content: str) -> Dict[str, bool]:
        """Send election broadcast to all agents"""
        return self.send_campaign_message(message_content, "election")
    
    def send_campaign_update(self, message_content: str) -> Dict[str, bool]:
        """Send campaign update to all agents"""
        return self.send_campaign_message(message_content, "campaign_update")
    
    def send_voter_engagement(self, message_content: str) -> Dict[str, bool]:
        """Send voter engagement message to all agents"""
        return self.send_campaign_message(message_content, "voter_engagement")
