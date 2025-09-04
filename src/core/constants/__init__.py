"""
Unified Constants Package

This package provides unified constants for the system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: Autonomous Cleanup - V2 Compliance
Status: SSOT Consolidation in Progress
"""


__all__ = [
    # Paths
    "ROOT_DIR",
    "HEALTH_REPORTS_DIR",
    "HEALTH_CHARTS_DIR",
    "MONITORING_DIR",
    # Decision
    "DEFAULT_MAX_CONCURRENT_DECISIONS",
    "DECISION_TIMEOUT_SECONDS",
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "AUTO_CLEANUP_COMPLETED_DECISIONS",
    "CLEANUP_INTERVAL_MINUTES",
    "MAX_DECISION_HISTORY",
    # Manager
    "DEFAULT_HEALTH_CHECK_INTERVAL",
    "DEFAULT_MAX_STATUS_HISTORY",
    "DEFAULT_AUTO_RESOLVE_TIMEOUT",
    "STATUS_CONFIG_PATH",
    # FSM
    "CORE_FSM_START_STATE",
    "CORE_FSM_PROCESS_STATE",
    "CORE_FSM_END_STATE",
    "CORE_FSM_DEFAULT_STATES",
    "CORE_FSM_TRANSITION_START_PROCESS",
    "CORE_FSM_TRANSITION_PROCESS_END",
]
