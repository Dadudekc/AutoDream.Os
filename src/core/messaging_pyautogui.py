#!/usr/bin/env python3
"""
PyAutoGUI Messaging Delivery - CONSOLIDATED SSOT (hardened)
===========================================================

Critical path for agent messaging via cursor/keyboard automation.

Changes:
- Cross-platform hotkeys (Ctrl vs Command)
- Resilient coordinate usage (no brittle bounds; safe attempts)
- Clipboard + typewrite fallback
- Consistent SSOT coordinate loader import
- Structured logging, retries, and small pauses
"""

from __future__ import annotations

import logging
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

from .messaging_core import (
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
DELETE_KEY = "backspace"  # safer than delete for text fields on most UIs


# -------------------- Coordinate Loader (SSOT) -------------------- #

def _get_coordinate_loader():
    # Single source-of-truth import path
    from .coordinate_loader import get_coordinate_loader  # local SSOT
    return get_coordinate_loader()


def load_coordinates_from_json() -> Dict[str, Tuple[int, int]]:
    """Load agent coordinates using SSOT coordinate loader."""
    try:
        loader = _get_coordinate_loader()
        coordinates: Dict[str, Tuple[int, int]] = {}
        for agent_id in loader.get_all_agents():
            try:
                if getattr(loader, "is_agent_active", lambda _a: True)(agent_id):
                    coords = loader.get_chat_coordinates(agent_id)
                    coordinates[agent_id] = coords  # type: ignore[assignment]
                    logger.debug("Loaded coordinates for %s: %s", agent_id, coords)
            except Exception as e:
                logger.warning("Invalid coordinates for %s: %s", agent_id, e)
        return coordinates
    except Exception as e:
        logger.error("Error loading coordinates: %s", e)
        return {}


def get_agent_coordinates(agent_id: str) -> Optional[Tuple[int, int]]:
    """Get coordinates for a specific agent via SSOT loader."""
    try:
        loader = _get_coordinate_loader()
        return loader.get_chat_coordinates(agent_id)  # type: ignore[return-value]
    except Exception as e:
        logger.warning("Invalid/missing coordinates for %s: %s", agent_id, e)
        return None


# -------------------- Formatting -------------------- #

def format_message_for_delivery(message: UnifiedMessage) -> str:
    """Format message for delivery with enhanced agent identification."""
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
        
        # Enhanced sender identification with visual emphasis
        sender_line = f"📤 FROM: {message.sender}"
        recipient_line = f"📥 TO: {message.recipient}"
        
        lines = [
            "=" * 60,
            f"{agent_tag} MESSAGE",
            "=" * 60,
            sender_line,
            recipient_line,
            f"Priority: {message.priority.value.upper()}",
        ]
        if message.tags:
            lines.append(f"Tags: {', '.join(tag.value for tag in message.tags)}")
        lines += [
            "-" * 60,
            "",
            message.content,
            "",
            "-" * 60,
            f"You are {message.recipient}",
            f"Timestamp: {message.timestamp}",
            "=" * 60,
        ]
        return "\n".join(lines)
    except Exception as e:
        logger.error("Error formatting message: %s", e)
        return message.content


# -------------------- Delivery Core -------------------- #

def _focus_and_clear(x: int, y: int) -> None:
    """Focus the input and clear it."""
    pyautogui.moveTo(x, y, duration=CLICK_MOVE_DURATION)
    pyautogui.click()
    time.sleep(PAUSE_S)
    pyautogui.hotkey(MOD, "a")
    time.sleep(PAUSE_S)
    pyautogui.press(DELETE_KEY)
    time.sleep(PAUSE_S)


def _paste_or_type(text: str) -> None:
    """Prefer clipboard paste; fallback to typewrite."""
    if PYPERCLIP_AVAILABLE:
        try:
            pyperclip.copy(text)
            time.sleep(PAUSE_S)
            pyautogui.hotkey(MOD, "v")
            return
        except Exception as e:
            logger.warning("Clipboard paste failed, falling back to typewrite: %s", e)
    pyautogui.typewrite(text, interval=0.0)


def deliver_message_pyautogui(message: UnifiedMessage, coords: Tuple[int, int]) -> bool:
    """Deliver message via PyAutoGUI to specific coordinates with validation."""
    if not PYAUTOGUI_AVAILABLE:
        logger.error("PyAutoGUI not available/enabled")
        return False
    if not coords:
        logger.error("No coordinates for %s", message.recipient)
        return False

    x, y = coords
    
    # Validate coordinates before attempting delivery
    if not _validate_coordinates_for_delivery(x, y, message.recipient):
        return False

    formatted_message = format_message_for_delivery(message)

    for attempt in range(1, SEND_RETRIES + 2):
        try:
            _focus_and_clear(x, y)
            _paste_or_type(formatted_message)
            time.sleep(PAUSE_S)
            pyautogui.press("enter")
            logger.info("Message delivered to %s at %s (attempt %d)", message.recipient, coords, attempt)
            return True
        except Exception as e:
            logger.warning("Deliver attempt %d failed for %s: %s", attempt, message.recipient, e)
            time.sleep(RETRY_SLEEP_S)

    logger.error("Failed to deliver to %s after %d attempts", message.recipient, SEND_RETRIES + 1)
    return False


def _validate_coordinates_for_delivery(x: int, y: int, agent_id: str) -> bool:
    """Validate coordinates before attempting message delivery."""
    # Check for valid coordinate types
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        logger.error("❌ Invalid coordinate types for %s: (%s, %s)", agent_id, type(x), type(y))
        return False
    
    # Check for reasonable coordinate ranges
    if x < -10000 or x > 10000 or y < -10000 or y > 10000:
        logger.error("❌ Coordinates out of reasonable range for %s: (%d, %d)", agent_id, x, y)
        return False
    
    # Check for default/invalid coordinates
    if x == 0 and y == 0:
        logger.error("❌ Default coordinates (0,0) for %s - likely not configured", agent_id)
        return False
    
    # Check for negative coordinates (might be valid for multi-monitor setups)
    if x < -5000 or y < -5000:
        logger.warning("⚠️ Very negative coordinates for %s: (%d, %d) - ensure this is correct", agent_id, x, y)
    
    logger.debug("✅ Coordinates validated for %s: (%d, %d)", agent_id, x, y)
    return True


def deliver_bulk_messages_pyautogui(
    messages: List[UnifiedMessage], agent_order: Optional[List[str]] = None
) -> Dict[str, bool]:
    """Deliver multiple messages via PyAutoGUI with validation."""
    results: Dict[str, bool] = {}
    if not PYAUTOGUI_AVAILABLE:
        logger.error("PyAutoGUI not available/enabled")
        return results

    # Validate all agents before starting delivery
    valid_agents = _validate_all_agents_for_delivery(messages)
    if not valid_agents:
        logger.error("❌ No valid agents found for bulk delivery")
        return {msg.recipient: False for msg in messages}

    order = agent_order or [f"Agent-{i}" for i in range(1, 9)]
    for msg in messages:
        if msg.recipient not in order:
            results[msg.recipient] = False
            logger.warning("⚠️ Agent %s not in expected order, skipping", msg.recipient)
            continue
        
        if msg.recipient not in valid_agents:
            results[msg.recipient] = False
            logger.error("❌ Agent %s failed validation, skipping delivery", msg.recipient)
            continue
            
        coords = get_agent_coordinates(msg.recipient)
        ok = deliver_message_pyautogui(msg, coords) if coords else False
        results[msg.recipient] = ok
        time.sleep(1.0)  # small pacing across recipients
    return results


def _validate_all_agents_for_delivery(messages: List[UnifiedMessage]) -> List[str]:
    """Validate all agents before bulk delivery."""
    valid_agents = []
    loader = _get_coordinate_loader()
    
    for msg in messages:
        agent_id = msg.recipient
        is_valid, error_msg = loader.validate_coordinates(agent_id)
        if is_valid:
            valid_agents.append(agent_id)
            logger.debug("✅ Agent %s validated for delivery", agent_id)
        else:
            logger.error("❌ Agent %s validation failed: %s", agent_id, error_msg)
    
    logger.info("📊 Bulk delivery validation: %d/%d agents valid", len(valid_agents), len(messages))
    return valid_agents


def cleanup_pyautogui_resources() -> bool:
    """Cleanup PyAutoGUI resources."""
    try:
        if PYAUTOGUI_AVAILABLE:
            # nothing to cleanup explicitly; keep FAILSAFE on
            logger.info("PyAutoGUI resources validated; FAILSAFE=%s, PAUSE=%.2f", pyautogui.FAILSAFE, pyautogui.PAUSE)
        return True
    except Exception as e:
        logger.error("Error during cleanup: %s", e)
        return False


class PyAutoGUIMessagingDelivery:
    """Simple wrapper class for PyAutoGUI messaging functions."""

    def __init__(self, agents: Optional[Dict[str, Tuple[int, int]]] = None):
        self.agents = agents or {}

    def send_message(self, message: UnifiedMessage) -> bool:
        return self.send_message_via_pyautogui(message)
    
    def deliver_message(self, message: UnifiedMessage) -> bool:
        """Alias for send_message to match expected interface."""
        return self.send_message_via_pyautogui(message)

    def send_message_via_pyautogui(
        self,
        message: UnifiedMessage,
        use_paste: bool = True,           # retained for API compatibility
        new_tab_method: str = "ctrl_t",   # deprecated; no-op
        use_new_tab: Optional[bool] = None,  # deprecated; no-op
    ) -> bool:
        if not PYAUTOGUI_AVAILABLE:
            logger.error("PyAutoGUI not available/enabled")
            return False
        coords = get_agent_coordinates(message.recipient)
        if not coords:
            logger.error("Missing coordinates for %s", message.recipient)
            return False
        return deliver_message_pyautogui(message, coords)

