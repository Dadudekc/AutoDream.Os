#!/usr/bin/env python3
"""Reporting and statistics mixin for FSM core."""

import json
from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, Optional


class Reporting:
    """Provides reporting utilities."""

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

    def export_workflow_report(
        self, workflow_id: str, format: str = "json"
    ) -> Optional[str]:
        """Export workflow execution report."""
        try:
            workflow = self.workflows.get(workflow_id)
            if not workflow:
                return None

            if format.lower() == "json":
                return json.dumps(asdict(workflow), indent=2, default=str)
            return f"Report format '{format}' not supported"

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to export workflow report: {e}")
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
