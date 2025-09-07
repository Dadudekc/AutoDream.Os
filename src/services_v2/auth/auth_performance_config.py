
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration helpers for authentication performance monitoring."""
from typing import Dict, Any


def get_default_config() -> Dict[str, Any]:
    """Return default configuration for the auth performance monitor."""
    return {
        "monitoring_interval": 5.0,  # 5 seconds
        "max_metrics_history": 1000,
        "max_alerts_history": 100,
        "enable_real_time_monitoring": True,
        "enable_performance_alerts": True,
        "enable_baseline_calculation": True,
        "baseline_calculation_period": 300,  # 5 minutes
        "performance_thresholds": {
            "auth_duration": {"warning": 0.5, "critical": 1.0},  # 500ms / 1s
            "success_rate": {"warning": 0.95, "critical": 0.90},  # 95% / 90%
            "concurrent_auths": {"warning": 50, "critical": 100},
            "error_rate": {"warning": 0.05, "critical": 0.10},
        },
        "alert_cooldown": 300,  # 5 minutes between similar alerts
        "performance_optimization": {
            "enable_auto_optimization": False,
            "optimization_threshold": 0.8,  # 80% of threshold
            "max_optimization_attempts": 3,
        },
    }
