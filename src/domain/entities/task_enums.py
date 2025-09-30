"""
Task Enums - V2 Compliant
=========================

Task-related enumerations separated for V2 compliance.
Maintains single responsibility principle.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
from enum import Enum


class TaskStatus(Enum):
    """Task status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority enumeration."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(Enum):
    """Task type enumeration."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    SYSTEM = "system"
