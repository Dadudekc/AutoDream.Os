#!/usr/bin/env python3
"""
🚨 DEPRECATED - PyAutoGUI Messaging Delivery
===========================================

⚠️  MIGRATION NOTICE: This file has been MIGRATED to the new unified messaging system.
🔄 NEW LOCATION: src/core/messaging/delivery/pyautogui.py
📦 This stub file exists only for backward compatibility during the migration period.

🔄 UPDATE IMPORTS: from src.core.messaging.delivery.pyautogui import ...

V2 Compliance: Single Source of Truth (SSOT) Implementation
Migration Status: LEGACY FILE - UPDATE IMPORTS IMMEDIATELY

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

import warnings
warnings.warn(
    "src.core.messaging_pyautogui is deprecated. "
    "Use src.core.messaging.delivery.pyautogui instead (Single Source of Truth). "
    "Update your imports: from src.core.messaging.delivery.pyautogui import ...",
    DeprecationWarning,
    stacklevel=2
)

# Import from new unified messaging system
from src.core.messaging.delivery.pyautogui import *