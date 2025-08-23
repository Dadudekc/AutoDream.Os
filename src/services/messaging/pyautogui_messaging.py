#!/usr/bin/env python3
"""
PyAutoGUI Messaging - Agent Cellphone V2
========================================

Handles PyAutoGUI-based messaging operations.
Single responsibility: PyAutoGUI messaging only.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time
import logging
import pyautogui
import pyperclip
from typing import Dict, Optional

from .interfaces import IMessageSender, IBulkMessaging
from .coordinate_manager import CoordinateManager, AgentCoordinates

logger = logging.getLogger(__name__)


class PyAutoGUIMessaging(IMessageSender, IBulkMessaging):
    """
    PyAutoGUI Messaging - Single responsibility: PyAutoGUI messaging operations
    
    This class only handles:
    - Sending messages via PyAutoGUI
    - Bulk messaging operations
    - PyAutoGUI safety and configuration
    """
    
    def __init__(self, coordinate_manager: CoordinateManager):
        """Initialize PyAutoGUI messaging with coordinate manager"""
        self.coordinate_manager = coordinate_manager
        self._setup_pyautogui()
        logger.info("PyAutoGUI Messaging initialized")
    
    def _setup_pyautogui(self):
        """Setup PyAutoGUI safety and configuration"""
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        logger.info("PyAutoGUI configured with safety settings")
    
    def send_message(self, recipient: str, message_content: str, message_type: str = "text", new_chat: bool = False) -> bool:
        """
        Send message using PyAutoGUI (coordinate-based)
        
        Args:
            recipient: Agent ID to send message to
            message_content: Message content to send
            message_type: Type of message (text, onboarding_start, etc.)
            new_chat: Whether this is a new chat (onboarding) message
        """
        try:
            coords = self.coordinate_manager.get_agent_coordinates(recipient, "8-agent")
            if not coords:
                logger.error(f"No coordinates for {recipient}")
                return False
            
            if new_chat or message_type == "onboarding_start":
                # Use onboarding sequence: starter location → Ctrl+N → validate → paste
                return self._send_onboarding_message(recipient, message_content, coords)
            elif message_type == "high_priority":
                # Use high priority messaging: Ctrl+Enter 2x for urgent messages
                return self._send_high_priority_message(recipient, message_content, coords)
            else:
                # Use normal messaging: input box coordinates
                return self._send_normal_message(recipient, message_content, coords)
                
        except Exception as e:
            logger.error(f"Error sending PyAutoGUI message to {recipient}: {e}")
            return False
    
    def _send_onboarding_message(self, recipient: str, message_content: str, coords: AgentCoordinates) -> bool:
        """Send onboarding message using the proper sequence: starter → Ctrl+N → validate → paste"""
        try:
            starter_x, starter_y = coords.starter_location
            
            logger.info(f"🚀 Onboarding message to {recipient} at starter coordinates ({starter_x}, {starter_y})")
            
            # Step 1: Click starter location (first input box)
            pyautogui.moveTo(starter_x, starter_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            # Step 2: Press Ctrl+N to open new chat
            logger.info(f"📱 Opening new chat for {recipient} with Ctrl+N...")
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(1.0)  # Wait for new chat to open
            
            # Step 3: Click starter location again to validate focus
            pyautogui.moveTo(starter_x, starter_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.5)
            
            # Step 4: Prepare and paste onboarding message
            complete_message = f"{recipient}\n\n{message_content}"
            pyperclip.copy(complete_message)
            
            # Clear any existing text (Ctrl+A + Delete)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(0.2)
            
            # Paste the onboarding message (Ctrl+V)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            # Step 5: Send onboarding message (Enter)
            pyautogui.press('enter')
            time.sleep(0.5)
            
            logger.info(f"✅ Onboarding message sent to {recipient} via new chat")
            return True
            
        except Exception as e:
            logger.error(f"Error sending onboarding message to {recipient}: {e}")
            return False
    
    def _send_high_priority_message(self, recipient: str, message_content: str, coords: AgentCoordinates) -> bool:
        """Send high priority message using Ctrl+Enter 2x sequence for urgent communications"""
        try:
            input_x, input_y = coords.input_box
            
            logger.info(f"🚨 HIGH PRIORITY message to {recipient} at input coordinates ({input_x}, {input_y})")
            
            # Prepare complete message with agent name and HIGH PRIORITY indicator
            complete_message = f"🚨 HIGH PRIORITY: {recipient}\n\n{message_content}"
            
            # Copy complete message to clipboard
            pyperclip.copy(complete_message)
            
            # Click input box
            pyautogui.moveTo(input_x, input_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.3)
            
            # Clear existing text (Ctrl+A + Delete)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(0.2)
            
            # Paste the complete message (Ctrl+V)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            # HIGH PRIORITY: Press Ctrl+Enter 2x for urgent delivery
            logger.info(f"🚨 Sending HIGH PRIORITY message with Ctrl+Enter 2x...")
            
            # First Ctrl+Enter
            pyautogui.hotkey('ctrl', 'enter')
            time.sleep(0.5)
            
            # Second Ctrl+Enter (double-tap for high priority)
            pyautogui.hotkey('ctrl', 'enter')
            time.sleep(0.5)
            
            logger.info(f"✅ HIGH PRIORITY message sent to {recipient} via Ctrl+Enter 2x")
            return True
            
        except Exception as e:
            logger.error(f"Error sending HIGH PRIORITY message to {recipient}: {e}")
            return False
    
    def _send_normal_message(self, recipient: str, message_content: str, coords: AgentCoordinates) -> bool:
        """Send normal message using input box coordinates"""
        try:
            input_x, input_y = coords.input_box
            
            logger.info(f"📤 Normal message to {recipient} at input coordinates ({input_x}, {input_y})")
            
            # Prepare complete message with agent name
            complete_message = f"{recipient}\n\n{message_content}"
            
            # Copy complete message to clipboard
            pyperclip.copy(complete_message)
            
            # Click input box
            pyautogui.moveTo(input_x, input_y, duration=0.3)
            pyautogui.click()
            time.sleep(0.3)
            
            # Clear existing text (Ctrl+A + Delete)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(0.2)
            
            # Paste the complete message (Ctrl+V)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            # Send message (Enter)
            pyautogui.press('enter')
            time.sleep(0.3)
            
            logger.info(f"✅ Normal message sent to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending normal message to {recipient}: {e}")
            return False
    
    def send_bulk_messages(self, messages: Dict[str, str], mode: str = "8-agent", message_type: str = "text", new_chat: bool = False) -> Dict[str, bool]:
        """
        Send messages to multiple agents using PyAutoGUI
        
        Args:
            messages: Dictionary of agent_id: message_content
            mode: Coordinate mode to use
            message_type: Type of message (text, onboarding_start, etc.)
            new_chat: Whether these are new chat (onboarding) messages
        """
        results = {}
        
        for agent_id, message_content in messages.items():
            logger.info(f"Sending bulk PyAutoGUI message to {agent_id}...")
            success = self.send_message(agent_id, message_content, message_type, new_chat)
            results[agent_id] = success
            
            # Small delay between agents
            time.sleep(0.5)
        
        return results
    
    def activate_agent(self, agent_id: str, mode: str = "8-agent") -> bool:
        """Activate an agent by clicking their starter location"""
        try:
            coords = self.coordinate_manager.get_agent_coordinates(agent_id, mode)
            if not coords:
                logger.error(f"No coordinates for {agent_id}")
                return False
            
            x, y = coords.starter_location
            
            logger.info(f"Activating {agent_id} at coordinates ({x}, {y})")
            
            # Move to and click starter location
            pyautogui.moveTo(x, y, duration=0.3)
            pyautogui.click()
            
            # Wait for activation
            time.sleep(1.0)
            
            logger.info(f"✅ {agent_id} activated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error activating {agent_id}: {e}")
            return False
    
    def send_onboarding_message(self, agent_id: str, onboarding_message: str, mode: str = "8-agent") -> bool:
        """
        Send onboarding message using the proper sequence:
        starter location → Ctrl+N → validate → paste onboarding message
        
        Args:
            agent_id: Agent to onboard
            onboarding_message: Onboarding message content
            mode: Coordinate mode to use
        """
        try:
            logger.info(f"🚀 Starting onboarding sequence for {agent_id}...")
            
            coords = self.coordinate_manager.get_agent_coordinates(agent_id, mode)
            if not coords:
                logger.error(f"No coordinates for {agent_id}")
                return False
            
            # Use the onboarding message flow
            return self._send_onboarding_message(agent_id, onboarding_message, coords)
            
        except Exception as e:
            logger.error(f"Error sending onboarding message to {agent_id}: {e}")
            return False
    
    def send_bulk_onboarding(self, onboarding_messages: Dict[str, str], mode: str = "8-agent") -> Dict[str, bool]:
        """
        Send onboarding messages to multiple agents using the proper sequence
        
        Args:
            onboarding_messages: Dictionary of agent_id: onboarding_message
            mode: Coordinate mode to use
        """
        results = {}
        
        for agent_id, message_content in onboarding_messages.items():
            logger.info(f"🚀 Starting onboarding for {agent_id}...")
            success = self.send_onboarding_message(agent_id, message_content, mode)
            results[agent_id] = success
            
            # Longer delay between onboarding messages to ensure stability
            time.sleep(1.0)
        
        return results
    
    def send_high_priority_message(self, agent_id: str, urgent_message: str, mode: str = "8-agent") -> bool:
        """
        Send high priority message using Ctrl+Enter 2x sequence for urgent communications
        
        Args:
            agent_id: Agent to send urgent message to
            urgent_message: High priority message content
            mode: Coordinate mode to use
        """
        try:
            logger.info(f"🚨 Starting HIGH PRIORITY message sequence for {agent_id}...")
            
            coords = self.coordinate_manager.get_agent_coordinates(agent_id, mode)
            if not coords:
                logger.error(f"No coordinates for {agent_id}")
                return False
            
            # Use the high priority message flow
            return self._send_high_priority_message(agent_id, urgent_message, coords)
            
        except Exception as e:
            logger.error(f"Error sending HIGH PRIORITY message to {agent_id}: {e}")
            return False
    
    def send_bulk_high_priority(self, urgent_messages: Dict[str, str], mode: str = "8-agent") -> Dict[str, bool]:
        """
        Send high priority messages to multiple agents using Ctrl+Enter 2x sequence
        
        Args:
            urgent_messages: Dictionary of agent_id: urgent_message
            mode: Coordinate mode to use
        """
        results = {}
        
        for agent_id, message_content in urgent_messages.items():
            logger.info(f"🚨 Starting HIGH PRIORITY message for {agent_id}...")
            success = self.send_high_priority_message(agent_id, message_content, mode)
            results[agent_id] = success
            
            # Shorter delay between high priority messages for urgency
            time.sleep(0.3)
        
        return results
