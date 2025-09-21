#!/usr/bin/env python3
"""
Messaging Interfaces Package
===========================

Abstract interfaces for unified messaging system.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from .messaging_interfaces import (
    FileBasedMessageHistoryProvider,
    InboxDeliveryProvider,
    MessageDeliveryProvider,
    MessageHistoryProvider,
    PyAutoGUIDeliveryProvider,
)

__all__ = [
    "MessageDeliveryProvider",
    "PyAutoGUIDeliveryProvider",
    "InboxDeliveryProvider",
    "MessageHistoryProvider",
    "FileBasedMessageHistoryProvider",
]

