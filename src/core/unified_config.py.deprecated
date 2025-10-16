#!/usr/bin/env python3
"""
DEPRECATED: This file has been replaced by src/core/config/config_manager.py
=============================================================================

This file is DEPRECATED as part of DUP-001 ConfigManager SSOT consolidation.

CONSOLIDATION: Agent-8 (2025-10-16) - DUP-001 SSOT Fix
All functionality has been moved to src/core/config/config_manager.py

Please update your imports to use src/core/config_ssot instead:

OLD:
    from src.core.unified_config import get_unified_config, TimeoutConfig

NEW:
    from src.core.config_ssot import get_unified_config, TimeoutConfig

This file will be removed in a future release.
"""

import warnings

warnings.warn(
    "unified_config.py is deprecated. Use src.core.config_ssot instead. "
    "This file will be removed in a future release.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export from SSOT for backward compatibility
from .config_ssot import (
    AgentConfig,
    BrowserConfig,
    ConfigEnvironment,
    ConfigSource,
    FilePatternConfig,
    ReportConfig,
    ReportFormat,
    TestConfig,
    ThresholdConfig,
    TimeoutConfig,
    UnifiedConfigManager,
    get_agent_config,
    get_browser_config,
    get_config,
    get_file_pattern_config,
    get_report_config,
    get_test_config,
    get_threshold_config,
    get_timeout_config,
    get_unified_config,
    reload_config,
    validate_config,
)

# Deprecated class alias
UnifiedConfig = UnifiedConfigManager

__all__ = [
    # Enums
    "ConfigEnvironment",
    "ConfigSource",
    "ReportFormat",
    # Dataclasses
    "TimeoutConfig",
    "AgentConfig",
    "BrowserConfig",
    "ThresholdConfig",
    "FilePatternConfig",
    "TestConfig",
    "ReportConfig",
    # Manager
    "UnifiedConfigManager",
    "UnifiedConfig",  # Deprecated alias
    # Accessor functions
    "get_config",
    "get_unified_config",
    "get_timeout_config",
    "get_agent_config",
    "get_browser_config",
    "get_threshold_config",
    "get_file_pattern_config",
    "get_test_config",
    "get_report_config",
    "validate_config",
    "reload_config",
]
