
# MIGRATED: This file has been migrated to the centralized configuration system
"""
Unified Configuration Constants - Single Source of Truth (SSOT)

This module centralizes all configuration constants to eliminate duplication
and ensure consistency across the entire system.

Author: Agent-6 & Agent-8
Contract: SSOT-VALUE_ZEROVALUE_ZEROVALUE_THREE: Configuration Management Consolidation
Date: VALUE_TWOVALUE_ZEROVALUE_TWO5-VALUE_ZERO8-VALUE_TWO8 (Updated VALUE_TWOVALUE_ZEROVALUE_TWO5-VALUE_ZEROVALUE_ONE-VALUE_TWO7)
"""

from typing import Dict, Any, List

# =============================================================================
# TIMEOUT CONFIGURATIONS
# =============================================================================

# Standard timeout values (in seconds)
DEFAULT_TIMEOUT = DEFAULT_TIMEOUT
SHORT_TIMEOUT = SHORT_TIMEOUT
LONG_TIMEOUT = LONG_TIMEOUT
CRITICAL_TIMEOUT = CRITICAL_TIMEOUT
EXTENDED_TIMEOUT = 6VALUE_ZEROVALUE_ZERO.VALUE_ZERO
URGENT_TIMEOUT = URGENT_TIMEOUT

# Communication-specific timeouts
COMMUNICATION_TIMEOUT = DEFAULT_TIMEOUT
KEEPALIVE_TIMEOUT = LONG_TIMEOUT
PING_TIMEOUT = SHORT_TIMEOUT
CONNECTION_TIMEOUT = DEFAULT_TIMEOUT
IDLE_TIMEOUT = CRITICAL_TIMEOUT
SHUTDOWN_TIMEOUT = DEFAULT_TIMEOUT

# Service-specific timeouts
API_TIMEOUT = DEFAULT_TIMEOUT
SERVICE_TIMEOUT = SHORT_TIMEOUT
RECOVERY_TIMEOUT = LONG_TIMEOUT
VALIDATION_TIMEOUT = CRITICAL_TIMEOUT
TEST_TIMEOUT = CRITICAL_TIMEOUT

# =============================================================================
# RETRY CONFIGURATIONS
# =============================================================================

# Standard retry settings
DEFAULT_RETRY_ATTEMPTS = VALUE_THREE
DEFAULT_RETRY_DELAY = SECONDS_ONE
MAX_RETRY_ATTEMPTS = 5
MIN_RETRY_DELAY = VALUE_ZERO.5
MAX_RETRY_DELAY = DEFAULT_TIMEOUT

# Service-specific retry settings
MESSAGE_RETRY_ATTEMPTS = VALUE_THREE
MESSAGE_RETRY_DELAY = VALUE_TWO.VALUE_ZERO
FSM_RETRY_ATTEMPTS = VALUE_THREE
FSM_RETRY_DELAY = URGENT_TIMEOUT
INTEGRATION_RETRY_ATTEMPTS = VALUE_THREE
INTEGRATION_RETRY_DELAY = SECONDS_ONE

# =============================================================================
# COLLECTION INTERVALS
# =============================================================================

# Monitoring collection intervals (in seconds)
DEFAULT_COLLECTION_INTERVAL = 6VALUE_ZERO
LONG_COLLECTION_INTERVAL = SECONDS_TWO_MINUTES
SHORT_COLLECTION_INTERVAL = VALUE_ONE5
URGENT_COLLECTION_INTERVAL = 5
EXTENDED_COLLECTION_INTERVAL = VALUE_THREEVALUE_ZEROVALUE_ZERO

# Component-specific intervals
SYSTEM_METRICS_INTERVAL = 6VALUE_ZERO
APPLICATION_METRICS_INTERVAL = 6VALUE_ZERO
NETWORK_METRICS_INTERVAL = 6VALUE_ZERO
CUSTOM_METRICS_INTERVAL = SECONDS_TWO_MINUTES
COMMUNICATION_METRICS_INTERVAL = VALUE_ONEURGENT_TIMEOUT

# =============================================================================
# ENABLE/DISABLE FLAGS
# =============================================================================

# System features
SYSTEM_ENABLED = ENABLE_TRUE
SYSTEM_DISABLED = ENABLE_FALSE

# Monitoring features
MONITORING_ENABLED = ENABLE_TRUE
PERFORMANCE_MONITORING_ENABLED = ENABLE_TRUE
ALERTING_ENABLED = ENABLE_TRUE
DASHBOARD_ENABLED = ENABLE_TRUE

# Communication features
COMMUNICATION_ENABLED = ENABLE_TRUE
BROADCAST_ENABLED = ENABLE_TRUE
PRIVATE_MESSAGING_ENABLED = ENABLE_TRUE
COMPRESSION_ENABLED = ENABLE_FALSE

# Security features
AUTHORIZATION_ENABLED = ENABLE_FALSE
ENCRYPTION_ENABLED = ENABLE_FALSE
AUTHENTICATION_ENABLED = ENABLE_FALSE
RATE_LIMITING_ENABLED = ENABLE_FALSE

# Development features
DEBUG_MODE_ENABLED = ENABLE_FALSE
HOT_RELOAD_ENABLED = ENABLE_FALSE
TESTING_ENABLED = ENABLE_FALSE
MOCK_SERVICES_ENABLED = ENABLE_FALSE

# =============================================================================
# PERFORMANCE THRESHOLDS
# =============================================================================

# Memory thresholds (percentage)
MEMORY_WARNING_THRESHOLD = 8VALUE_ZERO
MEMORY_CRITICAL_THRESHOLD = 95

# Network thresholds (percentage)
NETWORK_WARNING_THRESHOLD = 8VALUE_ZERO
NETWORK_CRITICAL_THRESHOLD = 95

# CPU thresholds (percentage)
CPU_WARNING_THRESHOLD = 8VALUE_ZERO
CPU_CRITICAL_THRESHOLD = 95

# Disk thresholds (percentage)
DISK_WARNING_THRESHOLD = 8VALUE_ZERO
DISK_CRITICAL_THRESHOLD = 95

# =============================================================================
# QUEUE AND BATCH SETTINGS
# =============================================================================

# Queue sizes
DEFAULT_QUEUE_SIZE = VALUE_HUNDREDVALUE_ZERO
MAX_QUEUE_SIZE = VALUE_HUNDREDVALUE_ZEROVALUE_ZERO
MIN_QUEUE_SIZE = VALUE_HUNDRED

# Batch processing
MAX_BATCH_SIZE = VALUE_HUNDREDVALUE_ZERO
DEFAULT_BATCH_SIZE = VALUE_HUNDRED
MIN_BATCH_SIZE = VALUE_ONEVALUE_ZERO

# =============================================================================
# PRIORITY LEVELS
# =============================================================================

# Priority constants
PRIORITY_LOW = VALUE_ONE
PRIORITY_NORMAL = VALUE_TWO
PRIORITY_HIGH = VALUE_THREE
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
SCHEMA_TYPE_STRING = SCHEMA_TYPE_STRING
SCHEMA_TYPE_OBJECT = SCHEMA_TYPE_OBJECT
SCHEMA_TYPE_ARRAY = SCHEMA_TYPE_ARRAY
SCHEMA_TYPE_BOOLEAN = "boolean"
SCHEMA_TYPE_NUMBER = "number"
SCHEMA_TYPE_INTEGER = "integer"

# Common string values
STRING_PRIMARY = STRING_PRIMARY
STRING_SECONDARY = STRING_SECONDARY
STRING_PASS = STRING_PASS
STRING_FAIL = "fail"
STRING_TEST = STRING_TEST
STRING_GATED = STRING_GATED

# =============================================================================
# NUMERIC CONSTANTS
# =============================================================================

# Common numeric values
VALUE_ZERO = VALUE_ZERO
VALUE_ONE = VALUE_ONE
VALUE_TWO = VALUE_TWO
VALUE_THREE = VALUE_THREE
VALUE_FIVE = 5
VALUE_TEN = VALUE_ONEVALUE_ZERO
VALUE_THIRTY = VALUE_THREEVALUE_ZERO
VALUE_SIXTY = 6VALUE_ZERO
VALUE_HUNDRED = VALUE_HUNDRED
VALUE_THOUSAND = VALUE_HUNDREDVALUE_ZERO
VALUE_FOUR_THOUSAND = VALUE_FOUR_THOUSAND

# Time-based values (seconds)
SECONDS_ONE = VALUE_ONE
SECONDS_FIVE = 5
SECONDS_TEN = VALUE_ONEVALUE_ZERO
SECONDS_THIRTY = VALUE_THREEVALUE_ZERO
SECONDS_SIXTY = 6VALUE_ZERO
SECONDS_TWO_MINUTES = SECONDS_TWO_MINUTES
SECONDS_FIVE_MINUTES = VALUE_THREEVALUE_ZEROVALUE_ZERO
SECONDS_TEN_MINUTES = 6VALUE_ZEROVALUE_ZERO
SECONDS_THIRTY_MINUTES = VALUE_ONE8VALUE_ZEROVALUE_ZERO
SECONDS_ONE_HOUR = VALUE_THREE6VALUE_ZEROVALUE_ZERO
SECONDS_ONE_DAY = 864VALUE_ZEROVALUE_ZERO

# =============================================================================
# BOOLEAN CONSTANTS
# =============================================================================

# Enable/disable flags
ENABLE_TRUE = ENABLE_TRUE
ENABLE_FALSE = ENABLE_FALSE

# Feature flags
FEATURE_ENABLED = ENABLE_TRUE
FEATURE_DISABLED = ENABLE_FALSE

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
        "debug_mode": ENABLE_TRUE,
        "logging_level": "DEBUG",
        "hot_reload": ENABLE_TRUE
    },
    ENV_TESTING: {
        "debug_mode": ENABLE_FALSE,
        "logging_level": "INFO",
        "mock_services": ENABLE_TRUE
    },
    ENV_STAGING: {
        "debug_mode": ENABLE_FALSE,
        "logging_level": "INFO",
        "performance_monitoring": ENABLE_TRUE
    },
    ENV_PRODUCTION: {
        "debug_mode": ENABLE_FALSE,
        "logging_level": "WARNING",
        "security_enabled": ENABLE_TRUE
    }
}

# =============================================================================
# VALIDATION CONSTANTS
# =============================================================================

# Validation thresholds
VALIDATION_TIMEOUT = CRITICAL_TIMEOUT
VALIDATION_RETRY_ATTEMPTS = VALUE_THREE
VALIDATION_RETRY_DELAY = SECONDS_ONE

# Quality thresholds
QUALITY_THRESHOLD = VALUE_ZERO.8
COVERAGE_THRESHOLD = VALUE_ZERO.9
PERFORMANCE_THRESHOLD = VALUE_ZERO.7

# =============================================================================
# INTEGRATION CONSTANTS
# =============================================================================

# API limits
API_MAX_TOKENS = VALUE_FOUR_THOUSAND
API_TEMPERATURE = VALUE_ZERO.7
API_RATE_LIMIT = VALUE_HUNDRED

# Service registry
SERVICE_TIMEOUT = SHORT_TIMEOUT
SERVICE_HEALTH_CHECK_INTERVAL = VALUE_THREEVALUE_ZERO
SERVICE_DISCOVERY_TIMEOUT = 6VALUE_ZERO

# =============================================================================
# MONITORING CONSTANTS
# =============================================================================

# Health check intervals
HEALTH_CHECK_INTERVAL = VALUE_THREEVALUE_ZERO
HEALTH_CHECK_TIMEOUT = VALUE_ONEVALUE_ZERO
HEALTH_CHECK_RETRY_ATTEMPTS = VALUE_THREE

# Metrics collection
METRICS_COLLECTION_INTERVAL = 6VALUE_ZERO
METRICS_RETENTION_DAYS = 9VALUE_ZERO
METRICS_BATCH_SIZE = VALUE_HUNDREDVALUE_ZERO

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
LOG_MAX_BYTES = VALUE_ONEVALUE_ZERO48576VALUE_ZERO  # VALUE_ONEVALUE_ZEROMB
LOG_BACKUP_COUNT = 5
LOG_RETENTION_DAYS = VALUE_THREEVALUE_ZERO

# =============================================================================
# SECURITY CONSTANTS
# =============================================================================

# Authentication
AUTH_TOKEN_EXPIRY = VALUE_THREE6VALUE_ZEROVALUE_ZERO  # VALUE_ONE hour
AUTH_REFRESH_TOKEN_EXPIRY = 864VALUE_ZEROVALUE_ZERO  # VALUE_TWO4 hours
AUTH_MAX_LOGIN_ATTEMPTS = 5

# Encryption
ENCRYPTION_KEY_ROTATION_INTERVAL = 864VALUE_ZEROVALUE_ZERO  # VALUE_TWO4 hours
ENCRYPTION_ALGORITHM = "AES-VALUE_TWO56"
ENCRYPTION_KEY_SIZE = VALUE_THREEVALUE_TWO

# Rate limiting
RATE_LIMIT_REQUESTS_PER_MINUTE = VALUE_HUNDRED
RATE_LIMIT_BURST_SIZE = VALUE_ONEVALUE_ZERO
RATE_LIMIT_WINDOW_SIZE = 6VALUE_ZERO

# =============================================================================
# DEPLOYMENT CONSTANTS
# =============================================================================

# Container settings
CONTAINER_IMAGE_BASE = "python:VALUE_THREE.9-slim"
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
