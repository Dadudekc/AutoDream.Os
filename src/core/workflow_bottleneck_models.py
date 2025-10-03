"""
Workflow Bottleneck Models - V2 Compliant
=========================================

Data models and enums for workflow bottleneck elimination.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

from dataclasses import dataclass
from enum import Enum


class BottleneckType(Enum):
    """Bottleneck type enumeration."""

    MANUAL_INBOX_SCAN = "manual_inbox_scan"
    MANUAL_TASK_EVAL = "manual_task_eval"
    MANUAL_DEVLOG_CREATE = "manual_devlog_create"
    MANUAL_COMPLIANCE_CHECK = "manual_compliance_check"
    MANUAL_DB_QUERY = "manual_db_query"


@dataclass
class BottleneckElimination:
    """Bottleneck elimination result."""

    bottleneck_type: BottleneckType
    eliminated: bool
    time_saved_per_cycle: float
    automation_created: str
    manual_steps_removed: int


@dataclass
class AutomationScript:
    """Automation script configuration."""

    script_name: str
    script_path: str
    description: str
    time_saved: float
    manual_steps_replaced: int


@dataclass
class BottleneckSummary:
    """Bottleneck elimination summary."""

    total_bottlenecks_eliminated: int
    total_time_saved: float
    total_manual_steps_removed: int
    automation_scripts_created: list[AutomationScript]
    efficiency_gain_percentage: float
