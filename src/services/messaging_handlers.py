# src/services/messaging_handlers.py
"""
Messaging Handlers for Unified Messaging System
"""

from src.core.messaging_core import UnifiedMessageType, broadcast_message, send_message
from src.services.messaging_cli import MessageCoordinator


def handle_message(content: str, recipient: str, use_pyautogui: bool = False) -> bool:
    """Route and send a message based on the specified delivery method."""
    if use_pyautogui:
        return MessageCoordinator.send_to_agent(recipient, content, use_pyautogui=True)
    return send_message(
        content=content, sender="HANDLER", recipient=recipient, message_type=UnifiedMessageType.TEXT
    )


def handle_broadcast(content: str) -> bool:
    """Broadcast a message to all agents."""
    return broadcast_message(content=content, sender="HANDLER")



