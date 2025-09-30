#!/usr/bin/env python3
"""
Operational Dashboard & Analytics Tool
=====================================

Real-time operational visibility and analytics for Team Alpha coordination.
Refactored into modular components for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

# Import all components from refactored modules
from .operational_dashboard_tool_core import (
    AgentPerformance,
    AlertLevel,
    MetricType,
    OperationalAlert,
    ProjectProgress,
    QualityGateResult,
)
from .operational_dashboard_tool_main import OperationalDashboard, main
from .operational_dashboard_tool_utils import (
    calculate_quality_score,
    count_completed_tasks,
    count_total_tasks,
    extract_metric,
    generate_recommendations,
    load_agent_performance_data,
    load_project_progress_data,
    load_quality_gate_data,
    load_v3_coordination_data,
)

# Re-export main classes for backward compatibility
__all__ = [
    # Core classes
    "MetricType",
    "AlertLevel",
    "QualityGateResult",
    "AgentPerformance",
    "ProjectProgress",
    "OperationalAlert",
    # Main dashboard
    "OperationalDashboard",
    # Utility functions
    "calculate_quality_score",
    "extract_metric",
    "count_completed_tasks",
    "count_total_tasks",
    "generate_recommendations",
    "load_v3_coordination_data",
    "load_quality_gate_data",
    "load_agent_performance_data",
    "load_project_progress_data",
    # CLI
    "main",
]


# For direct execution
if __name__ == "__main__":
    main()
