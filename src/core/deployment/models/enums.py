import logging

logger = logging.getLogger(__name__)
"""
Deployment Enums - V2 Compliant Module
======================================

Enums for deployment operations.
Extracted for V2 compliance and better organization.

V2 Compliance: Single responsibility, < 100 lines.

Author: Agent-2 - Infrastructure Specialist (Phase 2 Restoration)
License: MIT
"""

from enum import Enum


class DeploymentPriority(Enum):
    """Deployment priority levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PatternType(Enum):

EXAMPLE USAGE:
==============

# Import the core component
from src.core.deployment.models.enums import Enums

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Enums(config)

# Execute primary functionality
result = component.process_data(input_data)
logger.info(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    logger.info(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    logger.info(f"Operation failed: {e}")
    # Implement recovery logic

    """Types of patterns for deployment."""

    LOGGING = "logging"
    MANAGER = "manager"
    CONFIG = "config"
    INTEGRATION = "integration"
    ANALYTICS = "analytics"


class DeploymentStatus(Enum):
    """Deployment status values."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
