"""
Interface Enums - V2 Compliance Micro-refactoring
=================================================

Extracted enums for V2 compliance micro-refactoring.
Reduces models.py line count by extracting enum definitions.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Micro-refactoring
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from enum import Enum


class InterfaceType(Enum):
    """Interface types for V2 compliance system."""
    SERVICE = "service"
    REPOSITORY = "repository"
    VALIDATOR = "validator"
    ORCHESTRATOR = "orchestrator"
    ENGINE = "engine"
    HANDLER = "handler"
    UTILITY = "utility"
    CORE = "core"


class InterfaceStatus(Enum):
    """Interface status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    PENDING = "pending"


class InterfacePriority(Enum):
    """Interface priority."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ValidationLevel(Enum):
    """Validation level."""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    COMPREHENSIVE = "comprehensive"


class InterfaceCategory(Enum):
    """Interface category."""
    CORE = "core"
    INTEGRATION = "integration"
    UTILITY = "utility"
    SERVICE = "service"
    DATA = "data"
    COMMUNICATION = "communication"
