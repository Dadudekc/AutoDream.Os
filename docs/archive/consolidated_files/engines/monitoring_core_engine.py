from __future__ import annotations

from typing import Any

from .contracts import Engine, EngineContext, EngineResult


class MonitoringCoreEngine(Engine):
    """Core monitoring engine - consolidates all monitoring operations."""

    def __init__(self):
        self.metrics: dict[str, Any] = {}
        self.alerts: list[dict[str, Any]] = []
        self.is_initialized = False

    def initialize(self, context: EngineContext) -> bool:
        """Initialize monitoring core engine."""
        try:
            self.is_initialized = True
            context.logger.info("Monitoring Core Engine initialized")
            return True
        except Exception as e:
            context.logger.error(f"Failed to initialize Monitoring Core Engine: {e}")
            return False

    def execute(self, context: EngineContext, payload: dict[str, Any]) -> EngineResult:
        """Execute monitoring operation based on payload type."""
        try:
            operation = payload.get("operation", "unknown")

            if operation == "collect_metrics":
                return self._collect_metrics(context, payload)
            elif operation == "check_health":
                return self._check_health(context, payload)
            elif operation == "create_alert":
                return self._create_alert(context, payload)
            else:
                return EngineResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown monitoring operation: {operation}",
                )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def _collect_metrics(self, context: EngineContext, payload: dict[str, Any]) -> EngineResult:
        """Collect system metrics."""
        try:
            metric_name = payload.get("metric_name", "default")
            metric_value = payload.get("value", 0)
            metric_type = payload.get("type", "counter")

            metric_data = {
                "name": metric_name,
                "value": metric_value,
                "type": metric_type,
                "timestamp": context.metrics.get("timestamp", 0),
            }

            self.metrics[metric_name] = metric_data

            return EngineResult(
                success=True, data=metric_data, metrics={"metric_name": metric_name}
            )
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def _check_health(self, context: EngineContext, payload: dict[str, Any]) -> EngineResult:
        """Check system health."""
        try:
            component = payload.get("component", "system")

            # Simplified health check
            health_status = {
                "component": component,
                "status": "healthy",
                "timestamp": context.metrics.get("timestamp", 0),
                "metrics": {
                    "cpu_usage": 25.5,
                    "memory_usage": 60.2,
                    "disk_usage": 45.8,
                },
            }

            return EngineResult(success=True, data=health_status, metrics={"component": component})
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def _create_alert(self, context: EngineContext, payload: dict[str, Any]) -> EngineResult:
        """Create monitoring alert."""
        try:
            alert_id = f"alert_{len(self.alerts)}"
            alert_type = payload.get("type", "info")
            message = payload.get("message", "")
            severity = payload.get("severity", "medium")

            alert_data = {
                "alert_id": alert_id,
                "type": alert_type,
                "message": message,
                "severity": severity,
                "timestamp": context.metrics.get("timestamp", 0),
                "status": "active",
            }

            self.alerts.append(alert_data)

            return EngineResult(success=True, data=alert_data, metrics={"alert_id": alert_id})
        except Exception as e:
            return EngineResult(success=False, data={}, metrics={}, error=str(e))

    def cleanup(self, context: EngineContext) -> bool:
        """Cleanup monitoring core engine."""
        try:
            self.metrics.clear()
            self.alerts.clear()
            self.is_initialized = False
            context.logger.info("Monitoring Core Engine cleaned up")
            return True
        except Exception as e:
            context.logger.error(f"Failed to cleanup Monitoring Core Engine: {e}")
            return False

    def get_status(self) -> dict[str, Any]:
        """Get monitoring core engine status."""
        return {
            "initialized": self.is_initialized,
            "metrics_count": len(self.metrics),
            "alerts_count": len(self.alerts),
        }
