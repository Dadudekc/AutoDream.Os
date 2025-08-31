
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration utilities for continuous quality monitoring."""
from __future__ import annotations

from src.core.config_loader import load_config as _load_config

DEFAULT_CONFIG = {
    "monitoring": {
        "enabled": True,
        "interval_seconds": 300,
        "auto_validation": True,
        "alert_thresholds": {
            "critical": 60.0,
            "high": 70.0,
            "medium": 80.0,
            "low": 90.0,
        },
    },
    "quality_gates": {
        "enforce_loc_compliance": True,
        "enforce_code_quality": True,
        "enforce_enterprise_standards": True,
        "enforce_test_coverage": True,
    },
    "trend_analysis": {
        "history_window_days": 7,
        "trend_threshold": 5.0,
        "improvement_target": 2.0,
    },
}


def load_config(config_path: str) -> dict:
    """Load configuration from ``config_path`` using the SSOT loader."""
    return _load_config(config_path, DEFAULT_CONFIG)
