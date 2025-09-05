"""
Deployment Enums - V2 Compliant Module
=====================================

Enums for deployment operations.
Extracted from deployment_models.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from enum import Enum


class DeploymentStatus(Enum):
    """Deployment status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class PatternType(Enum):
    """Pattern types for deployment coordination."""
    LOGGING = "logging"
    MANAGER = "manager"
    CONFIG = "config"
    INTEGRATION = "integration"
    ANALYTICS = "analytics"


class DeploymentPriority(Enum):
    """Deployment priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DeploymentPhase(Enum):
    """Deployment phases."""
    INITIALIZATION = "initialization"
    PREPARATION = "preparation"
    EXECUTION = "execution"
    VALIDATION = "validation"
    CLEANUP = "cleanup"
    COMPLETION = "completion"


class DeploymentResult(Enum):
    """Deployment result types."""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"
