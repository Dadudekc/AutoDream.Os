"""Shared constants for performance validation."""

DEFAULT_THRESHOLDS = {
    "cpu_usage_percent": {
        "warning": 80.0,
        "critical": 95.0,
        "operator": ">=",
    },
    "memory_usage_percent": {
        "warning": 85.0,
        "critical": 95.0,
        "operator": ">=",
    },
    "disk_usage_percent": {
        "warning": 90.0,
        "critical": 98.0,
        "operator": ">=",
    },
    "response_time_ms": {
        "warning": 500.0,
        "critical": 1000.0,
        "operator": ">=",
    },
    "network_latency_ms": {
        "warning": 100.0,
        "critical": 200.0,
        "operator": ">=",
    },
}

# Maximum number of validation results kept in history before trimming.
HISTORY_LIMIT = 10000
# Number of results to retain after trimming history.
HISTORY_RETAIN = 5000
