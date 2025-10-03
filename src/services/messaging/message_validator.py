#!/usr/bin/env python3
"""
Message Validator - V2 Compliant Message Validation
=================================================

Message validation module for the messaging system.
Imports and exposes the MessageValidator from consolidated messaging service utils.

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
    from src.services.consolidated_messaging_service_utils import MessageValidator
except ImportError as e:
    logging.error(f"Failed to import MessageValidator: {e}")
    MessageValidator = None

logger = logging.getLogger(__name__)

# Re-export MessageValidator for messaging module
__all__ = ["MessageValidator"]

if MessageValidator is None:
    logger.warning("MessageValidator not available - messaging validation will be limited")
else:
    logger.info("MessageValidator module loaded successfully")
