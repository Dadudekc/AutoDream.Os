"""
SSOT Enums - V2 Compliance Micro-refactoring
============================================

Extracted enums for V2 compliance micro-refactoring.
KISS PRINCIPLE: Keep It Simple, Stupid - focused enum definitions.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Micro-refactoring
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from enum import Enum


class SSOTExecutionPhase(Enum):
    """SSOT execution phases."""
    INITIALIZATION = "initialization"
    VALIDATION = "validation"
    EXECUTION = "execution"
    VERIFICATION = "verification"
    COMPLETION = "completion"
    ERROR = "error"


class SSOTValidationLevel(Enum):
    """SSOT validation levels."""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    CRITICAL = "critical"


class SSOTComponentType(Enum):
    """SSOT component types."""
    EXECUTION = "execution"
    VALIDATION = "validation"
    INTEGRATION = "integration"
    MONITORING = "monitoring"
    REPORTING = "reporting"


class SSOTStatus(Enum):
    """SSOT status states."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class SSOTPriority(Enum):
    """SSOT priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
