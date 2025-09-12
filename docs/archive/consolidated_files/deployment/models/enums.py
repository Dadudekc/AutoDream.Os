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
