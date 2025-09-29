#!/usr/bin/env python3
"""
Messaging Providers Package
==========================

Message delivery providers for unified messaging system.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from ..delivery.inbox_delivery import send_message_inbox as InboxMessageDelivery
from ..delivery.pyautogui_delivery import deliver_message_pyautogui as PyAutoGUIMessageDelivery

__all__ = [
    "InboxMessageDelivery",
    "PyAutoGUIMessageDelivery",
]
