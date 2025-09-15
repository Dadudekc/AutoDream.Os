#!/usr/bin/env python3
"""
Unified Messaging Service - V2 Compliant Module
===============================================

Unified messaging service consolidating PyAutoGUI delivery and messaging operations.

Consolidates:
- src/core/messaging_pyautogui.py (PyAutoGUI delivery)
- src/services/consolidated_messaging_service.py (messaging operations)
- Coordinate management and message formatting

V2 Compliance: < 400 lines, single responsibility for all messaging operations.

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Phase 2 Consolidation - Chunk 002 (Services)
License: MIT
"""

import logging
import os
import sys
import time
from typing import Any

from ..core.messaging_core import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageType,
)

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
DELETE_KEY = "backspace"


class CoordinateManager:
    """Coordinate management using SSOT pattern."""

    def __init__(self):
        self.coordinates_cache: dict[str, tuple[int, int]] = {}
        self.last_load_time: float | None = None
        self.cache_ttl = 300  # 5 minutes

    def load_coordinates(self) -> dict[str, tuple[int, int]]:
        """Load agent coordinates with caching."""
        current_time = time.time()

        # Return cached coordinates if still valid
        if (
            self.last_load_time
            and self.coordinates_cache
            and current_time - self.last_load_time < self.cache_ttl
        ):
            return self.coordinates_cache

        try:
            # Load from coordinate file (simplified for V2 compliance)
            coordinates = {
                "Agent-1": (-1269, 481),
                "Agent-2": (-308, 480),
                "Agent-3": (-1269, 1001),
                "Agent-4": (-308, 1000),
                "Agent-5": (652, 421),
                "Agent-6": (1612, 419),
                "Agent-7": (920, 851),
                "Agent-8": (1611, 941),
            }

            self.coordinates_cache = coordinates
            self.last_load_time = current_time
            logger.info(f"Loaded coordinates for {len(coordinates)} agents")
            return coordinates

        except Exception as e:
            logger.error(f"Error loading coordinates: {e}")
            return {}

    def get_agent_coordinates(self, agent_id: str) -> tuple[int, int] | None:
        """Get coordinates for specific agent."""
        if not self.coordinates_cache:
            self.load_coordinates()
        return self.coordinates_cache.get(agent_id)

    def validate_coordinates(self, coordinates: tuple[int, int]) -> bool:
        """Validate coordinate format."""
        return (
            isinstance(coordinates, tuple)
            and len(coordinates) == 2
            and all(isinstance(coord, (int, float)) for coord in coordinates)
        )


class MessageFormatter:
    """Message formatting utilities."""

    @staticmethod
    def format_message_for_delivery(message: UnifiedMessage) -> str:
        """Format message for PyAutoGUI delivery."""
        timestamp = time.strftime("%H:%M:%S")

        # Format based on message type
        if message.message_type == UnifiedMessageType.BROADCAST:
            prefix = f"🚀 BROADCAST [{timestamp}]"
        elif message.message_type == UnifiedMessageType.CAPTAIN_TO_AGENT:
            prefix = f"⚡ CAPTAIN [{timestamp}]"
        elif message.message_type == UnifiedMessageType.AGENT_TO_AGENT:
            prefix = f"[A2A] {message.sender} → {message.recipient} [{timestamp}]"
        else:
            prefix = f"📨 {message.sender} → {message.recipient} [{timestamp}]"

        # Add priority indicator
        if message.priority == UnifiedMessagePriority.URGENT:
            prefix = f"🚨 URGENT {prefix}"
        elif message.priority == UnifiedMessagePriority.HIGH:
            prefix = f"⚡ HIGH {prefix}"

        return f"{prefix}\nPriority: {message.priority.value}\nTags: {', '.join(message.tags)}\n\n{message.content}"


class PyAutoGUIDelivery:
    """PyAutoGUI message delivery service."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.delivery_count = 0
        self.success_count = 0
        self.failure_count = 0

    def deliver_message(self, message: UnifiedMessage, coordinates: tuple[int, int]) -> bool:
        """Deliver message using PyAutoGUI automation."""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning("PyAutoGUI not available, skipping delivery")
            return False

        try:
            self.delivery_count += 1
            formatted_message = MessageFormatter.format_message_for_delivery(message)

            # Move to coordinates
            pyautogui.moveTo(coordinates[0], coordinates[1], duration=CLICK_MOVE_DURATION)
            time.sleep(0.1)

            # Click to focus
            pyautogui.click()
            time.sleep(0.1)

            # Clear existing content
            pyautogui.hotkey(MOD, "a")
            time.sleep(0.05)
            pyautogui.press(DELETE_KEY)
            time.sleep(0.05)

            # Type message
            if PYPERCLIP_AVAILABLE:
                # Use clipboard for better reliability
                pyperclip.copy(formatted_message)
                pyautogui.hotkey(MOD, "v")
            else:
                # Fallback to typewrite
                pyautogui.typewrite(formatted_message, interval=0.01)

            time.sleep(0.1)

            # Send message (Enter key)
            pyautogui.press("enter")

            self.success_count += 1
            self.logger.info(f"Message delivered to {coordinates}")
            return True

        except Exception as e:
            self.failure_count += 1
            self.logger.error(f"Failed to deliver message: {e}")
            return False

    def deliver_bulk_messages(
        self, messages: list[UnifiedMessage], coordinates_map: dict[str, tuple[int, int]]
    ) -> dict[str, bool]:
        """Deliver multiple messages."""
        results = {}

        for message in messages:
            if message.recipient in coordinates_map:
                coords = coordinates_map[message.recipient]
                success = self.deliver_message(message, coords)
                results[message.recipient] = success
                time.sleep(0.5)  # Pause between deliveries
            else:
                results[message.recipient] = False
                self.logger.warning(f"No coordinates found for {message.recipient}")

        return results

    def get_delivery_statistics(self) -> dict[str, Any]:
        """Get delivery statistics."""
        total = self.delivery_count
        success_rate = self.success_count / total * 100 if total > 0 else 0

        return {
            "total_deliveries": total,
            "successful_deliveries": self.success_count,
            "failed_deliveries": self.failure_count,
            "success_rate": success_rate,
            "pyautogui_available": PYAUTOGUI_AVAILABLE,
            "pyperclip_available": PYPERCLIP_AVAILABLE,
        }


class UnifiedMessagingService:
    """Unified messaging service combining all messaging operations."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.coordinate_manager = CoordinateManager()
        self.message_formatter = MessageFormatter()
        self.pyautogui_delivery = PyAutoGUIDelivery()
        self.message_count = 0
        self.broadcast_count = 0

    def send_message(
        self,
        recipient: str,
        content: str,
        sender: str = "System",
        message_type: UnifiedMessageType = UnifiedMessageType.AGENT_TO_AGENT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
        tags: list[str] = None,
    ) -> bool:
        """Send a single message."""
        try:
            self.message_count += 1

            # Create unified message
            message = UnifiedMessage(
                content=content,
                sender=sender,
                recipient=recipient,
                message_type=message_type,
                priority=priority,
                tags=tags or [],
            )

            # Get coordinates
            coordinates = self.coordinate_manager.get_agent_coordinates(recipient)
            if not coordinates:
                self.logger.error(f"No coordinates found for {recipient}")
                return False

            # Deliver message
            success = self.pyautogui_delivery.deliver_message(message, coordinates)

            if success:
                self.logger.info(f"Message sent to {recipient}")
            else:
                self.logger.error(f"Failed to send message to {recipient}")

            return success

        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False

    def send_broadcast(
        self,
        content: str,
        sender: str = "System",
        priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
        tags: list[str] = None,
    ) -> dict[str, bool]:
        """Send broadcast message to all agents."""
        try:
            self.broadcast_count += 1

            # Load all coordinates
            coordinates = self.coordinate_manager.load_coordinates()

            # Create messages for all agents
            messages = []
            for agent_id in coordinates.keys():
                message = UnifiedMessage(
                    content=content,
                    sender=sender,
                    recipient=agent_id,
                    message_type=UnifiedMessageType.BROADCAST,
                    priority=priority,
                    tags=tags or [],
                )
                messages.append(message)

            # Deliver all messages
            results = self.pyautogui_delivery.deliver_bulk_messages(messages, coordinates)

            success_count = sum(1 for success in results.values() if success)
            self.logger.info(f"Broadcast sent to {success_count}/{len(results)} agents")

            return results

        except Exception as e:
            self.logger.error(f"Error sending broadcast: {e}")
            return {}

    def get_service_statistics(self) -> dict[str, Any]:
        """Get service statistics."""
        delivery_stats = self.pyautogui_delivery.get_delivery_statistics()

        return {
            "messaging": {
                "total_messages": self.message_count,
                "total_broadcasts": self.broadcast_count,
                "coordinate_cache_size": len(self.coordinate_manager.coordinates_cache),
            },
            "delivery": delivery_stats,
            "coordinates": {
                "total_agents": len(self.coordinate_manager.coordinates_cache),
                "cache_loaded": self.coordinate_manager.last_load_time is not None,
            },
        }

    def reload_coordinates(self) -> bool:
        """Reload coordinate cache."""
        try:
            self.coordinate_manager.load_coordinates()
            self.logger.info("Coordinates reloaded successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error reloading coordinates: {e}")
            return False


# Export main classes
__all__ = ["UnifiedMessagingService", "CoordinateManager", "MessageFormatter", "PyAutoGUIDelivery"]
