#!/usr/bin/env python3
"""
Unified Enums - Consolidated Type Definitions
============================================

Consolidates all duplicate enum definitions from across the codebase into a single source of truth.
Eliminates SSOT violations by providing unified types for all systems.

This file consolidates enums from:
- src/core/workflow/types/workflow_enums.py
- src/core/health/types/health_types.py
- src/core/api_integration/types/api_types.py
- src/core/performance/types/enums.py
- src/services/messaging/types/v2_message_enums.py
- Multiple scattered enum definitions throughout the codebase

Agent: Agent-8 (Type Systems Consolidation Specialist)
Mission: CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders
Priority: CRITICAL - Above all other work
Status: IMPLEMENTATION PHASE 1 - Unified Type Registry

Author: Agent-8 - Integration Enhancement Optimization Manager
License: MIT
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime


# ============================================================================
# WORKFLOW AND TASK MANAGEMENT ENUMS
# ============================================================================

class WorkflowStatus(Enum):
    """Unified workflow execution status - consolidated from multiple sources"""
    
    # Core workflow states
    CREATED = "created"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    PLANNING = "planning"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    EXECUTING = "executing"
    RUNNING = "running"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ERROR = "error"
    
    # V2 specific states
    VALIDATING = "validating"
    OPTIMIZING = "optimizing"
    SCALING = "scaling"
    RECOVERING = "recovering"
    
    @classmethod
    def get_transition_map(cls) -> Dict[str, List[str]]:
        """Get valid status transitions"""
        return {
            cls.CREATED.value: [cls.INITIALIZING.value, cls.PLANNING.value],
            cls.INITIALIZING.value: [cls.INITIALIZED.value, cls.FAILED.value],
            cls.INITIALIZED.value: [cls.PLANNING.value, cls.PENDING.value],
            cls.PLANNING.value: [cls.PENDING.value, cls.FAILED.value],
            cls.PENDING.value: [cls.IN_PROGRESS.value, cls.CANCELLED.value],
            cls.IN_PROGRESS.value: [cls.EXECUTING.value, cls.FAILED.value],
            cls.EXECUTING.value: [cls.RUNNING.value, cls.FAILED.value, cls.PAUSED.value],
            cls.RUNNING.value: [cls.ACTIVE.value, cls.PAUSED.value, cls.FAILED.value],
            cls.ACTIVE.value: [cls.COMPLETED.value, cls.PAUSED.value, cls.FAILED.value],
            cls.PAUSED.value: [cls.ACTIVE.value, cls.CANCELLED.value],
            cls.VALIDATING.value: [cls.ACTIVE.value, cls.FAILED.value],
            cls.OPTIMIZING.value: [cls.ACTIVE.value, cls.FAILED.value],
            cls.SCALING.value: [cls.ACTIVE.value, cls.FAILED.value],
            cls.RECOVERING.value: [cls.ACTIVE.value, cls.FAILED.value],
            cls.COMPLETED.value: [],
            cls.FAILED.value: [cls.RECOVERING.value, cls.CANCELLED.value],
            cls.CANCELLED.value: [],
            cls.ERROR.value: [cls.RECOVERING.value, cls.CANCELLED.value]
        }


class TaskStatus(Enum):
    """Unified task status - consolidated from multiple sources"""
    
    # Core task states
    PENDING = "pending"
    QUEUED = "queued"
    ASSIGNED = "assigned"
    RUNNING = "running"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    
    # V2 specific states
    VALIDATING = "validating"
    RETRYING = "retrying"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    
    @classmethod
    def is_terminal(cls, status: 'TaskStatus') -> bool:
        """Check if status is terminal (no further transitions)"""
        return status in [cls.COMPLETED, cls.FAILED, cls.CANCELLED, cls.SKIPPED]
    
    @classmethod
    def is_active(cls, status: 'TaskStatus') -> bool:
        """Check if status indicates active execution"""
        return status in [cls.RUNNING, cls.EXECUTING, cls.VALIDATING]


class TaskPriority(Enum):
    """Unified task priority - consolidated from multiple sources"""
    
    # Core priorities
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"
    
    # V2 specific priorities
    EMERGENCY = "emergency"
    OPTIMIZATION = "optimization"
    MAINTENANCE = "maintenance"
    
    @classmethod
    def get_numeric_value(cls, priority: 'TaskPriority') -> int:
        """Get numeric value for priority comparison"""
        priority_map = {
            cls.LOW: 1,
            cls.NORMAL: 2,
            cls.HIGH: 3,
            cls.URGENT: 4,
            cls.CRITICAL: 5,
            cls.EMERGENCY: 6,
            cls.OPTIMIZATION: 2,
            cls.MAINTENANCE: 1
        }
        return priority_map.get(priority, 2)


class TaskType(Enum):
    """Unified task types - consolidated from multiple sources"""
    
    # Core task types
    COMPUTATION = "computation"
    DATA_PROCESSING = "data_processing"
    VALIDATION = "validation"
    MONITORING = "monitoring"
    REPORTING = "reporting"
    
    # V2 specific types
    CONSOLIDATION = "consolidation"
    OPTIMIZATION = "optimization"
    MIGRATION = "migration"
    INTEGRATION = "integration"
    TESTING = "testing"


class WorkflowType(Enum):
    """Unified workflow types - consolidated from multiple sources"""
    
    # Core workflow types
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    ERROR_HANDLING = "error_handling"
    
    # V2 specific types
    CONSOLIDATION = "consolidation"
    OPTIMIZATION = "optimization"
    MIGRATION = "migration"
    VALIDATION = "validation"


class ExecutionStrategy(Enum):
    """Unified execution strategies - consolidated from multiple sources"""
    
    # Core strategies
    IMMEDIATE = "immediate"
    SCHEDULED = "scheduled"
    ON_DEMAND = "on_demand"
    BATCH = "batch"
    
    # V2 specific strategies
    OPTIMIZED = "optimized"
    ADAPTIVE = "adaptive"
    INTELLIGENT = "intelligent"


# ============================================================================
# HEALTH AND PERFORMANCE ENUMS
# ============================================================================

class HealthLevel(Enum):
    """Unified health levels - consolidated from multiple sources"""
    
    # Core health levels
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"
    
    # V2 specific levels
    OPTIMAL = "optimal"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"
    ERROR = "error"
    
    @classmethod
    def get_numeric_value(cls, level: 'HealthLevel') -> int:
        """Get numeric value for health comparison"""
        health_map = {
            cls.EXCELLENT: 100,
            cls.OPTIMAL: 95,
            cls.GOOD: 80,
            cls.DEGRADED: 60,
            cls.WARNING: 40,
            cls.UNHEALTHY: 20,
            cls.CRITICAL: 10,
            cls.EMERGENCY: 5,
            cls.ERROR: 0,
            cls.OFFLINE: -1
        }
        return health_map.get(level, 50)


class AlertType(Enum):
    """Unified alert types - consolidated from multiple sources"""
    
    # Core alert types
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    EMERGENCY = "emergency"
    
    # V2 specific types
    OPTIMIZATION = "optimization"
    CONSOLIDATION = "consolidation"
    MIGRATION = "migration"
    VALIDATION = "validation"


class PerformanceLevel(Enum):
    """Unified performance levels - consolidated from multiple sources"""
    
    # Core performance levels
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    UNACCEPTABLE = "unacceptable"
    
    # V2 specific levels
    OPTIMAL = "optimal"
    SUBOPTIMAL = "suboptimal"
    DEGRADED = "degraded"


class BenchmarkType(Enum):
    """Unified benchmark types - consolidated from multiple sources"""
    
    # Core benchmark types
    PERFORMANCE = "performance"
    MEMORY = "memory"
    CPU = "cpu"
    NETWORK = "network"
    STORAGE = "storage"
    
    # V2 specific types
    CONSOLIDATION = "consolidation"
    OPTIMIZATION = "optimization"
    MIGRATION = "migration"


# ============================================================================
# API AND SERVICE MANAGEMENT ENUMS
# ============================================================================

class ServiceStatus(Enum):
    """Unified service status - consolidated from multiple sources"""
    
    # Core service statuses
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    OFFLINE = "offline"
    ERROR = "error"
    
    # V2 specific statuses
    OPTIMIZING = "optimizing"
    CONSOLIDATING = "consolidating"
    MIGRATING = "migrating"


class HTTPMethod(Enum):
    """Unified HTTP methods - consolidated from multiple sources"""
    
    # Standard HTTP methods
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    
    # V2 specific methods
    CONSOLIDATE = "CONSOLIDATE"
    OPTIMIZE = "OPTIMIZE"
    MIGRATE = "MIGRATE"


class AuthenticationLevel(Enum):
    """Unified authentication levels - consolidated from multiple sources"""
    
    # Core authentication levels
    NONE = "none"
    BASIC = "basic"
    TOKEN = "token"
    JWT = "jwt"
    OAUTH = "oauth"
    API_KEY = "api_key"
    
    # V2 specific levels
    MULTI_FACTOR = "multi_factor"
    BIOMETRIC = "biometric"
    SMART_CARD = "smart_card"


class RateLimitType(Enum):
    """Unified rate limiting types - consolidated from multiple sources"""
    
    # Core rate limit types
    NONE = "none"
    PER_SECOND = "per_second"
    PER_MINUTE = "per_minute"
    PER_HOUR = "per_hour"
    PER_DAY = "per_day"
    
    # V2 specific types
    ADAPTIVE = "adaptive"
    INTELLIGENT = "intelligent"
    BURST = "burst"


# ============================================================================
# VALIDATION AND ERROR HANDLING ENUMS
# ============================================================================

class ValidationSeverity(Enum):
    """Unified validation severity - consolidated from multiple sources"""
    
    # Core severity levels
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    
    # V2 specific levels
    OPTIMIZATION = "optimization"
    CONSOLIDATION = "consolidation"
    MIGRATION = "migration"


class ValidationStatus(Enum):
    """Unified validation status - consolidated from multiple sources"""
    
    # Core validation statuses
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    
    # V2 specific statuses
    OPTIMIZED = "optimized"
    CONSOLIDATED = "consolidated"
    MIGRATED = "migrated"


class ErrorSeverity(Enum):
    """Unified error severity - consolidated from multiple sources"""
    
    # Core error severities
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
    # V2 specific severities
    OPTIMIZATION = "optimization"
    CONSOLIDATION = "consolidation"
    MIGRATION = "migration"


class ComplianceLevel(Enum):
    """Unified compliance levels - consolidated from multiple sources"""
    
    # Core compliance levels
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    COMPLIANT = "compliant"
    FULLY_COMPLIANT = "fully_compliant"
    
    # V2 specific levels
    OPTIMIZED = "optimized"
    CONSOLIDATED = "consolidated"
    MIGRATED = "migrated"


# ============================================================================
# COMMUNICATION AND COORDINATION ENUMS
# ============================================================================

class MessagePriority(Enum):
    """Unified message priority - consolidated from multiple sources"""
    
    # Core message priorities
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"
    
    # V2 specific priorities
    OPTIMIZATION = "optimization"
    CONSOLIDATION = "consolidation"
    MIGRATION = "migration"


class MessageStatus(Enum):
    """Unified message status - consolidated from multiple sources"""
    
    # Core message statuses
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    
    # V2 specific statuses
    OPTIMIZED = "optimized"
    CONSOLIDATED = "consolidated"
    MIGRATED = "migrated"


class CoordinationMode(Enum):
    """Unified coordination modes - consolidated from multiple sources"""
    
    # Core coordination modes
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    BATCH = "batch"
    STREAMING = "streaming"
    
    # V2 specific modes
    OPTIMIZED = "optimized"
    INTELLIGENT = "intelligent"
    ADAPTIVE = "adaptive"


class NotificationType(Enum):
    """Unified notification types - consolidated from multiple sources"""
    
    # Core notification types
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    SLACK = "slack"
    DISCORD = "discord"
    LOG = "log"
    
    # V2 specific types
    OPTIMIZATION = "optimization"
    CONSOLIDATION = "consolidation"
    MIGRATION = "migration"


# ============================================================================
# SYSTEM AND INFRASTRUCTURE ENUMS
# ============================================================================

class SystemStatus(Enum):
    """Unified system status - consolidated from multiple sources"""
    
    # Core system statuses
    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
    ERROR = "error"
    
    # V2 specific statuses
    OPTIMIZING = "optimizing"
    CONSOLIDATING = "consolidating"
    MIGRATING = "migrating"


class ResourceType(Enum):
    """Unified resource types - consolidated from multiple sources"""
    
    # Core resource types
    CPU = "cpu"
    MEMORY = "memory"
    STORAGE = "storage"
    NETWORK = "network"
    DATABASE = "database"
    
    # V2 specific types
    OPTIMIZATION = "optimization"
    CONSOLIDATION = "consolidation"
    MIGRATION = "migration"


class SecurityLevel(Enum):
    """Unified security levels - consolidated from multiple sources"""
    
    # Core security levels
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"
    
    # V2 specific levels
    OPTIMIZED = "optimized"
    CONSOLIDATED = "consolidated"
    MIGRATED = "migrated"


class MonitoringType(Enum):
    """Unified monitoring types - consolidated from multiple sources"""
    
    # Core monitoring types
    PERFORMANCE = "performance"
    HEALTH = "health"
    SECURITY = "security"
    BUSINESS = "business"
    
    # V2 specific types
    OPTIMIZATION = "optimization"
    CONSOLIDATION = "consolidation"
    MIGRATION = "migration"


# ============================================================================
# CONSOLIDATION STATUS ENUMS
# ============================================================================

class ConsolidationStatus(Enum):
    """Consolidation status for tracking SSOT consolidation progress"""
    
    # Core consolidation statuses
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    
    # V2 specific statuses
    OPTIMIZED = "optimized"
    VALIDATED = "validated"
    DEPLOYED = "deployed"


class ConsolidationTarget(Enum):
    """Consolidation targets for SSOT consolidation mission"""
    
    # Core consolidation targets
    TYPE_SYSTEMS = "type_systems"
    WORKFLOW_SYSTEMS = "workflow_systems"
    VALIDATION_SYSTEMS = "validation_systems"
    API_SYSTEMS = "api_systems"
    
    # V2 specific targets
    PERFORMANCE_SYSTEMS = "performance_systems"
    HEALTH_SYSTEMS = "health_systems"
    COMMUNICATION_SYSTEMS = "communication_systems"


# ============================================================================
# UTILITY METHODS
# ============================================================================

def get_all_enums() -> Dict[str, Enum]:
    """Get all enum classes for dynamic access"""
    return {
        name: value for name, value in globals().items()
        if isinstance(value, type) and issubclass(value, Enum) and value != Enum
    }


def get_enum_by_name(name: str) -> Optional[Enum]:
    """Get enum class by name"""
    enums = get_all_enums()
    return enums.get(name)


def get_enum_values(enum_name: str) -> Optional[List[str]]:
    """Get all values for a specific enum"""
    enum_class = get_enum_by_name(enum_name)
    if enum_class:
        return [e.value for e in enum_class]
    return None


def validate_enum_value(enum_name: str, value: str) -> bool:
    """Validate if a value is valid for a specific enum"""
    enum_values = get_enum_values(enum_name)
    if enum_values:
        return value in enum_values
    return False
