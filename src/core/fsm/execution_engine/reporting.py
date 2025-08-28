#!/usr/bin/env python3
"""Reporting and statistics mixin for FSM core."""

import json
from dataclasses import asdict
from datetime import datetime
from string import Template
from typing import Any, Callable, Dict, Optional


class Reporting:
    """Provides reporting utilities."""

    # Report format plugins. Mapped as {format_name: formatter_callable}
    report_plugins: Dict[str, Callable[[Dict[str, Any]], str]]

    def _ensure_plugins(self) -> None:
        if not hasattr(self, "report_plugins"):
            self.report_plugins = {}

    # ------------------------------------------------------------------
    # Data gathering
    def gather_workflow_data(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Gather raw workflow data for reporting."""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        return asdict(workflow)

    # ------------------------------------------------------------------
    # Formatting
    def register_report_plugin(
        self, format_name: str, formatter: Callable[[Dict[str, Any]], str]
    ) -> None:
        """Register a formatter plugin for a report format."""
        self._ensure_plugins()
        self.report_plugins[format_name.lower()] = formatter

    def format_report(self, data: Dict[str, Any], format: str = "json") -> str:
        """Format report data into a string using built-in or plugin formatters."""
        self._ensure_plugins()
        fmt = format.lower()
        if fmt in self.report_plugins:
            return self.report_plugins[fmt](data)
        if fmt == "json":
            return json.dumps(data, indent=2, default=str)
        return Template("Report format '${format}' not supported").substitute(
            format=format
        )

    def get_system_stats(self) -> Dict[str, Any]:
        """Get FSM system statistics."""
        return {
            "total_workflows": len(self.workflows),
            "active_workflows": len(self.active_workflows),
            "queued_workflows": len(self.workflow_queue),
            "total_workflows_executed": self.total_workflows_executed,
            "successful_workflows": self.successful_workflows,
            "failed_workflows": self.failed_workflows,
            "total_state_transitions": self.total_state_transitions,
            "system_status": "running" if self.is_running else "stopped",
            "monitoring_active": self.monitoring_active,
            "last_updated": datetime.now().isoformat(),
        }

    # ------------------------------------------------------------------
    # Export
    def export_workflow_report(
        self, workflow_id: str, format: str = "json"
    ) -> Optional[str]:
        """Export workflow execution report."""
        try:
            data = self.gather_workflow_data(workflow_id)
            if data is None:
                return None
            return self.format_report(data, format)
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(
                Template("Failed to export workflow report: ${error}").substitute(
                    error=e
                )
            )
            return None

    def clear_history(self) -> None:
        """Clear workflow history."""
        self.workflows.clear()
        self.active_workflows.clear()
        self.workflow_queue.clear()
        self.total_workflows_executed = 0
        self.successful_workflows = 0
        self.failed_workflows = 0
        self.total_state_transitions = 0
        self.logger.info("✅ FSM history cleared")


__all__ = ["Reporting"]
