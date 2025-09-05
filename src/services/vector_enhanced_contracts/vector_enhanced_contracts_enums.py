#!/usr/bin/env python3
"""
Vector Enhanced Contracts Enums - V2 Compliance Module
======================================================

Enums for vector enhanced contracts operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from enum import Enum


class ContractStatus(Enum):
    """Contract status enumeration."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class PriorityLevel(Enum):
    """Priority level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(Enum):
    """Task type enumeration."""
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    OPTIMIZATION = "optimization"
    INTEGRATION = "integration"
    DEBUGGING = "debugging"
    FEATURE_DEVELOPMENT = "feature_development"
    MAINTENANCE = "maintenance"


class AssignmentStrategy(Enum):
    """Assignment strategy enumeration."""
    ROUND_ROBIN = "round_robin"
    CAPABILITY_BASED = "capability_based"
    LOAD_BALANCED = "load_balanced"
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    RANDOM = "random"
