"""
Fallback Module

This module provides service functionality for the swarm system.

Component Type: Service
Priority: High
Dependencies: None


EXAMPLE USAGE:
==============

# Import the service
from src.services.messaging.delivery.fallback import FallbackService

# Initialize service
service = FallbackService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(FallbackService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

"""
from __future__ import annotations

import logging

from ..coordinates import get_agent_coordinates, list_agents
from ..models import UnifiedMessage
from .inbox_delivery import send_message_inbox
from .pyautogui_delivery import deliver_message_pyautogui

logger = logging.getLogger(__name__)


def send_with_fallback(message: UnifiedMessage, high_priority: bool = False) -> bool:
    coords = get_agent_coordinates(message.recipient)
    if coords:
        try:
            if deliver_message_pyautogui(message, coords, high_priority=high_priority):
                return True
        except Exception as e:
            logger.warning(f"[fallback] pyautogui path failed: {e}")
    logger.info(f"[fallback] using inbox for {message.recipient}")
    return send_message_inbox(message)


def broadcast(content: str, sender: str) -> dict[str, bool]:
    results: dict[str, bool] = {}
    for agent in list_agents():
        m = UnifiedMessage(
            content=content,
            sender=sender,
            recipient=agent,
            message_type=...,  # type: ignore
        )
        # keep type minimal; delivery doesn’t depend on it
        ok = send_with_fallback(m)
        results[agent] = ok
    return results
