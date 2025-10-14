#!/usr/bin/env python3
"""
Feature Flags
=============

Runtime feature toggles for safe rollbacks.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import os

# Feature flags (env-based)
FF_MSG_TASK = os.getenv("FF_MSG_TASK", "on") == "on"
FF_OSS_CLI = os.getenv("FF_OSS_CLI", "on") == "on"
FF_CONCURRENT_MSG_LOCK = os.getenv("FF_CONCURRENT_MSG_LOCK", "on") == "on"
FF_ERROR_CLASSIFICATION = os.getenv("FF_ERROR_CLASSIFICATION", "on") == "on"


def is_enabled(feature: str) -> bool:
    """
    Check if feature is enabled.

    Args:
        feature: Feature name (msg_task, oss_cli, etc.)

    Returns:
        True if enabled
    """
    flags = {
        "msg_task": FF_MSG_TASK,
        "oss_cli": FF_OSS_CLI,
        "concurrent_msg_lock": FF_CONCURRENT_MSG_LOCK,
        "error_classification": FF_ERROR_CLASSIFICATION,
    }

    return flags.get(feature, False)


def disable_feature(feature: str):
    """Disable feature at runtime (for rollback)."""
    os.environ[f"FF_{feature.upper()}"] = "off"


def enable_feature(feature: str):
    """Enable feature at runtime."""
    os.environ[f"FF_{feature.upper()}"] = "on"
