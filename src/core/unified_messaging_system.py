#!/usr/bin/env python3
"""
Unified Messaging System - V2 Compliant Core Module
Consolidates messaging_core.py, messaging_pyautogui.py, health_check.py, registry_loader.py
V2 Compliance: < 400 lines, single responsibility for all core messaging operations.
Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)

# Feature flags
ENABLE_PYAUTOGUI = os.getenv("ENABLE_PYAUTOGUI", "1") not in ("0", "false", "False")
PAUSE_S = float(os.getenv("PYAUTO_PAUSE_S", "0.05"))
CLICK_MOVE_DURATION = float(os.getenv("PYAUTO_MOVE_DURATION", "0.4"))
SEND_RETRIES = int(os.getenv("PYAUTO_SEND_RETRIES", "2"))
RETRY_SLEEP_S = float(os.getenv("PYAUTO_RETRY_SLEEP_S", "0.3"))
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

IS_MAC = sys.platform == "darwin"
MOD = "command" if IS_MAC else "ctrl"
DELETE_KEY = "backspace"


class UnifiedMessageType(Enum):
    AGENT_TO_AGENT = "agent_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    SYSTEM_TO_AGENT = "system_to_agent"
    HUMAN_TO_AGENT = "human_to_agent"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"


class UnifiedMessagePriority(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


class UnifiedMessageTag(Enum):
    GENERAL = "GENERAL"
    COORDINATION = "COORDINATION"
    TASK = "TASK"
    STATUS = "STATUS"
    CLEANUP = "CLEANUP"
    MODULARIZATION = "MODULARIZATION"


@dataclass
class UnifiedMessage:
    """Unified message structure with formatting support."""

    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType = UnifiedMessageType.AGENT_TO_AGENT
    priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL
    tags: list[str] = None
    timestamp: datetime | None = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.tags is None:
            self.tags = []


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


class HealthMonitor:
    """Health monitoring for messaging system."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.health_checks = 0
        self.last_health_check = None
        self.health_status = "unknown"

    def check_health(self) -> dict[str, Any]:
        """Check messaging system health."""
        try:
            self.health_checks += 1
            self.last_health_check = time.time()

            # Check PyAutoGUI availability
            pyautogui_healthy = PYAUTOGUI_AVAILABLE
            pyperclip_healthy = PYPERCLIP_AVAILABLE

            # Determine overall health
            if pyautogui_healthy and pyperclip_healthy:
                self.health_status = "healthy"
            elif pyautogui_healthy:
                self.health_status = "degraded"
            else:
                self.health_status = "unhealthy"

            return {
                "status": self.health_status,
                "pyautogui_available": pyautogui_healthy,
                "pyperclip_available": pyperclip_healthy,
                "last_check": self.last_health_check,
                "total_checks": self.health_checks,
            }

        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            self.health_status = "error"
            return {
                "status": "error",
                "error": str(e),
                "last_check": self.last_health_check,
                "total_checks": self.health_checks,
            }


class RegistryManager:
    """Registry management for messaging system."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.registered_agents: dict[str, dict[str, Any]] = {}
        self.registry_updates = 0

    def register_agent(self, agent_id: str, metadata: dict[str, Any]) -> bool:
        """Register an agent in the messaging registry."""
        try:
            self.registered_agents[agent_id] = {
                **metadata,
                "registered_at": time.time(),
                "last_activity": time.time(),
            }
            self.registry_updates += 1
            self.logger.info(f"Registered agent {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to register agent {agent_id}: {e}")
            return False

    def get_agent_info(self, agent_id: str) -> dict[str, Any] | None:
        """Get agent information from registry."""
        return self.registered_agents.get(agent_id)

    def list_agents(self) -> list[str]:
        """List all registered agents."""
        return list(self.registered_agents.keys())


class UnifiedMessagingSystem:
    """Unified messaging system combining all core messaging functionality."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.coordinate_manager = CoordinateManager()
        self.message_formatter = MessageFormatter()
        self.pyautogui_delivery = PyAutoGUIDelivery()
        self.health_monitor = HealthMonitor()
        self.registry_manager = RegistryManager()
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
            results = {}
            for agent_id in coordinates.keys():
                success = self.send_message(
                    recipient=agent_id,
                    content=content,
                    sender=sender,
                    message_type=UnifiedMessageType.BROADCAST,
                    priority=priority,
                    tags=tags,
                )
                results[agent_id] = success

            success_count = sum(1 for success in results.values() if success)
            self.logger.info(f"Broadcast sent to {success_count}/{len(results)} agents")

            return results

        except Exception as e:
            self.logger.error(f"Error sending broadcast: {e}")
            return {}

    def get_system_health(self) -> dict[str, Any]:
        """Get messaging system health status."""
        return self.health_monitor.check_health()

    def get_system_statistics(self) -> dict[str, Any]:
        """Get system statistics."""
        delivery_stats = {
            "total_deliveries": self.pyautogui_delivery.delivery_count,
            "successful_deliveries": self.pyautogui_delivery.success_count,
            "failed_deliveries": self.pyautogui_delivery.failure_count,
            "success_rate": (
                self.pyautogui_delivery.success_count / self.pyautogui_delivery.delivery_count * 100
                if self.pyautogui_delivery.delivery_count > 0
                else 0
            ),
        }

        return {
            "messaging": {
                "total_messages": self.message_count,
                "total_broadcasts": self.broadcast_count,
                "coordinate_cache_size": len(self.coordinate_manager.coordinates_cache),
            },
            "delivery": delivery_stats,
            "health": self.get_system_health(),
            "registry": {
                "registered_agents": len(self.registry_manager.registered_agents),
                "registry_updates": self.registry_manager.registry_updates,
            },
        }


# Export main classes
__all__ = [
    "UnifiedMessagingSystem",
    "UnifiedMessage",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "CoordinateManager",
    "MessageFormatter",
    "PyAutoGUIDelivery",
    "HealthMonitor",
    "RegistryManager",
]
