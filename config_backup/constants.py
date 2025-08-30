"""
Unified Configuration Constants - Single Source of Truth (SSOT)

This module centralizes all configuration constants to eliminate duplication
and ensure consistency across the entire system.

Author: Agent-6 & Agent-8
Contract: SSOT-003: Configuration Management Consolidation
Date: 2025-08-28 (Updated 2025-01-27)
"""

from typing import Dict, Any, List

# =============================================================================
# TIMEOUT CONFIGURATIONS
# =============================================================================

# Standard timeout values (in seconds)
DEFAULT_TIMEOUT = 30.0
SHORT_TIMEOUT = 10.0
LONG_TIMEOUT = 60.0
CRITICAL_TIMEOUT = 300.0
EXTENDED_TIMEOUT = 600.0
URGENT_TIMEOUT = 5.0

# Communication-specific timeouts
COMMUNICATION_TIMEOUT = 30.0
KEEPALIVE_TIMEOUT = 60.0
PING_TIMEOUT = 10.0
CONNECTION_TIMEOUT = 30.0
IDLE_TIMEOUT = 300.0
SHUTDOWN_TIMEOUT = 30.0

# Service-specific timeouts
API_TIMEOUT = 30.0
SERVICE_TIMEOUT = 10.0
RECOVERY_TIMEOUT = 60.0
VALIDATION_TIMEOUT = 300.0
TEST_TIMEOUT = 300.0

# =============================================================================
# RETRY CONFIGURATIONS
# =============================================================================

# Standard retry settings
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 1.0
MAX_RETRY_ATTEMPTS = 5
MIN_RETRY_DELAY = 0.5
MAX_RETRY_DELAY = 30.0

# Service-specific retry settings
MESSAGE_RETRY_ATTEMPTS = 3
MESSAGE_RETRY_DELAY = 2.0
FSM_RETRY_ATTEMPTS = 3
FSM_RETRY_DELAY = 5.0
INTEGRATION_RETRY_ATTEMPTS = 3
INTEGRATION_RETRY_DELAY = 1.0

# =============================================================================
# COLLECTION INTERVALS
# =============================================================================

# Monitoring collection intervals (in seconds)
DEFAULT_COLLECTION_INTERVAL = 60
LONG_COLLECTION_INTERVAL = 120
SHORT_COLLECTION_INTERVAL = 15
URGENT_COLLECTION_INTERVAL = 5
EXTENDED_COLLECTION_INTERVAL = 300

# Component-specific intervals
SYSTEM_METRICS_INTERVAL = 60
APPLICATION_METRICS_INTERVAL = 60
NETWORK_METRICS_INTERVAL = 60
CUSTOM_METRICS_INTERVAL = 120
COMMUNICATION_METRICS_INTERVAL = 15.0

# =============================================================================
# ENABLE/DISABLE FLAGS
# =============================================================================

# System features
SYSTEM_ENABLED = True
SYSTEM_DISABLED = False

# Monitoring features
MONITORING_ENABLED = True
PERFORMANCE_MONITORING_ENABLED = True
ALERTING_ENABLED = True
DASHBOARD_ENABLED = True

# Communication features
COMMUNICATION_ENABLED = True
BROADCAST_ENABLED = True
PRIVATE_MESSAGING_ENABLED = True
COMPRESSION_ENABLED = False

# Security features
AUTHORIZATION_ENABLED = False
ENCRYPTION_ENABLED = False
AUTHENTICATION_ENABLED = False
RATE_LIMITING_ENABLED = False

# Development features
DEBUG_MODE_ENABLED = False
HOT_RELOAD_ENABLED = False
TESTING_ENABLED = False
MOCK_SERVICES_ENABLED = False

# =============================================================================
# PERFORMANCE THRESHOLDS
# =============================================================================

# Memory thresholds (percentage)
MEMORY_WARNING_THRESHOLD = 80
MEMORY_CRITICAL_THRESHOLD = 95

# Network thresholds (percentage)
NETWORK_WARNING_THRESHOLD = 80
NETWORK_CRITICAL_THRESHOLD = 95

# CPU thresholds (percentage)
CPU_WARNING_THRESHOLD = 80
CPU_CRITICAL_THRESHOLD = 95

# Disk thresholds (percentage)
DISK_WARNING_THRESHOLD = 80
DISK_CRITICAL_THRESHOLD = 95

# =============================================================================
# QUEUE AND BATCH SETTINGS
# =============================================================================

# Queue sizes
DEFAULT_QUEUE_SIZE = 1000
MAX_QUEUE_SIZE = 10000
MIN_QUEUE_SIZE = 100

# Batch processing
MAX_BATCH_SIZE = 1000
DEFAULT_BATCH_SIZE = 100
MIN_BATCH_SIZE = 10

# =============================================================================
# PRIORITY LEVELS
# =============================================================================

# Priority constants
PRIORITY_LOW = 1
PRIORITY_NORMAL = 2
PRIORITY_HIGH = 3
PRIORITY_CRITICAL = 4
PRIORITY_EMERGENCY = 5

# Priority names
PRIORITY_NAMES = {
    PRIORITY_LOW: "low",
    PRIORITY_NORMAL: "normal", 
    PRIORITY_HIGH: "high",
    PRIORITY_CRITICAL: "critical",
    PRIORITY_EMERGENCY: "emergency"
}

# =============================================================================
# DATA TYPES AND SCHEMAS
# =============================================================================

# JSON Schema types
SCHEMA_TYPE_STRING = "string"
SCHEMA_TYPE_OBJECT = "object"
SCHEMA_TYPE_ARRAY = "array"
SCHEMA_TYPE_BOOLEAN = "boolean"
SCHEMA_TYPE_NUMBER = "number"
SCHEMA_TYPE_INTEGER = "integer"

# Common string values
STRING_PRIMARY = "primary"
STRING_SECONDARY = "secondary"
STRING_PASS = "pass"
STRING_FAIL = "fail"
STRING_TEST = "test"
STRING_GATED = "gated"

# =============================================================================
# NUMERIC CONSTANTS
# =============================================================================

# Common numeric values
VALUE_ZERO = 0
VALUE_ONE = 1
VALUE_TWO = 2
VALUE_THREE = 3
VALUE_FIVE = 5
VALUE_TEN = 10
VALUE_THIRTY = 30
VALUE_SIXTY = 60
VALUE_HUNDRED = 100
VALUE_THOUSAND = 1000
VALUE_FOUR_THOUSAND = 4000

# Time-based values (seconds)
SECONDS_ONE = 1
SECONDS_FIVE = 5
SECONDS_TEN = 10
SECONDS_THIRTY = 30
SECONDS_SIXTY = 60
SECONDS_TWO_MINUTES = 120
SECONDS_FIVE_MINUTES = 300
SECONDS_TEN_MINUTES = 600
SECONDS_THIRTY_MINUTES = 1800
SECONDS_ONE_HOUR = 3600
SECONDS_ONE_DAY = 86400

# =============================================================================
# BOOLEAN CONSTANTS
# =============================================================================

# Enable/disable flags
ENABLE_TRUE = True
ENABLE_FALSE = False

# Feature flags
FEATURE_ENABLED = True
FEATURE_DISABLED = False

# =============================================================================
# REQUIRED CONFIGURATION KEYS
# =============================================================================

# System configuration keys
REQUIRED_SYSTEM_KEYS = [
    "version",
    "environment", 
    "debug_mode",
    "logging_level"
]

# Communication configuration keys
REQUIRED_COMMUNICATION_KEYS = [
    "timeout",
    "retry_attempts",
    "retry_delay",
    "max_connections"
]

# Agent configuration keys
REQUIRED_AGENT_KEYS = [
    "agent_id",
    "status",
    "capabilities",
    "communication_config"
]

# =============================================================================
# ENVIRONMENT OVERRIDES
# =============================================================================

# Environment names
ENV_DEVELOPMENT = "development"
ENV_TESTING = "testing"
ENV_STAGING = "staging"
ENV_PRODUCTION = "production"

# Environment-specific overrides
ENVIRONMENT_OVERRIDES = {
    ENV_DEVELOPMENT: {
        "debug_mode": True,
        "logging_level": "DEBUG",
        "hot_reload": True
    },
    ENV_TESTING: {
        "debug_mode": False,
        "logging_level": "INFO",
        "mock_services": True
    },
    ENV_STAGING: {
        "debug_mode": False,
        "logging_level": "INFO",
        "performance_monitoring": True
    },
    ENV_PRODUCTION: {
        "debug_mode": False,
        "logging_level": "WARNING",
        "security_enabled": True
    }
}

# =============================================================================
# VALIDATION CONSTANTS
# =============================================================================

# Validation thresholds
VALIDATION_TIMEOUT = 300.0
VALIDATION_RETRY_ATTEMPTS = 3
VALIDATION_RETRY_DELAY = 1.0

# Quality thresholds
QUALITY_THRESHOLD = 0.8
COVERAGE_THRESHOLD = 0.9
PERFORMANCE_THRESHOLD = 0.7

# =============================================================================
# INTEGRATION CONSTANTS
# =============================================================================

# API limits
API_MAX_TOKENS = 4000
API_TEMPERATURE = 0.7
API_RATE_LIMIT = 100

# Service registry
SERVICE_TIMEOUT = 10.0
SERVICE_HEALTH_CHECK_INTERVAL = 30
SERVICE_DISCOVERY_TIMEOUT = 60

# =============================================================================
# MONITORING CONSTANTS
# =============================================================================

# Health check intervals
HEALTH_CHECK_INTERVAL = 30
HEALTH_CHECK_TIMEOUT = 10
HEALTH_CHECK_RETRY_ATTEMPTS = 3

# Metrics collection
METRICS_COLLECTION_INTERVAL = 60
METRICS_RETENTION_DAYS = 90
METRICS_BATCH_SIZE = 1000

# =============================================================================
# LOGGING CONSTANTS
# =============================================================================

# Log levels
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_CRITICAL = "CRITICAL"

# Log formats
LOG_FORMAT_STANDARD = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FORMAT_DETAILED = "%(asctime)s | %(name)s | %(levelname)8s | %(message)s"

# Log rotation
LOG_MAX_BYTES = 10485760  # 10MB
LOG_BACKUP_COUNT = 5
LOG_RETENTION_DAYS = 30

# =============================================================================
# SECURITY CONSTANTS
# =============================================================================

# Authentication
AUTH_TOKEN_EXPIRY = 3600  # 1 hour
AUTH_REFRESH_TOKEN_EXPIRY = 86400  # 24 hours
AUTH_MAX_LOGIN_ATTEMPTS = 5

# Encryption
ENCRYPTION_KEY_ROTATION_INTERVAL = 86400  # 24 hours
ENCRYPTION_ALGORITHM = "AES-256"
ENCRYPTION_KEY_SIZE = 32

# Rate limiting
RATE_LIMIT_REQUESTS_PER_MINUTE = 100
RATE_LIMIT_BURST_SIZE = 10
RATE_LIMIT_WINDOW_SIZE = 60

# =============================================================================
# DEPLOYMENT CONSTANTS
# =============================================================================

# Container settings
CONTAINER_IMAGE_BASE = "python:3.9-slim"
CONTAINER_WORKING_DIR = "/workspace"
CONTAINER_VOLUME_DRIVER = "local"

# CI/CD artifacts
ARTIFACT_EXPIRATION = "$ARTIFACT_EXPIRATION"
ARTIFACT_COVERAGE_FORMAT = "cobertura"
ARTIFACT_COVERAGE_PATH = "coverage.xml"

# =============================================================================
# EXPORT ALL CONSTANTS
# =============================================================================

__all__ = [
    # Timeouts
    "DEFAULT_TIMEOUT", "SHORT_TIMEOUT", "LONG_TIMEOUT", "CRITICAL_TIMEOUT",
    "EXTENDED_TIMEOUT", "URGENT_TIMEOUT", "COMMUNICATION_TIMEOUT", "KEEPALIVE_TIMEOUT",
    "PING_TIMEOUT", "CONNECTION_TIMEOUT", "IDLE_TIMEOUT", "SHUTDOWN_TIMEOUT",
    "API_TIMEOUT", "SERVICE_TIMEOUT", "RECOVERY_TIMEOUT", "VALIDATION_TIMEOUT", "TEST_TIMEOUT",
    
    # Retry settings
    "DEFAULT_RETRY_ATTEMPTS", "DEFAULT_RETRY_DELAY", "MAX_RETRY_ATTEMPTS",
    "MIN_RETRY_DELAY", "MAX_RETRY_DELAY", "MESSAGE_RETRY_ATTEMPTS", "MESSAGE_RETRY_DELAY",
    "FSM_RETRY_ATTEMPTS", "FSM_RETRY_DELAY", "INTEGRATION_RETRY_ATTEMPTS", "INTEGRATION_RETRY_DELAY",
    
    # Collection intervals
    "DEFAULT_COLLECTION_INTERVAL", "LONG_COLLECTION_INTERVAL", "SHORT_COLLECTION_INTERVAL",
    "URGENT_COLLECTION_INTERVAL", "EXTENDED_COLLECTION_INTERVAL", "SYSTEM_METRICS_INTERVAL",
    "APPLICATION_METRICS_INTERVAL", "NETWORK_METRICS_INTERVAL", "CUSTOM_METRICS_INTERVAL",
    "COMMUNICATION_METRICS_INTERVAL",
    
    # Enable/disable flags
    "SYSTEM_ENABLED", "SYSTEM_DISABLED", "MONITORING_ENABLED", "PERFORMANCE_MONITORING_ENABLED",
    "ALERTING_ENABLED", "DASHBOARD_ENABLED", "COMMUNICATION_ENABLED", "BROADCAST_ENABLED",
    "PRIVATE_MESSAGING_ENABLED", "COMPRESSION_ENABLED", "AUTHORIZATION_ENABLED", "ENCRYPTION_ENABLED",
    "AUTHENTICATION_ENABLED", "RATE_LIMITING_ENABLED", "DEBUG_MODE_ENABLED", "HOT_RELOAD_ENABLED",
    "TESTING_ENABLED", "MOCK_SERVICES_ENABLED",
    
    # Performance thresholds
    "MEMORY_WARNING_THRESHOLD", "MEMORY_CRITICAL_THRESHOLD", "NETWORK_WARNING_THRESHOLD",
    "NETWORK_CRITICAL_THRESHOLD", "CPU_WARNING_THRESHOLD", "CPU_CRITICAL_THRESHOLD",
    "DISK_WARNING_THRESHOLD", "DISK_CRITICAL_THRESHOLD",
    
    # Queue and batch settings
    "DEFAULT_QUEUE_SIZE", "MAX_QUEUE_SIZE", "MIN_QUEUE_SIZE", "MAX_BATCH_SIZE",
    "DEFAULT_BATCH_SIZE", "MIN_BATCH_SIZE",
    
    # Priority levels
    "PRIORITY_LOW", "PRIORITY_NORMAL", "PRIORITY_HIGH", "PRIORITY_CRITICAL", "PRIORITY_EMERGENCY",
    "PRIORITY_NAMES",
    
    # Data types and schemas
    "SCHEMA_TYPE_STRING", "SCHEMA_TYPE_OBJECT", "SCHEMA_TYPE_ARRAY", "SCHEMA_TYPE_BOOLEAN",
    "SCHEMA_TYPE_NUMBER", "SCHEMA_TYPE_INTEGER", "STRING_PRIMARY", "STRING_SECONDARY",
    "STRING_PASS", "STRING_FAIL", "STRING_TEST", "STRING_GATED",
    
    # Numeric constants
    "VALUE_ZERO", "VALUE_ONE", "VALUE_TWO", "VALUE_THREE", "VALUE_FIVE", "VALUE_TEN",
    "VALUE_THIRTY", "VALUE_SIXTY", "VALUE_HUNDRED", "VALUE_THOUSAND", "VALUE_FOUR_THOUSAND",
    "SECONDS_ONE", "SECONDS_FIVE", "SECONDS_TEN", "SECONDS_THIRTY", "SECONDS_SIXTY",
    "SECONDS_TWO_MINUTES", "SECONDS_FIVE_MINUTES", "SECONDS_TEN_MINUTES", "SECONDS_THIRTY_MINUTES",
    "SECONDS_ONE_HOUR", "SECONDS_ONE_DAY",
    
    # Boolean constants
    "ENABLE_TRUE", "ENABLE_FALSE", "FEATURE_ENABLED", "FEATURE_DISABLED",
    
    # Required keys
    "REQUIRED_SYSTEM_KEYS", "REQUIRED_COMMUNICATION_KEYS", "REQUIRED_AGENT_KEYS",
    
    # Environment overrides
    "ENV_DEVELOPMENT", "ENV_TESTING", "ENV_STAGING", "ENV_PRODUCTION", "ENVIRONMENT_OVERRIDES",
    
    # Validation constants
    "VALIDATION_TIMEOUT", "VALIDATION_RETRY_ATTEMPTS", "VALIDATION_RETRY_DELAY",
    "QUALITY_THRESHOLD", "COVERAGE_THRESHOLD", "PERFORMANCE_THRESHOLD",
    
    # Integration constants
    "API_MAX_TOKENS", "API_TEMPERATURE", "API_RATE_LIMIT", "SERVICE_TIMEOUT",
    "SERVICE_HEALTH_CHECK_INTERVAL", "SERVICE_DISCOVERY_TIMEOUT",
    
    # Monitoring constants
    "HEALTH_CHECK_INTERVAL", "HEALTH_CHECK_TIMEOUT", "HEALTH_CHECK_RETRY_ATTEMPTS",
    "METRICS_COLLECTION_INTERVAL", "METRICS_RETENTION_DAYS", "METRICS_BATCH_SIZE",
    
    # Logging constants
    "LOG_LEVEL_DEBUG", "LOG_LEVEL_INFO", "LOG_LEVEL_WARNING", "LOG_LEVEL_ERROR", "LOG_LEVEL_CRITICAL",
    "LOG_FORMAT_STANDARD", "LOG_FORMAT_DETAILED", "LOG_MAX_BYTES", "LOG_BACKUP_COUNT", "LOG_RETENTION_DAYS",
    
    # Security constants
    "AUTH_TOKEN_EXPIRY", "AUTH_REFRESH_TOKEN_EXPIRY", "AUTH_MAX_LOGIN_ATTEMPTS",
    "ENCRYPTION_KEY_ROTATION_INTERVAL", "ENCRYPTION_ALGORITHM", "ENCRYPTION_KEY_SIZE",
    "RATE_LIMIT_REQUESTS_PER_MINUTE", "RATE_LIMIT_BURST_SIZE", "RATE_LIMIT_WINDOW_SIZE",
    
    # Deployment constants
    "CONTAINER_IMAGE_BASE", "CONTAINER_WORKING_DIR", "CONTAINER_VOLUME_DRIVER",
    "ARTIFACT_EXPIRATION", "ARTIFACT_COVERAGE_FORMAT", "ARTIFACT_COVERAGE_PATH"
]
