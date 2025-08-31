"""Authoritative constants for the AutoDream system."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple, Final

from .fsm.fsm_core import StateDefinition, TransitionDefinition, TransitionType

# -----------------------------------------------------------------------------
# Repository paths
# -----------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]
HEALTH_REPORTS_DIR = ROOT_DIR / "health_reports"
HEALTH_CHARTS_DIR = ROOT_DIR / "health_charts"
MONITORING_DIR = ROOT_DIR / "agent_workspaces" / "monitoring"

# -----------------------------------------------------------------------------
# Decision module
# -----------------------------------------------------------------------------
DEFAULT_MAX_CONCURRENT_DECISIONS = 100
DECISION_TIMEOUT_SECONDS = 300
DEFAULT_CONFIDENCE_THRESHOLD = 0.7
AUTO_CLEANUP_COMPLETED_DECISIONS = True
CLEANUP_INTERVAL_MINUTES = 15
MAX_DECISION_HISTORY = 1000

# -----------------------------------------------------------------------------
# Manager module
# -----------------------------------------------------------------------------
DEFAULT_HEALTH_CHECK_INTERVAL = 30
DEFAULT_MAX_STATUS_HISTORY = 1000
DEFAULT_AUTO_RESOLVE_TIMEOUT = 3600
STATUS_CONFIG_PATH = "config/status_manager.json"

# -----------------------------------------------------------------------------
# Core FSM definitions
# -----------------------------------------------------------------------------
CORE_FSM_START_STATE = StateDefinition(
    name="start",
    description="Starting state",
    entry_actions=[],
    exit_actions=[],
    timeout_seconds=None,
    retry_count=0,
    retry_delay=0.0,
    required_resources=[],
    dependencies=[],
    metadata={},
)

CORE_FSM_PROCESS_STATE = StateDefinition(
    name="process",
    description="Processing state",
    entry_actions=[],
    exit_actions=[],
    timeout_seconds=None,
    retry_count=0,
    retry_delay=0.0,
    required_resources=[],
    dependencies=[],
    metadata={},
)

CORE_FSM_END_STATE = StateDefinition(
    name="end",
    description="Ending state",
    entry_actions=[],
    exit_actions=[],
    timeout_seconds=None,
    retry_count=0,
    retry_delay=0.0,
    required_resources=[],
    dependencies=[],
    metadata={},
)

CORE_FSM_DEFAULT_STATES = [
    CORE_FSM_START_STATE,
    CORE_FSM_PROCESS_STATE,
    CORE_FSM_END_STATE,
]

CORE_FSM_TRANSITION_START_PROCESS = TransitionDefinition(
    from_state="start",
    to_state="process",
    transition_type=TransitionType.AUTOMATIC,
    condition=None,
    priority=1,
    timeout_seconds=None,
    actions=[],
    metadata={},
)

CORE_FSM_TRANSITION_PROCESS_END = TransitionDefinition(
    from_state="process",
    to_state="end",
    transition_type=TransitionType.AUTOMATIC,
    condition=None,
    priority=1,
    timeout_seconds=None,
    actions=[],
    metadata={},
)

CORE_FSM_DEFAULT_TRANSITIONS = [
    CORE_FSM_TRANSITION_START_PROCESS,
    CORE_FSM_TRANSITION_PROCESS_END,
]

# -----------------------------------------------------------------------------
# Baseline module
# -----------------------------------------------------------------------------
DEFAULT_METRICS = [
    "code_complexity",
    "maintainability_index",
    "duplication_percentage",
    "refactoring_duration",
    "performance_improvement",
    "memory_usage",
    "cpu_utilization",
    "lines_of_code",
    "test_coverage",
    "bug_density",
]

DEFAULT_BASELINE_CONFIG = {
    "auto_calibration_enabled": True,
    "calibration_threshold": 0.8,
    "max_baselines_per_type": 5,
    "baseline_retention_days": 90,
    "trend_analysis_enabled": True,
    "forecast_horizon_days": 30,
    "validation_interval_hours": 24,
    "default_metrics": DEFAULT_METRICS,
}

# -----------------------------------------------------------------------------
# FSM workflow defaults
# -----------------------------------------------------------------------------
FSM_DEFAULT_STATES: Tuple[str, ...] = (
    "pending",
    "in_progress",
    "completed",
    "failed",
)

FSM_DEFAULT_TRANSITIONS: Dict[str, Tuple[str, ...]] = {
    "pending": ("in_progress",),
    "in_progress": ("completed", "failed"),
    "completed": (),
    "failed": (),
}

# -----------------------------------------------------------------------------
# Extended AI/ML
# -----------------------------------------------------------------------------
DEFAULT_AI_MANAGER_CONFIG: Final[str] = "config/ai_ml/ai_manager.json"

WORKFLOW_STATUS_CREATED: Final[str] = "created"
WORKFLOW_STATUS_RUNNING: Final[str] = "running"
WORKFLOW_STATUS_COMPLETED: Final[str] = "completed"
WORKFLOW_STATUS_FAILED: Final[str] = "failed"

# -----------------------------------------------------------------------------
# Status monitor service
# -----------------------------------------------------------------------------
DEFAULT_AGENT_IDS = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-4",
    "Agent-5",
]

ERROR_PENALTY = 10
WARNING_PENALTY = 5
MIN_ACTIVE_AGENTS = 2
LOW_ACTIVE_AGENT_PENALTY = 20

STATUS_EMOJIS = {
    "active": "🟢",
    "standby": "🟡",
    "offline": "🔴",
}

# -----------------------------------------------------------------------------
# Generic service constants
# -----------------------------------------------------------------------------
SUMMARY_PASSED = "passed"
SUMMARY_FAILED = "failed"

RESULTS_KEY = "results"
SUMMARY_KEY = "summary"

DEFAULT_CONTRACT_ID = "unknown"

# -----------------------------------------------------------------------------
# Trading intelligence service
# -----------------------------------------------------------------------------
DEFAULT_REQUIRED_COLUMNS = {"Close", "Volume"}
RSI_PERIOD = 14

__all__ = [
    "ROOT_DIR",
    "HEALTH_REPORTS_DIR",
    "HEALTH_CHARTS_DIR",
    "MONITORING_DIR",
    "DEFAULT_MAX_CONCURRENT_DECISIONS",
    "DECISION_TIMEOUT_SECONDS",
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "AUTO_CLEANUP_COMPLETED_DECISIONS",
    "CLEANUP_INTERVAL_MINUTES",
    "MAX_DECISION_HISTORY",
    "DEFAULT_HEALTH_CHECK_INTERVAL",
    "DEFAULT_MAX_STATUS_HISTORY",
    "DEFAULT_AUTO_RESOLVE_TIMEOUT",
    "STATUS_CONFIG_PATH",
    "CORE_FSM_START_STATE",
    "CORE_FSM_PROCESS_STATE",
    "CORE_FSM_END_STATE",
    "CORE_FSM_DEFAULT_STATES",
    "CORE_FSM_TRANSITION_START_PROCESS",
    "CORE_FSM_TRANSITION_PROCESS_END",
    "CORE_FSM_DEFAULT_TRANSITIONS",
    "DEFAULT_METRICS",
    "DEFAULT_BASELINE_CONFIG",
    "FSM_DEFAULT_STATES",
    "FSM_DEFAULT_TRANSITIONS",
    "DEFAULT_AI_MANAGER_CONFIG",
    "WORKFLOW_STATUS_CREATED",
    "WORKFLOW_STATUS_RUNNING",
    "WORKFLOW_STATUS_COMPLETED",
    "WORKFLOW_STATUS_FAILED",
    "DEFAULT_AGENT_IDS",
    "ERROR_PENALTY",
    "WARNING_PENALTY",
    "MIN_ACTIVE_AGENTS",
    "LOW_ACTIVE_AGENT_PENALTY",
    "STATUS_EMOJIS",
    "SUMMARY_PASSED",
    "SUMMARY_FAILED",
    "RESULTS_KEY",
    "SUMMARY_KEY",
    "DEFAULT_CONTRACT_ID",
    "DEFAULT_REQUIRED_COLUMNS",
    "RSI_PERIOD",
]
