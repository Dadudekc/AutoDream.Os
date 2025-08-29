"""Messaging transport implementations for PyAutoGUI delivery."""
from __future__ import annotations

import logging
import time
from typing import Dict

from .coordinate_manager import AgentCoordinates
from .pyautogui_helpers import (
    PYAUTOGUI_AVAILABLE,
    move_and_click,
    paste_text,
    press_enter,
    press_hotkey,
)

logger = logging.getLogger(__name__)


def send_normal_message(coords: AgentCoordinates, message: str) -> bool:
    """Send a standard message to an agent."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("PyAutoGUI not available - simulating normal message")
            return True
        move_and_click(*coords.input_box)
        time.sleep(0.5)
        paste_text(message)
        time.sleep(0.5)
        press_enter()
        logger.info("✅ Normal message sent")
        return True
    except Exception as e:  # pragma: no cover - runtime safeguard
        logger.error(f"Failed to send normal message: {e}")
        return False


def send_high_priority_message(coords: AgentCoordinates, message: str) -> bool:
    """Send a high priority message."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("PyAutoGUI not available - simulating high priority message")
            return True
        move_and_click(*coords.input_box)
        time.sleep(0.5)
        paste_text(f"⚠️ {message}")
        time.sleep(0.5)
        press_enter()
        logger.info("✅ High priority message sent")
        return True
    except Exception as e:  # pragma: no cover - runtime safeguard
        logger.error(f"Failed to send high priority message: {e}")
        return False


def send_urgent_message(coords: AgentCoordinates, message: str) -> bool:
    """Send an urgent message with emphasis."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("PyAutoGUI not available - simulating urgent message")
            return True
        move_and_click(*coords.input_box)
        time.sleep(0.3)
        paste_text(f"🚨 URGENT: {message}")
        time.sleep(0.3)
        press_hotkey("ctrl", "enter")
        logger.info("✅ Urgent message sent")
        return True
    except Exception as e:  # pragma: no cover
        logger.error(f"Failed to send urgent message: {e}")
        return False


def send_onboarding_message(coords: AgentCoordinates, message: str) -> bool:
    """Send an onboarding message using a new chat sequence."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("PyAutoGUI not available - simulating onboarding message")
            return True
        starter_x, starter_y = coords.starter_location
        move_and_click(starter_x, starter_y)
        time.sleep(0.5)
        press_hotkey("ctrl", "n")
        time.sleep(1.0)
        move_and_click(starter_x, starter_y)
        time.sleep(0.5)
        paste_text(message)
        time.sleep(0.5)
        press_enter()
        logger.info("✅ Onboarding message sent")
        return True
    except Exception as e:  # pragma: no cover
        logger.error(f"Failed to send onboarding message: {e}")
        return False


def activate_agent(coords: AgentCoordinates) -> bool:
    """Activate an agent by clicking its starter location."""
    try:
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("PyAutoGUI not available - simulating agent activation")
            return True
        move_and_click(*coords.starter_location)
        logger.info("✅ Agent activated")
        return True
    except Exception as e:  # pragma: no cover
        logger.error(f"Failed to activate agent: {e}")
        return False
