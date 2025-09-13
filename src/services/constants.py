#!/usr/bin/env python3
"""
Services Constants - V2_SWARM Service Layer Constants
====================================================

Common constants used across the services layer.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

# Service status constants
SERVICE_STATUS_ACTIVE = "active"
SERVICE_STATUS_INACTIVE = "inactive"
SERVICE_STATUS_ERROR = "error"

# Default timeouts
DEFAULT_TIMEOUT = 30
DEFAULT_RESPONSE_TIMEOUT = 60

# File size limits
MAX_FILE_SIZE = 400  # V2 compliance limit
MAJOR_VIOLATION_SIZE = 600  # Major violation threshold

# Quality thresholds
MIN_TEST_COVERAGE = 85
MIN_SUCCESS_RATE = 99.9

__all__ = [
    "SERVICE_STATUS_ACTIVE",
    "SERVICE_STATUS_INACTIVE",
    "SERVICE_STATUS_ERROR",
    "DEFAULT_TIMEOUT",
    "DEFAULT_RESPONSE_TIMEOUT",
    "MAX_FILE_SIZE",
    "MAJOR_VIOLATION_SIZE",
    "MIN_TEST_COVERAGE",
    "MIN_SUCCESS_RATE"
]
