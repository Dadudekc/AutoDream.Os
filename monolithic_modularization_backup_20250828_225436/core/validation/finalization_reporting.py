"""Reporting helpers for validation system finalization."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from .finalization_constants import AGENT_NAME, REPORT_PATH, TASK_ID, TASK_NAME


def format_completion_report(report: Dict[str, Any]) -> str:
    """Format the completion report as markdown."""
    return (
        f"# {TASK_ID} - {TASK_NAME} Report\n\n"
        f"**Agent**: {AGENT_NAME}\n"
        f"**Status**: {report.get('overall_status', 'UNKNOWN')}\n"
        f"**Completion Time**: {report['completion_timestamp']}\n"
        f"**Execution Duration**: {report['execution_time']:.2f} seconds\n"
    )


def generate_completion_report(results: Dict[str, Any]) -> Path:
    """Generate the completion report and return its path."""
    completion_report = {
        "overall_status": results.get("status", "UNKNOWN"),
        "completion_timestamp": datetime.now().isoformat(),
        "execution_time": results.get("completion_time", 0.0),
        "system_health": results.get("system_health", {}),
        "integration_tests": results.get("integration_tests", {}),
        "performance_metrics": results.get("performance_metrics", {}),
        "framework_validation": results.get("framework_validation", {}),
    }
    report_path = REPORT_PATH
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(format_completion_report(completion_report))
    return report_path
