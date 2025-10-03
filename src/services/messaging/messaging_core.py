#!/usr/bin/env python3
"""
Messaging Core - V2 Compliant Core Messaging
===========================================

Core messaging functionality for the messaging system.
Imports and exposes the MessagingService from core messaging service.

Author: Agent-4 (Captain)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.services.messaging.core.messaging_service import MessagingService

    MessagingCore = MessagingService  # Alias for compatibility
except ImportError as e:
    logging.error(f"Failed to import MessagingService: {e}")
    MessagingCore = None

logger = logging.getLogger(__name__)

# Re-export MessagingCore for messaging module
__all__ = ["MessagingCore"]

if MessagingCore is None:
    logger.warning("MessagingCore not available - core messaging will be limited")
else:
    logger.info("MessagingCore module loaded successfully")
