"""Central configuration for the quality monitoring system."""

DEFAULT_CHECK_INTERVAL = 30.0

DEFAULT_ALERT_RULES = {
    "test_failure": {
        "threshold": 0,
        "severity": "high",
        "message": "Test failures detected",
    },
    "performance_degradation": {
        "threshold": 100.0,
        "severity": "medium",
        "message": "Performance degradation detected",
    },
    "low_coverage": {
        "threshold": 80.0,
        "severity": "medium",
        "message": "Test coverage below threshold",
    },
}
