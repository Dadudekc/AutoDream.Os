# Shared utilities for communication systems.

"""Shared utilities for communication systems."""

import logging
from enum import Enum

# Configure logging once for all communications modules
logging.basicConfig(level=logging.INFO)


def get_logger(name: str = __name__) -> logging.Logger:
    """Return a module-specific logger."""
    return logging.getLogger(name)


class TestStatus(Enum):
    """Test execution status."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class TestCategory(Enum):
    """Test categories."""

    COMMUNICATION = "communication"
    PROTOCOL = "protocol"
    COORDINATION = "coordination"
    PERFORMANCE = "performance"
    INTEGRATION = "integration"
    STRESS = "stress"


class AlertSeverity(Enum):
    """Alert severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class HealthStatus(Enum):
    """Health status enumeration."""

    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"
