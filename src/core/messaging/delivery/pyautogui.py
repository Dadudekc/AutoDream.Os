#!/usr/bin/env python3
"""
PyAutoGUI Delivery Service - V2 Compliant Physical Automation
============================================================

V2 compliant PyAutoGUI delivery service for physical automation-based messaging.
Consolidated from src/core/messaging_pyautogui.py with improved architecture.

V2 Compliance: <300 lines, single responsibility for PyAutoGUI delivery
Enterprise Ready: High availability, error handling, retry logic, monitoring

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

from __future__ import annotations

import logging
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

from ..models import UnifiedMessage, DeliveryMethod, MessageStatus
from ..interfaces import BaseMessageDelivery, ICoordinateProvider

logger = logging.getLogger(__name__)

# Feature flags (can be overridden by env)
ENABLE_PYAUTOGUI = os.getenv("ENABLE_PYAUTOGUI", "1") not in ("0", "false", "False")
PAUSE_S = float(os.getenv("PYAUTO_PAUSE_S", "0.05"))
CLICK_MOVE_DURATION = float(os.getenv("PYAUTO_MOVE_DURATION", "0.4"))
SEND_RETRIES = int(os.getenv("PYAUTO_SEND_RETRIES", "2"))
RETRY_SLEEP_S = float(os.getenv("PYAUTO_RETRY_SLEEP_S", "0.3"))

# Runtime deps (optional)
try:
    import pyautogui  # type: ignore
    PYAUTOGUI_AVAILABLE = True and ENABLE_PYAUTOGUI
    if PYAUTOGUI_AVAILABLE:
        pyautogui.PAUSE = PAUSE_S
        pyautogui.FAILSAFE = True
except Exception as e:
    PYAUTOGUI_AVAILABLE = False
    logger.info("⚠️ PyAutoGUI not available/enabled: %s", e)

try:
    import pyperclip  # type: ignore
    PYPERCLIP_AVAILABLE = True
except Exception as e:
    PYPERCLIP_AVAILABLE = False
    logger.info("⚠️ Pyperclip not available: %s", e)

# OS modifiers
IS_MAC = sys.platform == "darwin"
MOD = "command" if IS_MAC else "ctrl"
DELETE_KEY = "backspace"  # safer than delete for text fields on most UIs

class PyAutoGUIMessagingDelivery(BaseMessageDelivery):
    """V2 compliant PyAutoGUI messaging delivery service."""

    def __init__(self, coordinate_provider: Optional[ICoordinateProvider] = None):
        """Initialize PyAutoGUI delivery service."""
        super().__init__(DeliveryMethod.PYAUTOGUI)
        self.coordinate_provider = coordinate_provider
        self.logger = logging.getLogger(__name__)
        
        # Initialize coordinate provider if not provided
        if not self.coordinate_provider:
            self._initialize_coordinate_provider()

    def _initialize_coordinate_provider(self):
        """Initialize coordinate provider."""
        try:
            from ...coordinate_loader import get_coordinate_loader
            self.coordinate_provider = get_coordinate_loader()
        except ImportError:
            self.logger.warning("Coordinate loader not available")

    def send_message(self, message: UnifiedMessage) -> bool:
        """Send message via PyAutoGUI."""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.error("PyAutoGUI not available/enabled")
            self._record_metrics(message, False)
            return False

        if not self.coordinate_provider:
            self.logger.error("No coordinate provider available")
            self._record_metrics(message, False)
            return False

        try:
            # Get coordinates for recipient
            coords = self.coordinate_provider.get_agent_coordinates(message.recipient)
            if not coords:
                self.logger.error("Missing coordinates for %s", message.recipient)
                self._record_metrics(message, False)
                return False

            # Format message for delivery
            formatted_message = self._format_message_for_delivery(message)
            
            # Deliver message
            success = self._deliver_message_pyautogui(message, coords, formatted_message)
            
            # Update message status
            message.status = MessageStatus.SENT if success else MessageStatus.FAILED
            message.delivery_method = DeliveryMethod.PYAUTOGUI
            
            # Record metrics
            self._record_metrics(message, success)
            
            return success

        except Exception as e:
            self.logger.error(f"Error sending message via PyAutoGUI: {e}")
            message.status = MessageStatus.FAILED
            self._record_metrics(message, False)
            return False

    def can_deliver(self, message: UnifiedMessage) -> bool:
        """Check if PyAutoGUI can deliver this message."""
        return (
            PYAUTOGUI_AVAILABLE and 
            self.coordinate_provider is not None and
            self.coordinate_provider.get_agent_coordinates(message.recipient) is not None
        )

    def _format_message_for_delivery(self, message: UnifiedMessage) -> str:
        """Format message for delivery with agent identification."""
        try:
            tag_map = {
                "agent_to_agent": "[A2A]",
                "captain_to_agent": "[C2A]",
                "system_to_agent": "[S2A]",
                "human_to_agent": "[H2A]",
                "broadcast": "[BROADCAST]",
                "onboarding": "[ONBOARDING]",
            }
            agent_tag = tag_map.get(message.message_type.value, "[TEXT]")
            lines = [
                f"{agent_tag} {message.sender} → {message.recipient}",
                f"Priority: {message.priority.value.upper()}",
            ]
            if message.tags:
                lines.append(f"Tags: {', '.join(tag.value for tag in message.tags)}")
            lines += [
                "",
                message.content,
                "",
                f"You are {message.recipient}",
                f"Timestamp: {message.timestamp}",
            ]
            return "\n".join(lines)
        except Exception as e:
            self.logger.error("Error formatting message: %s", e)
            return message.content

    def _deliver_message_pyautogui(self, message: UnifiedMessage, coords: Tuple[int, int], 
                                  formatted_message: str) -> bool:
        """Deliver message via PyAutoGUI to specific coordinates."""
        x, y = coords

        for attempt in range(1, SEND_RETRIES + 2):
            try:
                # Focus and clear input
                self._focus_and_clear(x, y)
                
                # Paste or type message
                self._paste_or_type(formatted_message)
                
                # Send message
                time.sleep(PAUSE_S)
                pyautogui.press("enter")
                
                self.logger.info("Message delivered to %s at %s (attempt %d)", 
                               message.recipient, coords, attempt)
                return True
                
            except Exception as e:
                self.logger.warning("Deliver attempt %d failed for %s: %s", 
                                  attempt, message.recipient, e)
                time.sleep(RETRY_SLEEP_S)

        self.logger.error("Failed to deliver to %s after %d attempts", 
                         message.recipient, SEND_RETRIES + 1)
        return False

    def _focus_and_clear(self, x: int, y: int) -> None:
        """Focus the input and clear it."""
        pyautogui.moveTo(x, y, duration=CLICK_MOVE_DURATION)
        pyautogui.click()
        time.sleep(PAUSE_S)
        pyautogui.hotkey(MOD, "a")
        time.sleep(PAUSE_S)
        pyautogui.press(DELETE_KEY)
        time.sleep(PAUSE_S)

    def _paste_or_type(self, text: str) -> None:
        """Prefer clipboard paste; fallback to typewrite."""
        if PYPERCLIP_AVAILABLE:
            try:
                pyperclip.copy(text)
                time.sleep(PAUSE_S)
                pyautogui.hotkey(MOD, "v")
                return
            except Exception as e:
                self.logger.warning("Clipboard paste failed, falling back to typewrite: %s", e)
        pyautogui.typewrite(text, interval=0.0)

    def deliver_bulk_messages(self, messages: List[UnifiedMessage], 
                            agent_order: Optional[List[str]] = None) -> Dict[str, bool]:
        """Deliver multiple messages via PyAutoGUI."""
        results: Dict[str, bool] = {}
        
        if not PYAUTOGUI_AVAILABLE:
            self.logger.error("PyAutoGUI not available/enabled")
            return results

        order = agent_order or [f"Agent-{i}" for i in range(1, 9)]
        
        for msg in messages:
            if msg.recipient not in order:
                results[msg.recipient] = False
                continue
                
            success = self.send_message(msg)
            results[msg.recipient] = success
            
            # Small pacing across recipients
            time.sleep(1.0)
            
        return results

    def cleanup_resources(self) -> bool:
        """Cleanup PyAutoGUI resources."""
        try:
            if PYAUTOGUI_AVAILABLE:
                # Nothing to cleanup explicitly; keep FAILSAFE on
                self.logger.info("PyAutoGUI resources validated; FAILSAFE=%s, PAUSE=%.2f", 
                               pyautogui.FAILSAFE, pyautogui.PAUSE)
            return True
        except Exception as e:
            self.logger.error("Error during cleanup: %s", e)
            return False

    def get_system_status(self) -> Dict[str, any]:
        """Get PyAutoGUI system status."""
        return {
            "pyautogui_available": PYAUTOGUI_AVAILABLE,
            "pyperclip_available": PYPERCLIP_AVAILABLE,
            "coordinate_provider_available": self.coordinate_provider is not None,
            "pause_seconds": PAUSE_S,
            "move_duration": CLICK_MOVE_DURATION,
            "send_retries": SEND_RETRIES,
            "retry_sleep": RETRY_SLEEP_S,
            "platform": sys.platform,
            "modifier_key": MOD
        }

# Legacy compatibility functions
def deliver_message_pyautogui(message: UnifiedMessage, coords: Tuple[int, int]) -> bool:
    """Legacy function for backward compatibility."""
    delivery = PyAutoGUIMessagingDelivery()
    formatted_message = delivery._format_message_for_delivery(message)
    return delivery._deliver_message_pyautogui(message, coords, formatted_message)

def deliver_bulk_messages_pyautogui(messages: List[UnifiedMessage], 
                                  agent_order: Optional[List[str]] = None) -> Dict[str, bool]:
    """Legacy function for backward compatibility."""
    delivery = PyAutoGUIMessagingDelivery()
    return delivery.deliver_bulk_messages(messages, agent_order)

def format_message_for_delivery(message: UnifiedMessage) -> str:
    """Legacy function for backward compatibility."""
    delivery = PyAutoGUIMessagingDelivery()
    return delivery._format_message_for_delivery(message)

def get_agent_coordinates(agent_id: str) -> Optional[Tuple[int, int]]:
    """Legacy function for backward compatibility."""
    try:
        from ...coordinate_loader import get_coordinate_loader
        loader = get_coordinate_loader()
        return loader.get_chat_coordinates(agent_id)
    except Exception as e:
        logger.warning("Invalid/missing coordinates for %s: %s", agent_id, e)
        return None

def cleanup_pyautogui_resources() -> bool:
    """Legacy function for backward compatibility."""
    delivery = PyAutoGUIMessagingDelivery()
    return delivery.cleanup_resources()

# EXPORTS
__all__ = [
    # Main class
    "PyAutoGUIMessagingDelivery",
    
    # Legacy compatibility functions
    "deliver_message_pyautogui",
    "deliver_bulk_messages_pyautogui", 
    "format_message_for_delivery",
    "get_agent_coordinates",
    "cleanup_pyautogui_resources",
    
    # Constants
    "PYAUTOGUI_AVAILABLE",
    "PYPERCLIP_AVAILABLE",
]