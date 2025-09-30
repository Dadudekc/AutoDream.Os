#!/usr/bin/env python3
"""
Messaging Module - V2 Compliant Messaging Services
================================================

Modular messaging services extracted for V2 compliance.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from .consolidated_messaging_service_v2 import ConsolidatedMessagingServiceV2
from .coordination_tracker import CoordinationTracker
from .message_validator import MessageValidator
from .messaging_core import MessagingCore
from .pyautogui_handler import PyAutoGUIHandler

__all__ = [
    "MessagingCore",
    "CoordinationTracker",
    "PyAutoGUIHandler",
    "MessageValidator",
    "ConsolidatedMessagingServiceV2",
]
