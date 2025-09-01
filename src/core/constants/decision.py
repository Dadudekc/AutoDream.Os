from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
Decision Constants - Decision Module Definitions

This module provides decision-related constants.

Agent: Agent-6 (Performance Optimization Manager)
Mission: Autonomous Cleanup - V2 Compliance
Status: SSOT Consolidation in Progress
"""

# Decision module constants
DEFAULT_MAX_CONCURRENT_DECISIONS = get_config('DEFAULT_MAX_CONCURRENT_DECISIONS', 100)
DECISION_TIMEOUT_SECONDS = get_config('DECISION_TIMEOUT_SECONDS', 300)
DEFAULT_CONFIDENCE_THRESHOLD = get_config('DEFAULT_CONFIDENCE_THRESHOLD', 0.7)
AUTO_CLEANUP_COMPLETED_DECISIONS = get_config('AUTO_CLEANUP_COMPLETED_DECISIONS', True)
CLEANUP_INTERVAL_MINUTES = get_config('CLEANUP_INTERVAL_MINUTES', 15)
MAX_DECISION_HISTORY = get_config('MAX_DECISION_HISTORY', 1000)
