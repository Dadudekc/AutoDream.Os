
#!/usr/bin/env python3
"""
Manager Constants - V2 Compliance Manager Module Definitions
===========================================================

This module provides manager-related constants with V2 compliance standards.

V2 COMPLIANCE: Type-safe manager constants with validation and configuration
DESIGN PATTERN: Configuration-driven manager parameters with validation
DEPENDENCY INJECTION: Uses unified configuration and path systems

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Manager Constants Optimized
"""

from typing import Final
from ..unified_configuration_system import get_unified_config, get_config
from ..constants.paths import get_project_root

# ================================
# MANAGER HEALTH MONITORING CONSTANTS
# ================================

# Health check intervals and timing
DEFAULT_HEALTH_CHECK_INTERVAL: Final[int] = get_config("DEFAULT_HEALTH_CHECK_INTERVAL", 30)
"""Default interval in seconds between health check operations."""

HEALTH_CHECK_TIMEOUT_SECONDS: Final[int] = get_config("HEALTH_CHECK_TIMEOUT_SECONDS", 10)
"""Timeout in seconds for individual health check operations."""

HEALTH_CHECK_RETRY_COUNT: Final[int] = get_config("HEALTH_CHECK_RETRY_COUNT", 3)
"""Number of retry attempts for failed health checks."""

HEALTH_CHECK_RETRY_DELAY: Final[float] = get_config("HEALTH_CHECK_RETRY_DELAY", 2.0)
"""Delay in seconds between health check retry attempts."""

# ================================
# MANAGER STATUS CONSTANTS
# ================================

# Status history and storage
DEFAULT_MAX_STATUS_HISTORY: Final[int] = get_config("DEFAULT_MAX_STATUS_HISTORY", 1000)
"""Maximum number of status records to retain in history."""

STATUS_CLEANUP_INTERVAL_MINUTES: Final[int] = get_config("STATUS_CLEANUP_INTERVAL_MINUTES", 60)
"""Interval in minutes between status history cleanup operations."""

STATUS_COMPRESSION_THRESHOLD: Final[int] = get_config("STATUS_COMPRESSION_THRESHOLD", 5000)
"""Number of status records that triggers compression."""

# ================================
# MANAGER RESOLUTION CONSTANTS
# ================================

# Auto-resolution settings
DEFAULT_AUTO_RESOLVE_TIMEOUT: Final[int] = get_config("DEFAULT_AUTO_RESOLVE_TIMEOUT", 3600)
"""Default timeout in seconds for automatic issue resolution."""

AUTO_RESOLVE_MAX_ATTEMPTS: Final[int] = get_config("AUTO_RESOLVE_MAX_ATTEMPTS", 5)
"""Maximum number of auto-resolution attempts per issue."""

AUTO_RESOLVE_RETRY_DELAY: Final[float] = get_config("AUTO_RESOLVE_RETRY_DELAY", 30.0)
"""Delay in seconds between auto-resolution retry attempts."""

# ================================
# MANAGER RESOURCE CONSTANTS
# ================================

# Resource monitoring thresholds
RESOURCE_WARNING_THRESHOLD: Final[float] = get_config("RESOURCE_WARNING_THRESHOLD", 0.8)
"""Resource utilization threshold that triggers warnings (0.0 to 1.0)."""

RESOURCE_CRITICAL_THRESHOLD: Final[float] = get_config("RESOURCE_CRITICAL_THRESHOLD", 0.95)
"""Resource utilization threshold that triggers critical alerts (0.0 to 1.0)."""

RESOURCE_MONITORING_INTERVAL: Final[int] = get_config("RESOURCE_MONITORING_INTERVAL", 60)
"""Interval in seconds between resource monitoring checks."""

# ================================
# MANAGER CONFIGURATION PATHS
# ================================

# Configuration file paths - using unified path system
STATUS_CONFIG_PATH: Final[str] = str(get_project_root() / "config" / "status_manager.json")
"""Path to status manager configuration file."""

HEALTH_CONFIG_PATH: Final[str] = str(get_project_root() / "config" / "health_manager.json")
"""Path to health manager configuration file."""

RESOURCE_CONFIG_PATH: Final[str] = str(get_project_root() / "config" / "resource_manager.json")
"""Path to resource manager configuration file."""

# ================================
# MANAGER VALIDATION CONSTANTS
# ================================

# Validation ranges
MIN_HEALTH_CHECK_INTERVAL: Final[int] = 5
"""Minimum allowed health check interval in seconds."""

MAX_HEALTH_CHECK_INTERVAL: Final[int] = 3600  # 1 hour
"""Maximum allowed health check interval in seconds."""

MIN_STATUS_HISTORY: Final[int] = 10
"""Minimum allowed status history size."""

MAX_STATUS_HISTORY: Final[int] = 10000
"""Maximum allowed status history size."""

MIN_AUTO_RESOLVE_TIMEOUT: Final[int] = 60  # 1 minute
"""Minimum allowed auto-resolution timeout in seconds."""

MAX_AUTO_RESOLVE_TIMEOUT: Final[int] = 86400  # 24 hours
"""Maximum allowed auto-resolution timeout in seconds."""

# ================================
# UTILITY FUNCTIONS
# ================================

def validate_manager_constants() -> bool:
    """Validate manager configuration constants."""
    config = get_unified_config()

    # Validate health check interval
    if not (MIN_HEALTH_CHECK_INTERVAL <= DEFAULT_HEALTH_CHECK_INTERVAL <= MAX_HEALTH_CHECK_INTERVAL):
        config.get_logger(__name__).error(
            f"Invalid health check interval: {DEFAULT_HEALTH_CHECK_INTERVAL} "
            f"(must be between {MIN_HEALTH_CHECK_INTERVAL} and {MAX_HEALTH_CHECK_INTERVAL})"
        )
        return False

    # Validate status history
    if not (MIN_STATUS_HISTORY <= DEFAULT_MAX_STATUS_HISTORY <= MAX_STATUS_HISTORY):
        config.get_logger(__name__).error(
            f"Invalid max status history: {DEFAULT_MAX_STATUS_HISTORY} "
            f"(must be between {MIN_STATUS_HISTORY} and {MAX_STATUS_HISTORY})"
        )
        return False

    # Validate auto-resolve timeout
    if not (MIN_AUTO_RESOLVE_TIMEOUT <= DEFAULT_AUTO_RESOLVE_TIMEOUT <= MAX_AUTO_RESOLVE_TIMEOUT):
        config.get_logger(__name__).error(
            f"Invalid auto-resolve timeout: {DEFAULT_AUTO_RESOLVE_TIMEOUT} "
            f"(must be between {MIN_AUTO_RESOLVE_TIMEOUT} and {MAX_AUTO_RESOLVE_TIMEOUT})"
        )
        return False

    # Validate resource thresholds
    if not (0.0 <= RESOURCE_WARNING_THRESHOLD <= 1.0):
        config.get_logger(__name__).error(
            f"Invalid resource warning threshold: {RESOURCE_WARNING_THRESHOLD} "
            "(must be between 0.0 and 1.0)"
        )
        return False

    if not (0.0 <= RESOURCE_CRITICAL_THRESHOLD <= 1.0):
        config.get_logger(__name__).error(
            f"Invalid resource critical threshold: {RESOURCE_CRITICAL_THRESHOLD} "
            "(must be between 0.0 and 1.0)"
        )
        return False

    if RESOURCE_WARNING_THRESHOLD >= RESOURCE_CRITICAL_THRESHOLD:
        config.get_logger(__name__).error(
            f"Resource warning threshold ({RESOURCE_WARNING_THRESHOLD}) must be less than "
            f"critical threshold ({RESOURCE_CRITICAL_THRESHOLD})"
        )
        return False

    return True

def get_manager_config_summary() -> dict:
    """Get a summary of manager configuration."""
    return {
        "health_check": {
            "interval_seconds": DEFAULT_HEALTH_CHECK_INTERVAL,
            "timeout_seconds": HEALTH_CHECK_TIMEOUT_SECONDS,
            "retry_count": HEALTH_CHECK_RETRY_COUNT,
            "retry_delay": HEALTH_CHECK_RETRY_DELAY
        },
        "status": {
            "max_history": DEFAULT_MAX_STATUS_HISTORY,
            "cleanup_interval_minutes": STATUS_CLEANUP_INTERVAL_MINUTES,
            "compression_threshold": STATUS_COMPRESSION_THRESHOLD
        },
        "auto_resolve": {
            "timeout_seconds": DEFAULT_AUTO_RESOLVE_TIMEOUT,
            "max_attempts": AUTO_RESOLVE_MAX_ATTEMPTS,
            "retry_delay": AUTO_RESOLVE_RETRY_DELAY
        },
        "resources": {
            "warning_threshold": RESOURCE_WARNING_THRESHOLD,
            "critical_threshold": RESOURCE_CRITICAL_THRESHOLD,
            "monitoring_interval": RESOURCE_MONITORING_INTERVAL
        },
        "config_paths": {
            "status": STATUS_CONFIG_PATH,
            "health": HEALTH_CONFIG_PATH,
            "resource": RESOURCE_CONFIG_PATH
        },
        "validation_ranges": {
            "health_check_interval": f"{MIN_HEALTH_CHECK_INTERVAL}-{MAX_HEALTH_CHECK_INTERVAL}",
            "status_history": f"{MIN_STATUS_HISTORY}-{MAX_STATUS_HISTORY}",
            "auto_resolve_timeout": f"{MIN_AUTO_RESOLVE_TIMEOUT}-{MAX_AUTO_RESOLVE_TIMEOUT}"
        }
    }

# ================================
# INITIALIZATION
# ================================

# Validate manager constants on import
if not validate_manager_constants():
    raise ValueError("Manager constants validation failed - check configuration values")
