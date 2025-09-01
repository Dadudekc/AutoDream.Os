from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
Manager Constants - Manager Module Definitions

This module provides manager-related constants.

Agent: Agent-6 (Performance Optimization Manager)
Mission: Autonomous Cleanup - V2 Compliance
Status: SSOT Consolidation in Progress
"""

# Manager module constants
DEFAULT_HEALTH_CHECK_INTERVAL = get_config('DEFAULT_HEALTH_CHECK_INTERVAL', 30)
DEFAULT_MAX_STATUS_HISTORY = get_config('DEFAULT_MAX_STATUS_HISTORY', 1000)
DEFAULT_AUTO_RESOLVE_TIMEOUT = get_config('DEFAULT_AUTO_RESOLVE_TIMEOUT', 3600)
STATUS_CONFIG_PATH = "config/status_manager.json"
