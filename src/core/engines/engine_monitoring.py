"""
Engine Monitoring - V2 Compliance Module
=======================================

Monitors engine performance and health following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from datetime import datetime
from typing import Any, Dict, List

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None


class EngineMetrics:
    """Tracks engine performance metrics."""

    def __init__(self, engine_id: str):
        """Initialize metrics tracking."""
        self.engine_id = engine_id
        self.start_time = datetime.now()
        self.operation_count = 0
        self.error_count = 0
        self.success_count = 0
        self.average_response_time = 0.0
        self.peak_memory_usage = 0
        self.cpu_usage_history: List[float] = []
        self.memory_usage_history: List[float] = []

    def record_operation(self, success: bool, response_time: float):
        """Record an operation result."""
        self.operation_count += 1

        if success:
            self.success_count += 1
        else:
            self.error_count += 1

        # Update average response time
        if self.operation_count == 1:
            self.average_response_time = response_time
        else:
            self.average_response_time = (
                (self.average_response_time * (self.operation_count - 1)) + response_time
            ) / self.operation_count

        # Track resource usage
        self._update_resource_usage()

    def _update_resource_usage(self):
        """Update CPU and memory usage tracking."""
        if not PSUTIL_AVAILABLE:
            # If psutil is not available, skip resource monitoring
            return

        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_info = psutil.virtual_memory()

            self.cpu_usage_history.append(cpu_percent)
            self.memory_usage_history.append(memory_info.percent)

            # Keep only last 100 readings
            if len(self.cpu_usage_history) > 100:
                self.cpu_usage_history.pop(0)
                self.memory_usage_history.pop(0)

            # Update peak memory
            if memory_info.percent > self.peak_memory_usage:
                self.peak_memory_usage = memory_info.percent

        except Exception:
            # Silently handle resource monitoring failures
            pass

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary."""
        uptime = (datetime.now() - self.start_time).total_seconds()

        return {
            "engine_id": self.engine_id,
            "uptime_seconds": uptime,
            "total_operations": self.operation_count,
            "successful_operations": self.success_count,
            "failed_operations": self.error_count,
            "success_rate": (self.success_count / self.operation_count) if self.operation_count > 0 else 0,
            "average_response_time": self.average_response_time,
            "peak_memory_usage": self.peak_memory_usage,
            "current_cpu_usage": self.cpu_usage_history[-1] if self.cpu_usage_history else 0,
            "current_memory_usage": self.memory_usage_history[-1] if self.memory_usage_history else 0
        }


class EngineHealthMonitor:
    """Monitors engine health and provides diagnostics."""

    def __init__(self, engine_id: str, metrics: EngineMetrics):
        """Initialize health monitor."""
        self.engine_id = engine_id
        self.metrics = metrics
        self.health_checks: List[Dict[str, Any]] = []
        self.last_health_check = datetime.now()

    def perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        check_time = datetime.now()

        health_status = {
            "timestamp": check_time.isoformat(),
            "engine_id": self.engine_id,
            "overall_health": "healthy",
            "checks": {},
            "recommendations": []
        }

        # Check operation success rate
        success_rate = self.metrics.success_count / self.metrics.operation_count if self.metrics.operation_count > 0 else 1.0
        health_status["checks"]["success_rate"] = {
            "status": "healthy" if success_rate >= 0.95 else "warning" if success_rate >= 0.85 else "critical",
            "value": success_rate,
            "threshold": 0.95
        }

        # Check response time
        if self.metrics.average_response_time > 5.0:  # 5 second threshold
            health_status["checks"]["response_time"] = {
                "status": "warning",
                "value": self.metrics.average_response_time,
                "threshold": 5.0
            }
            health_status["recommendations"].append("Consider optimizing response time")

        # Check memory usage
        if self.metrics.peak_memory_usage > 80:  # 80% threshold
            health_status["checks"]["memory_usage"] = {
                "status": "warning",
                "value": self.metrics.peak_memory_usage,
                "threshold": 80
            }
            health_status["recommendations"].append("Monitor memory usage")

        # Determine overall health
        critical_checks = [check for check in health_status["checks"].values() if check["status"] == "critical"]
        warning_checks = [check for check in health_status["checks"].values() if check["status"] == "warning"]

        if critical_checks:
            health_status["overall_health"] = "critical"
        elif warning_checks:
            health_status["overall_health"] = "warning"

        self.health_checks.append(health_status)
        self.last_health_check = check_time

        # Keep only last 50 health checks
        if len(self.health_checks) > 50:
            self.health_checks.pop(0)

        return health_status

    def get_health_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent health check history."""
        return self.health_checks[-limit:] if limit > 0 else self.health_checks

    def is_healthy(self) -> bool:
        """Check if engine is currently healthy."""
        if not self.health_checks:
            return True

        latest_check = self.health_checks[-1]
        return latest_check["overall_health"] == "healthy"
