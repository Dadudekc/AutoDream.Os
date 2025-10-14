#!/usr/bin/env python3
"""
UNIFIED CONFIGURATION SSOT - SINGLE SOURCE OF TRUTH
===================================================

THE definitive configuration system for Agent Cellphone V2.
Consolidates ALL configuration from 12 files into 1 unified SSOT.

V2 COMPLIANCE REFACTOR HISTORY:
- Agent-7 (2025-10-12): Consolidated 12 config files → 471 lines
- Agent-2 (2025-10-13): Modularized → 4 modules <150 lines each (ROI 32.26)

V2 Compliance: Modular architecture, <100 lines main file
Architecture: Dataclass-based with validation, backward compatible

Consolidates:
- config_core.py (manager)
- unified_config.py (dataclasses)
- config_browser.py (browser config)
- config_thresholds.py (thresholds)
- config_defaults.py (defaults)
- shared_utils/config.py (env loading)
- infrastructure/browser/unified/config.py (browser paths)

Authors:
- Agent-7 - Web Development Specialist (Config SSOT Consolidation)
- Agent-2 - Architecture & Design Specialist (Modular Refactor, ROI 32.26)
License: MIT
"""

# Re-export all components for backwards compatibility
from .config.config_accessors import (
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
from .config.config_dataclasses import (
    AgentConfig,
    BrowserConfig,
    FilePatternConfig,
    ReportConfig,
    TestConfig,
    ThresholdConfig,
    TimeoutConfig,
)
from .config.config_enums import ConfigEnvironment, ConfigSource, ReportFormat
from .config.config_manager import UnifiedConfigManager

# Public API - Backwards compatible with original config_ssot.py
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
