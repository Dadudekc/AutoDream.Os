#!/usr/bin/env python3
"""
Messaging Core Service - V2 Compliant Module
===========================================

Core messaging service functionality.
V2 Compliance: < 400 lines, single responsibility.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 Compliance - Messaging Service Modularization
License: MIT
"""

import asyncio
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# Import PyAutoGUI messaging system
try:
    from src.core.messaging_pyautogui import (
        format_message_for_delivery,
        deliver_message_pyautogui,
        deliver_bulk_messages_pyautogui,
        get_agent_coordinates,
        load_coordinates_from_json,
        PyAutoGUIMessagingDelivery,
        PYAUTOGUI_AVAILABLE,
        PYPERCLIP_AVAILABLE,
    )
except ImportError:
    # Fallback for missing imports
    PYAUTOGUI_AVAILABLE = False
    PYPERCLIP_AVAILABLE = False


class UnifiedMessageType(Enum):
    """Message type enumeration."""
    AGENT_TO_AGENT = "A2A"
    BROADCAST = "BROADCAST"
    SYSTEM = "SYSTEM"
    TEXT = "TEXT"


class UnifiedMessagePriority(Enum):
    """Message priority enumeration."""
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


class UnifiedMessageTag(Enum):
    """Message tag enumeration."""
    GENERAL = "GENERAL"
    COORDINATION = "COORDINATION"
    EMERGENCY = "EMERGENCY"
    WORKFLOW = "WORKFLOW"


class UnifiedMessage:
    """Unified message model."""

    def __init__(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
        tags: List[UnifiedMessageTag] = None,
        timestamp: Optional[datetime] = None
    ):
        """Initialize unified message."""
        self.content = content
        self.sender = sender
        self.recipient = recipient
        self.message_type = message_type
        self.priority = priority
        self.tags = tags or [UnifiedMessageTag.GENERAL]
        self.timestamp = timestamp or datetime.now()


class ConsolidatedMessagingService:
    """Consolidated messaging service with core functionality."""

    def __init__(self):
        """Initialize messaging service."""
        self.logger = self._setup_logger()
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._coordinates_loaded = False
        self._load_coordinates()

    def _setup_logger(self) -> logging.Logger:
        """Setup logger for messaging service."""
        logger = logging.getLogger("messaging_service")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger

    def _load_coordinates(self) -> None:
        """Load agent coordinates."""
        try:
            if PYAUTOGUI_AVAILABLE:
                load_coordinates_from_json()
                self._coordinates_loaded = True
                self.logger.info("Agent coordinates loaded successfully")
            else:
                self.logger.warning("PyAutoGUI not available - coordinates not loaded")
        except Exception as e:
            self.logger.error(f"Failed to load coordinates: {e}")

    def send_message_to_agent(
        self,
        agent_id: str,
        message: str,
        sender: str = "System",
        priority: str = "NORMAL",
        tags: List[str] = None
    ) -> bool:
        """Send message to specific agent."""
        try:
            # Create unified message
            unified_message = UnifiedMessage(
                content=message,
                sender=sender,
                recipient=agent_id,
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority(priority),
                tags=[UnifiedMessageTag(tag) for tag in (tags or ["GENERAL"])]
            )

            # Get coordinates for the agent
            coords = get_agent_coordinates(agent_id) if PYAUTOGUI_AVAILABLE else None
            
            if coords:
                # Use PyAutoGUI delivery
                result = deliver_message_pyautogui(unified_message, coords)
                if result:
                    self.logger.info(f"Message sent to {agent_id} via PyAutoGUI")
                    return True
                else:
                    self.logger.warning(f"PyAutoGUI delivery failed for {agent_id}")
            
            # Fallback to inbox delivery
            return self._send_to_inbox(unified_message)
            
        except Exception as e:
            self.logger.error(f"Failed to send message to {agent_id}: {e}")
            return False

    def broadcast_message(
        self,
        message: str,
        sender: str = "System",
        priority: str = "NORMAL",
        tags: List[str] = None
    ) -> bool:
        """Broadcast message to all agents."""
        try:
            # Create unified message
            unified_message = UnifiedMessage(
                content=message,
                sender=sender,
                recipient="ALL",
                message_type=UnifiedMessageType.BROADCAST,
                priority=UnifiedMessagePriority(priority),
                tags=[UnifiedMessageTag(tag) for tag in (tags or ["GENERAL"])]
            )

            # Get all agent coordinates
            if PYAUTOGUI_AVAILABLE and self._coordinates_loaded:
                agent_coords = {}
                for i in range(1, 9):  # Agent-1 to Agent-8
                    agent_id = f"Agent-{i}"
                    coords = get_agent_coordinates(agent_id)
                    if coords:
                        agent_coords[agent_id] = coords

                if agent_coords:
                    # Use bulk PyAutoGUI delivery
                    result = deliver_bulk_messages_pyautogui(unified_message, agent_coords)
                    if result:
                        self.logger.info(f"Broadcast sent to {len(agent_coords)} agents via PyAutoGUI")
                        return True

            # Fallback to individual inbox delivery
            return self._broadcast_to_inboxes(unified_message)
            
        except Exception as e:
            self.logger.error(f"Failed to broadcast message: {e}")
            return False

    def _send_to_inbox(self, message: UnifiedMessage) -> bool:
        """Send message to agent inbox as fallback."""
        try:
            # Create inbox path
            from pathlib import Path
            inbox_path = Path("agent_workspaces") / message.recipient / "inbox"
            inbox_path.mkdir(parents=True, exist_ok=True)

            # Create message filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"CAPTAIN_MESSAGE_{timestamp}_messaging.md"

            # Create message content
            content = f"""# 🚨 CAPTAIN MESSAGE FROM MESSAGING SERVICE

**From**: {message.sender}
**To**: {message.recipient}
**Priority**: {message.priority.value}
**Type**: {message.message_type.value}
**Tags**: {', '.join([tag.value for tag in message.tags])}
**Timestamp**: {message.timestamp.isoformat()}

---

{message.content}

---

**Message delivered via Messaging Service**
**WE. ARE. SWARM. ⚡️🔥**
"""

            # Write message to inbox
            message_file = inbox_path / filename
            with open(message_file, "w", encoding="utf-8") as f:
                f.write(content)

            self.logger.info(f"Message sent to {message.recipient} inbox: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send to inbox: {e}")
            return False

    def _broadcast_to_inboxes(self, message: UnifiedMessage) -> bool:
        """Broadcast message to all agent inboxes."""
        try:
            success_count = 0
            for i in range(1, 9):  # Agent-1 to Agent-8
                agent_id = f"Agent-{i}"
                message.recipient = agent_id
                if self._send_to_inbox(message):
                    success_count += 1

            self.logger.info(f"Broadcast sent to {success_count}/8 agent inboxes")
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Failed to broadcast to inboxes: {e}")
            return False

    def get_service_status(self) -> Dict[str, Any]:
        """Get messaging service status."""
        return {
            "active": True,
            "pyautogui_available": PYAUTOGUI_AVAILABLE,
            "pyperclip_available": PYPERCLIP_AVAILABLE,
            "coordinates_loaded": self._coordinates_loaded,
            "active_agents": 8,  # Agent-1 to Agent-8
            "timestamp": datetime.now().isoformat()
        }

    def shutdown(self) -> None:
        """Shutdown messaging service."""
        try:
            self.executor.shutdown(wait=True)
            self.logger.info("Messaging service shutdown complete")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")


# Export for use by other modules
__all__ = [
    "UnifiedMessage",
    "UnifiedMessageType", 
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "ConsolidatedMessagingService"
]
