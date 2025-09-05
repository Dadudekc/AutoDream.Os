"""
Integration Enums - V2 Compliance Micro-refactoring
==================================================

Extracted enums for V2 compliance micro-refactoring.
KISS PRINCIPLE: Keep It Simple, Stupid - focused enum definitions.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Micro-refactoring
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from enum import Enum


class IntegrationType(Enum):
    """Types of system integrations."""
    MESSAGING = "messaging"
    VECTOR_DATABASE = "vector_database"
    VALIDATION = "validation"
    LOGGING = "logging"
    CACHING = "caching"
    MONITORING = "monitoring"


class OptimizationLevel(Enum):
    """Optimization levels."""
    NONE = "none"
    BASIC = "basic"
    ADVANCED = "advanced"
    MAXIMUM = "maximum"


class IntegrationStatus(Enum):
    """Integration status states."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    OPTIMIZING = "optimizing"
    MAINTENANCE = "maintenance"


class IntegrationPriority(Enum):
    """Integration priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IntegrationMode(Enum):
    """Integration operation modes."""
    SYNC = "sync"
    ASYNC = "async"
    BATCH = "batch"
    STREAM = "stream"
