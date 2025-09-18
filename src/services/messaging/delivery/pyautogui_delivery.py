"""
Deliveryautogui_Delivery Module

This module provides service functionality for the swarm system.

Component Type: Service
Priority: High
Dependencies: None


EXAMPLE USAGE:
==============

# Import the service
from src.services.messaging.deliveryautogui_delivery import Deliveryautogui_DeliveryService

# Initialize service
service = Deliveryautogui_DeliveryService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Deliveryautogui_DeliveryService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

"""
from __future__ import annotations

import logging
import time

from ..models import UnifiedMessage

logger = logging.getLogger(__name__)


def _lazy_import():
    try:
        import pyautogui as pg  # type: ignore

        try:
            pg.FAILSAFE = False
        except Exception:
            pass
        try:
            import pyperclip as pc  # type: ignore
        except Exception:
            pc = None
        return pg, pc
    except Exception as e:
        raise RuntimeError(f"pyautogui unavailable: {e}")


def _focus_and_clear(pg, x: int, y: int):
    pg.click(x, y, duration=0.4)
    time.sleep(0.05)
# SECURITY: Key placeholder - replace with environment variable
    time.sleep(0.02)
    pg.press("backspace")
    time.sleep(0.02)


def _paste_or_type(pg, pc, text: str):
    if pc is not None:
        try:
            pc.copy(text)
# SECURITY: Key placeholder - replace with environment variable
            return
        except Exception:
            pass
    pg.typewrite(text, interval=0.01)


def deliver_message_pyautogui(message: UnifiedMessage, coords: tuple[int, int], high_priority: bool = False) -> bool:
    pg, pc = _lazy_import()
    x, y = coords
    formatted = f"[{message.sender}] {message.content}"
    
    # Add high priority indicator to message
    if high_priority:
        formatted = f"🚨 HIGH PRIORITY 🚨 {formatted}"
    
    for attempt in range(1, 3):
        try:
            _focus_and_clear(pg, x, y)
            _paste_or_type(pg, pc, formatted)
            time.sleep(0.03)
            
            # Use ctrl+enter for high priority messages to bypass cursor queue
            if high_priority:
                pg.hotkey("ctrl", "enter")
                logger.info(f"[pyautogui] HIGH PRIORITY delivered to {message.recipient} at {coords} (ctrl+enter)")
            else:
                pg.press("enter")
                logger.info(f"[pyautogui] delivered to {message.recipient} at {coords}")
            
            return True
        except Exception as e:
            logger.warning(f"[pyautogui] attempt {attempt} failed: {e}")
            time.sleep(0.3)
    return False
