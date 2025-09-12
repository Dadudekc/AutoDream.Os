#!/usr/bin/env python3
"""
Decision Constants - V2 Compliance Decision Module Definitions
================================================================

This module provides decision-related constants with V2 compliance standards.

V2 COMPLIANCE: Type-safe constants with validation and documentation
DESIGN PATTERN: Configuration-driven constants with fallback defaults
DEPENDENCY INJECTION: Uses unified configuration system

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Decision Constants Optimized
"""

from typing import Final

from ..unified_config import get_config, get_unified_config

# Configuration simplified - KISS compliance

# ================================
# DECISION MODULE CONSTANTS
# ================================

# Decision processing limits
DEFAULT_MAX_CONCURRENT_DECISIONS: Final[int] = get_config("DEFAULT_MAX_CONCURRENT_DECISIONS", 100)

DECISION_TIMEOUT_SECONDS: Final[int] = get_config("DECISION_TIMEOUT_SECONDS", 300)

# Decision quality thresholds
DEFAULT_CONFIDENCE_THRESHOLD: Final[float] = get_config("DEFAULT_CONFIDENCE_THRESHOLD", 0.7)

# Cleanup and maintenance
AUTO_CLEANUP_COMPLETED_DECISIONS: Final[bool] = get_config("AUTO_CLEANUP_COMPLETED_DECISIONS", True)
"""Enable automatic cleanup of completed decision records."""

CLEANUP_INTERVAL_MINUTES: Final[int] = get_config("CLEANUP_INTERVAL_MINUTES", 15)

EXAMPLE USAGE:
==============

# Import the core component
from src.core.constants.decision import Decision

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Decision(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

"""Interval in minutes between automatic cleanup operations."""

# History and storage
MAX_DECISION_HISTORY: Final[int] = get_config("MAX_DECISION_HISTORY", 1000)
"""Maximum number of decision records to retain in history."""

# ================================
# VALIDATION CONSTANTS
# ================================

# Decision validation ranges
MIN_CONFIDENCE_THRESHOLD: Final[float] = 0.0
"""Minimum allowed confidence threshold value."""

MAX_CONFIDENCE_THRESHOLD: Final[float] = 1.0
"""Maximum allowed confidence threshold value."""

MIN_CONCURRENT_DECISIONS: Final[int] = 1
"""Minimum allowed concurrent decisions."""

MAX_CONCURRENT_DECISIONS: Final[int] = 1000
"""Maximum allowed concurrent decisions."""

MIN_TIMEOUT_SECONDS: Final[int] = 10
"""Minimum allowed timeout in seconds."""

MAX_TIMEOUT_SECONDS: Final[int] = 3600
"""Maximum allowed timeout in seconds."""

MIN_CLEANUP_INTERVAL: Final[int] = 1
"""Minimum cleanup interval in minutes."""

MAX_CLEANUP_INTERVAL: Final[int] = 1440
"""Maximum cleanup interval in minutes (24 hours)."""

# ================================
# UTILITY FUNCTIONS
# ================================


def validate_decision_constants() -> bool:
    """Validate that all decision constants are within acceptable ranges."""
    config = get_unified_config()

    # Validate confidence threshold
    if not (MIN_CONFIDENCE_THRESHOLD <= DEFAULT_CONFIDENCE_THRESHOLD <= MAX_CONFIDENCE_THRESHOLD):
        config.get_logger(__name__).error(
            f"Invalid confidence threshold: {DEFAULT_CONFIDENCE_THRESHOLD} "
            f"(must be between {MIN_CONFIDENCE_THRESHOLD} and {MAX_CONFIDENCE_THRESHOLD})"
        )
        return False

    # Validate concurrent decisions
    if not (
        MIN_CONCURRENT_DECISIONS <= DEFAULT_MAX_CONCURRENT_DECISIONS <= MAX_CONCURRENT_DECISIONS
    ):
        config.get_logger(__name__).error(
            f"Invalid max concurrent decisions: {DEFAULT_MAX_CONCURRENT_DECISIONS} "
            f"(must be between {MIN_CONCURRENT_DECISIONS} and {MAX_CONCURRENT_DECISIONS})"
        )
        return False

    # Validate timeout
    if not (MIN_TIMEOUT_SECONDS <= DECISION_TIMEOUT_SECONDS <= MAX_TIMEOUT_SECONDS):
        config.get_logger(__name__).error(
            f"Invalid timeout: {DECISION_TIMEOUT_SECONDS} "
            f"(must be between {MIN_TIMEOUT_SECONDS} and {MAX_TIMEOUT_SECONDS})"
        )
        return False

    # Validate cleanup interval
    if not (MIN_CLEANUP_INTERVAL <= CLEANUP_INTERVAL_MINUTES <= MAX_CLEANUP_INTERVAL):
        config.get_logger(__name__).error(
            f"Invalid cleanup interval: {CLEANUP_INTERVAL_MINUTES} "
            f"(must be between {MIN_CLEANUP_INTERVAL} and {MAX_CLEANUP_INTERVAL})"
        )
        return False

    return True


def get_decision_config_summary() -> dict:
    """Get a summary of all decision configuration values."""
    return {
        "max_concurrent_decisions": DEFAULT_MAX_CONCURRENT_DECISIONS,
        "timeout_seconds": DECISION_TIMEOUT_SECONDS,
        "confidence_threshold": DEFAULT_CONFIDENCE_THRESHOLD,
        "auto_cleanup_enabled": AUTO_CLEANUP_COMPLETED_DECISIONS,
        "cleanup_interval_minutes": CLEANUP_INTERVAL_MINUTES,
        "max_history": MAX_DECISION_HISTORY,
        "validation_ranges": {
            "confidence": f"{MIN_CONFIDENCE_THRESHOLD}-{MAX_CONFIDENCE_THRESHOLD}",
            "concurrent": f"{MIN_CONCURRENT_DECISIONS}-{MAX_CONCURRENT_DECISIONS}",
            "timeout": f"{MIN_TIMEOUT_SECONDS}-{MAX_TIMEOUT_SECONDS}",
            "cleanup": f"{MIN_CLEANUP_INTERVAL}-{MAX_CLEANUP_INTERVAL}",
        },
    }


# ================================
# INITIALIZATION
# ================================

# Validate constants on import
if not validate_decision_constants():
    raise ValueError("Decision constants validation failed - check configuration values")
