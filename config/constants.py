"""
Unified Configuration Constants - Single Source of Truth (SSOT)

This module centralizes all configuration constants to eliminate duplication
and ensure consistency across the entire system.

Author: Agent-6
Contract: SSOT-003: Configuration Management Consolidation
Date: 2025-08-28
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
AUTO_DISCOVERY_ENABLED = True
PLUGIN_SYSTEM_ENABLED = True

# =============================================================================
# PRIORITY LEVELS
# =============================================================================

# Message priority levels
PRIORITY_LOW = 1
PRIORITY_NORMAL = 2
PRIORITY_HIGH = 3
PRIORITY_URGENT = 4
PRIORITY_CRITICAL = 5

# =============================================================================
# QUEUE CONFIGURATIONS
# =============================================================================

# Message queue settings
DEFAULT_QUEUE_SIZE = 1000
MAX_QUEUE_SIZE = 10000
DEFAULT_BATCH_SIZE = 100
MAX_BATCH_SIZE = 1000

# =============================================================================
# PERFORMANCE THRESHOLDS
# =============================================================================

# CPU and memory thresholds
CPU_WARNING_THRESHOLD = 70
CPU_CRITICAL_THRESHOLD = 90
MEMORY_WARNING_THRESHOLD = 80
MEMORY_CRITICAL_THRESHOLD = 95

# Network thresholds
NETWORK_WARNING_THRESHOLD = 80
NETWORK_CRITICAL_THRESHOLD = 95

# =============================================================================
# PORTS AND ENDPOINTS
# =============================================================================

# Standard service ports
DASHBOARD_PORT = 8080
API_GATEWAY_PORT = 8443
METRICS_PORT = 9090
HEALTH_CHECK_PORT = 8081

# =============================================================================
# FILE PATHS AND NAMES
# =============================================================================

# Response capture settings
FILE_WATCH_ROOT = "agent_workspaces"
FILE_RESPONSE_NAME = "response.txt"

# =============================================================================
# OCR SETTINGS
# =============================================================================

# Optical character recognition defaults
OCR_LANG = "eng"
OCR_PSM = 6

# =============================================================================
# CLIPBOARD SETTINGS
# =============================================================================

# Clipboard monitoring
CLIPBOARD_POLL_MS = 500

# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

# Required configuration keys for validation
REQUIRED_SYSTEM_KEYS = [
    "enabled",
    "version",
    "collection_interval"
]

REQUIRED_COMMUNICATION_KEYS = [
    "enabled",
    "timeout",
    "retry_attempts"
]

REQUIRED_AGENT_KEYS = [
    "enabled",
    "max_queue_size",
    "retry_attempts"
]

# =============================================================================
# CONFIGURATION MAPPINGS
# =============================================================================

# Map configuration types to their default values
DEFAULT_CONFIGURATIONS: Dict[str, Dict[str, Any]] = {
    "timeout": {
        "default": DEFAULT_TIMEOUT,
        "short": SHORT_TIMEOUT,
        "long": LONG_TIMEOUT,
        "critical": CRITICAL_TIMEOUT,
        "urgent": URGENT_TIMEOUT
    },
    "retry": {
        "attempts": DEFAULT_RETRY_ATTEMPTS,
        "delay": DEFAULT_RETRY_DELAY,
        "max_attempts": MAX_RETRY_ATTEMPTS
    },
    "collection_interval": {
        "default": DEFAULT_COLLECTION_INTERVAL,
        "short": SHORT_COLLECTION_INTERVAL,
        "long": LONG_COLLECTION_INTERVAL
    },
    "priority": {
        "low": PRIORITY_LOW,
        "normal": PRIORITY_NORMAL,
        "high": PRIORITY_HIGH,
        "urgent": PRIORITY_URGENT,
        "critical": PRIORITY_CRITICAL
    }
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_timeout_config(timeout_type: str = "default") -> float:
    """Get timeout configuration value by type."""
    return DEFAULT_CONFIGURATIONS["timeout"].get(timeout_type, DEFAULT_TIMEOUT)

def get_retry_config(retry_type: str = "attempts") -> Any:
    """Get retry configuration value by type."""
    return DEFAULT_CONFIGURATIONS["retry"].get(retry_type, DEFAULT_RETRY_ATTEMPTS)

def get_collection_interval(interval_type: str = "default") -> int:
    """Get collection interval configuration value by type."""
    return DEFAULT_CONFIGURATIONS["collection_interval"].get(interval_type, DEFAULT_COLLECTION_INTERVAL)

def get_priority_level(priority_name: str) -> int:
    """Get priority level by name."""
    return DEFAULT_CONFIGURATIONS["priority"].get(priority_name.lower(), PRIORITY_NORMAL)

def validate_config_consistency(config: Dict[str, Any], required_keys: List[str]) -> bool:
    """Validate that configuration contains required keys."""
    return all(key in config for key in required_keys)

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Timeouts
    "DEFAULT_TIMEOUT", "SHORT_TIMEOUT", "LONG_TIMEOUT", "CRITICAL_TIMEOUT",
    "EXTENDED_TIMEOUT", "URGENT_TIMEOUT", "COMMUNICATION_TIMEOUT",
    "KEEPALIVE_TIMEOUT", "PING_TIMEOUT", "CONNECTION_TIMEOUT",
    "IDLE_TIMEOUT", "SHUTDOWN_TIMEOUT", "API_TIMEOUT", "SERVICE_TIMEOUT",
    "RECOVERY_TIMEOUT", "VALIDATION_TIMEOUT", "TEST_TIMEOUT",
    
    # Retry settings
    "DEFAULT_RETRY_ATTEMPTS", "DEFAULT_RETRY_DELAY", "MAX_RETRY_ATTEMPTS",
    "MIN_RETRY_DELAY", "MAX_RETRY_DELAY", "MESSAGE_RETRY_ATTEMPTS",
    "MESSAGE_RETRY_DELAY", "FSM_RETRY_ATTEMPTS", "FSM_RETRY_DELAY",
    "INTEGRATION_RETRY_ATTEMPTS", "INTEGRATION_RETRY_DELAY",
    
    # Collection intervals
    "DEFAULT_COLLECTION_INTERVAL", "LONG_COLLECTION_INTERVAL",
    "SHORT_COLLECTION_INTERVAL", "URGENT_COLLECTION_INTERVAL",
    "EXTENDED_COLLECTION_INTERVAL", "SYSTEM_METRICS_INTERVAL",
    "APPLICATION_METRICS_INTERVAL", "NETWORK_METRICS_INTERVAL",
    "CUSTOM_METRICS_INTERVAL", "COMMUNICATION_METRICS_INTERVAL",
    
    # Enable/disable flags
    "SYSTEM_ENABLED", "SYSTEM_DISABLED", "MONITORING_ENABLED",
    "PERFORMANCE_MONITORING_ENABLED", "ALERTING_ENABLED",
    "DASHBOARD_ENABLED", "COMMUNICATION_ENABLED", "BROADCAST_ENABLED",
    "PRIVATE_MESSAGING_ENABLED", "COMPRESSION_ENABLED",
    "AUTHORIZATION_ENABLED", "ENCRYPTION_ENABLED", "AUTO_DISCOVERY_ENABLED",
    "PLUGIN_SYSTEM_ENABLED",
    
    # Priority levels
    "PRIORITY_LOW", "PRIORITY_NORMAL", "PRIORITY_HIGH",
    "PRIORITY_URGENT", "PRIORITY_CRITICAL",
    
    # Queue configurations
    "DEFAULT_QUEUE_SIZE", "MAX_QUEUE_SIZE", "DEFAULT_BATCH_SIZE",
    "MAX_BATCH_SIZE",
    
    # Performance thresholds
    "CPU_WARNING_THRESHOLD", "CPU_CRITICAL_THRESHOLD",
    "MEMORY_WARNING_THRESHOLD", "MEMORY_CRITICAL_THRESHOLD",
    "NETWORK_WARNING_THRESHOLD", "NETWORK_CRITICAL_THRESHOLD",
    
    # Ports and endpoints
    "DASHBOARD_PORT", "API_GATEWAY_PORT", "METRICS_PORT",
    "HEALTH_CHECK_PORT",
    
    # File paths and names
    "FILE_WATCH_ROOT", "FILE_RESPONSE_NAME",
    
    # OCR settings
    "OCR_LANG", "OCR_PSM",
    
    # Clipboard settings
    "CLIPBOARD_POLL_MS",
    
    # Configuration validation
    "REQUIRED_SYSTEM_KEYS", "REQUIRED_COMMUNICATION_KEYS",
    "REQUIRED_AGENT_KEYS", "DEFAULT_CONFIGURATIONS",
    
    # Utility functions
    "get_timeout_config", "get_retry_config", "get_collection_interval",
    "get_priority_level", "validate_config_consistency"
]
