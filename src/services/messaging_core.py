#!/usr/bin/env python3
"""
Core Messaging Service - Agent Cellphone V2
=========================================

Core messaging functionality for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import os
import time
from typing import List, Dict, Any

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedSenderType,
    UnifiedRecipientType,
)
from .onboarding_service import OnboardingService
from .messaging_pyautogui import PyAutoGUIMessagingDelivery
from ..utils.logger import get_messaging_logger


class UnifiedMessagingCore:
    """Core unified messaging service functionality."""

    def __init__(self):
        """Initialize the core messaging service."""
        self.messages: List[UnifiedMessage] = []
        self.logger = get_messaging_logger()

        # Load configuration from external config files (V2 compliance)
        self._load_configuration()
        # Initialize services
        self.pyautogui_delivery = PyAutoGUIMessagingDelivery(self.agents)
        self.onboarding_service = OnboardingService()

        self.logger.info("UnifiedMessagingCore initialized successfully",
                        extra={"agent_count": len(self.agents), "inbox_paths": len(self.inbox_paths)})
