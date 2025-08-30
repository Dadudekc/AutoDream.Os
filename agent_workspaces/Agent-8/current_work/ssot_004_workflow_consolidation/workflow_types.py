#!/usr/bin/env python3
"""
Workflow Types - SSOT-004 Implementation

Type definitions and enums for unified workflow system.
Maintains V2 compliance with modular architecture.

Author: Agent-8 (Integration Enhancement Optimization Manager)
Contract: SSOT-004: Workflow & Reporting System Consolidation
License: MIT
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


class WorkflowType(Enum):
    """Workflow type enumeration."""
    BUSINESS_PROCESS = "business_process"
    DATA_PROCESSING = "data_processing"
    SYSTEM_INTEGRATION = "system_integration"
    TESTING = "testing"
    VALIDATION = "validation"
    REPORTING = "reporting"
    CLEANUP = "cleanup"
    CUSTOM = "custom"


class WorkflowStatus(Enum):
    """Workflow status enumeration."""
    CREATED = "CREATED"
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    EXECUTING = "EXECUTING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ERROR = "ERROR"


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"
    SKIPPED = "SKIPPED"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class ExecutionStrategy(Enum):
    """Workflow execution strategy."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    HYBRID = "hybrid"


class ResourceType(Enum):
    """Resource type enumeration."""
    CPU = "cpu"
    MEMORY = "memory"
    STORAGE = "storage"
    NETWORK = "network"
    DATABASE = "database"
    EXTERNAL_API = "external_api"
    FILE_SYSTEM = "file_system"


class ValidationLevel(Enum):
    """Validation level enumeration."""
    NONE = "none"
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    CUSTOM = "custom"


class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    FATAL = "fatal"


class WorkflowCategory(Enum):
    """Workflow category enumeration."""
    CORE = "core"
    BUSINESS = "business"
    TECHNICAL = "technical"
    ADMINISTRATIVE = "administrative"
    MONITORING = "monitoring"
    MAINTENANCE = "maintenance"


class DataFormat(Enum):
    """Data format enumeration."""
    JSON = "json"
    XML = "xml"
    YAML = "yaml"
    CSV = "csv"
    BINARY = "binary"
    TEXT = "text"
    CUSTOM = "custom"


class AuthenticationType(Enum):
    """Authentication type enumeration."""
    NONE = "none"
    BASIC = "basic"
    TOKEN = "token"
    OAUTH = "oauth"
    API_KEY = "api_key"
    CUSTOM = "custom"


class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class WorkflowPhase(Enum):
    """Workflow execution phase."""
    INITIALIZATION = "initialization"
    VALIDATION = "validation"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    CLEANUP = "cleanup"
    COMPLETION = "completion"


class RetryPolicy(Enum):
    """Retry policy types."""
    NONE = "none"
    IMMEDIATE = "immediate"
    LINEAR_BACKOFF = "linear_backoff"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    CUSTOM = "custom"


class TimeoutPolicy(Enum):
    """Timeout policy types."""
    NONE = "none"
    SOFT = "soft"
    HARD = "hard"
    GRACEFUL = "graceful"
    AGGRESSIVE = "aggressive"


class WorkflowComplexity(Enum):
    """Workflow complexity levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"
    EXTREME = "extreme"


class PerformanceTier(Enum):
    """Performance tier levels."""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class SecurityLevel(Enum):
    """Security level enumeration."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    CLASSIFIED = "classified"


class ComplianceLevel(Enum):
    """Compliance level enumeration."""
    NONE = "none"
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    CERTIFIED = "certified"


class WorkflowVersion(Enum):
    """Workflow version status."""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    EXPERIMENTAL = "experimental"


class IntegrationType(Enum):
    """Integration type enumeration."""
    NONE = "none"
    API = "api"
    DATABASE = "database"
    FILE = "file"
    MESSAGE_QUEUE = "message_queue"
    WEBHOOK = "webhook"
    CUSTOM = "custom"


class MonitoringType(Enum):
    """Monitoring type enumeration."""
    NONE = "none"
    BASIC = "basic"
    ADVANCED = "advanced"
    REAL_TIME = "real_time"
    PREDICTIVE = "predictive"
    CUSTOM = "custom"


class BackupPolicy(Enum):
    """Backup policy types."""
    NONE = "none"
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    CONTINUOUS = "continuous"
    INCREMENTAL = "incremental"
    CUSTOM = "custom"


class RollbackPolicy(Enum):
    """Rollback policy types."""
    NONE = "none"
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    GRADUAL = "gradual"
    IMMEDIATE = "immediate"
    CUSTOM = "custom"


class NotificationType(Enum):
    """Notification type enumeration."""
    NONE = "none"
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    DASHBOARD = "dashboard"
    LOG = "log"
    CUSTOM = "custom"


class WorkflowTag(Enum):
    """Common workflow tags."""
    CRITICAL = "critical"
    HIGH_PRIORITY = "high_priority"
    LOW_PRIORITY = "low_priority"
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    TESTING = "testing"
    MAINTENANCE = "maintenance"
    EMERGENCY = "emergency"
    SCHEDULED = "scheduled"
    ON_DEMAND = "on_demand"


class DataSourceType(Enum):
    """Data source type enumeration."""
    DATABASE = "database"
    FILE = "file"
    API = "api"
    MESSAGE_QUEUE = "message_queue"
    STREAM = "stream"
    CACHE = "cache"
    EXTERNAL = "external"
    CUSTOM = "custom"


class OutputFormat(Enum):
    """Output format enumeration."""
    JSON = "json"
    XML = "xml"
    YAML = "yaml"
    CSV = "csv"
    HTML = "html"
    PDF = "pdf"
    EXCEL = "excel"
    CUSTOM = "custom"


class WorkflowTemplate(Enum):
    """Predefined workflow templates."""
    DATA_PIPELINE = "data_pipeline"
    ETL_PROCESS = "etl_process"
    VALIDATION_WORKFLOW = "validation_workflow"
    REPORTING_WORKFLOW = "reporting_workflow"
    INTEGRATION_WORKFLOW = "integration_workflow"
    CLEANUP_WORKFLOW = "cleanup_workflow"
    MONITORING_WORKFLOW = "monitoring_workflow"
    CUSTOM_WORKFLOW = "custom_workflow"


class WorkflowPermission(Enum):
    """Workflow permission levels."""
    NONE = "none"
    READ = "read"
    EXECUTE = "execute"
    MODIFY = "modify"
    ADMIN = "admin"
    OWNER = "owner"


class WorkflowScope(Enum):
    """Workflow scope levels."""
    LOCAL = "local"
    TEAM = "team"
    DEPARTMENT = "department"
    ORGANIZATION = "organization"
    GLOBAL = "global"
    CUSTOM = "custom"


class WorkflowLifecycle(Enum):
    """Workflow lifecycle stages."""
    DESIGN = "design"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    PRODUCTION = "production"
    MAINTENANCE = "maintenance"
    RETIREMENT = "retirement"


class WorkflowMetric(Enum):
    """Workflow metric types."""
    EXECUTION_TIME = "execution_time"
    SUCCESS_RATE = "success_rate"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    LATENCY = "latency"
    RESOURCE_USAGE = "resource_usage"
    COST = "cost"
    CUSTOM = "custom"


class WorkflowAlert(Enum):
    """Workflow alert types."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    SUCCESS = "success"
    CUSTOM = "custom"


class WorkflowSchedule(Enum):
    """Workflow schedule types."""
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    EVENT_DRIVEN = "event_driven"
    CONDITIONAL = "conditional"
    CONTINUOUS = "continuous"
    CUSTOM = "custom"


class WorkflowDependency(Enum):
    """Workflow dependency types."""
    NONE = "none"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    RESOURCE = "resource"
    DATA = "data"
    CUSTOM = "custom"
