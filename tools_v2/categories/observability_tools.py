#!/usr/bin/env python3
"""
Observability Tools
===================

Tools for metrics, monitoring, and system health.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging
from typing import Any

from ..adapters.base_adapter import IToolAdapter, ToolSpec, ToolResult

logger = logging.getLogger(__name__)


class MetricsSnapshotTool(IToolAdapter):
    """Get current metrics snapshot."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="obs.metrics", version="1.0.0", category="observability",
                       summary="Get current metrics snapshot", required_params=[], optional_params={})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        return (True, [])

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute metrics snapshot."""
        try:
            from src.obs.metrics import snapshot

            metrics = snapshot()

            output = {"metrics": metrics, "count": len(metrics)}
            return ToolResult(success=True, output=output)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class MetricsTool(IToolAdapter):
    """Get specific metric value."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="obs.get", version="1.0.0", category="observability",
                       summary="Get specific metric value", required_params=["key"], optional_params={})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute metric retrieval."""
        try:
            if params is None:
                return ToolResult(success=False, output=None, error_message="params required", exit_code=1)
                
            from src.obs.metrics import get

            key = params.get("key")
            if not key:
                return ToolResult(success=False, output=None, error_message="key required", exit_code=1)

            value = get(key)

            output = {"key": key, "value": value}
            return ToolResult(success=True, output=output)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class SystemHealthTool(IToolAdapter):
    """Check system health status."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="obs.health", version="1.0.0", category="observability",
                       summary="Check system health status", required_params=[], optional_params={})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        return (True, [])

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute health check."""
        try:
            from src.obs.metrics import get

            # Check key metrics
            health = {
                "messaging": {
                    "sent": get("messaging.sent", 0),
                    "failed": get("messaging.failed", 0),
                },
                "msg_task": {
                    "ingest_ok": get("msg_task.ingest.ok", 0),
                    "ingest_fail": get("msg_task.ingest.fail", 0),
                    "duplicates": get("msg_task.dedupe.duplicate", 0),
                },
                "oss": {
                    "clone_ok": get("oss.clone.ok", 0),
                    "clone_fail": get("oss.clone.fail", 0),
                },
            }

            # Calculate success rates
            msg_total = health["messaging"]["sent"] + health["messaging"]["failed"]
            ingest_total = health["msg_task"]["ingest_ok"] + health["msg_task"]["ingest_fail"]

            health["messaging"]["success_rate"] = (
                (health["messaging"]["sent"] / msg_total * 100) if msg_total > 0 else 100
            )
            health["msg_task"]["success_rate"] = (
                (health["msg_task"]["ingest_ok"] / ingest_total * 100) if ingest_total > 0 else 100
            )

            output = {"health": health, "status": "operational"}
            return ToolResult(success=True, output=output)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class SLOCheckTool(IToolAdapter):
    """Check SLO compliance."""

    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="obs.slo", version="1.0.0", category="observability",
                       summary="Check SLO compliance", required_params=[], optional_params={})
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        return (True, [])

    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        """Execute SLO check."""
        try:
            from src.obs.metrics import get

            slos = {}

            # Message-Task SLOs
            ingest_ok = get("msg_task.ingest.ok", 0)
            ingest_fail = get("msg_task.ingest.fail", 0)
            ingest_total = ingest_ok + ingest_fail

            if ingest_total > 0:
                ingest_rate = (ingest_ok / ingest_total) * 100
                slos["msg_task_ingest"] = {
                    "current": ingest_rate,
                    "target": 99.0,
                    "passing": ingest_rate >= 99.0,
                }

            # Messaging SLOs
            msg_sent = get("messaging.sent", 0)
            msg_failed = get("messaging.failed", 0)
            msg_total = msg_sent + msg_failed

            if msg_total > 0:
                msg_rate = (msg_sent / msg_total) * 100
                slos["messaging_delivery"] = {
                    "current": msg_rate,
                    "target": 100.0,
                    "passing": msg_rate == 100.0,
                }

            passing = all(slo.get("passing", True) for slo in slos.values())

            output = {
                "slos": slos,
                "all_passing": passing,
                "checked": len(slos),
            }
            return ToolResult(success=True, output=output)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)
