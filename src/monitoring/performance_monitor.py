#!/usr/bin/env python3
"""
Real-Time Performance Monitoring System
=======================================

Comprehensive performance monitoring for all modular components.
V2 Compliance: ≤400 lines, focused monitoring functionality.
"""

import asyncio
import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import psutil

logger = logging.getLogger(__name__)


@dataclass
class PerformanceSnapshot:
    """Performance snapshot at a point in time."""

    timestamp: datetime
    cpu_percent: float
    memory_mb: float
    disk_usage_percent: float
    active_connections: int
    workflow_executions: int
    discord_messages: int
    command_executions: int
    error_count: int
    response_time_ms: float

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass
class ComponentMetrics:
    """Metrics for a specific component."""

    component_name: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    max_response_time: float
    min_response_time: float
    last_activity: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data["last_activity"] = self.last_activity.isoformat()
        data["success_rate"] = (
            self.successful_requests / self.total_requests if self.total_requests > 0 else 0
        )
        return data


class RealTimePerformanceMonitor:
    """Real-time performance monitoring system."""

    def __init__(self, project_root: Path, monitoring_interval: int = 30):
        self.project_root = project_root
        self.monitoring_interval = monitoring_interval
        self.is_monitoring = False
        self.monitoring_task: asyncio.Task | None = None

        # Performance data storage
        self.performance_history: list[PerformanceSnapshot] = []
        self.component_metrics: dict[str, ComponentMetrics] = {}
        self.alert_thresholds = {
            "cpu_percent": 80.0,
            "memory_mb": 1000.0,
            "response_time_ms": 5000.0,
            "error_rate": 0.1,
        }

        # Monitoring state
        self.start_time = datetime.now()
        self.total_requests = 0
        self.total_errors = 0

        # Component references (simplified - no weakref)
        self.workflow_optimizer = None
        self.discord_optimizer = None

    def register_component(self, component_name: str, optimizer_ref):
        """Register a component for monitoring."""
        self.component_metrics[component_name] = ComponentMetrics(
            component_name=component_name,
            total_requests=0,
            successful_requests=0,
            failed_requests=0,
            average_response_time=0.0,
            max_response_time=0.0,
            min_response_time=float("inf"),
            last_activity=datetime.now(),
        )

        # Store direct reference (simplified - no weakref)
        if component_name == "workflow":
            self.workflow_optimizer = optimizer_ref
        elif component_name == "discord":
            self.discord_optimizer = optimizer_ref

        logger.info(f"Registered component for monitoring: {component_name}")

    def record_request(self, component_name: str, success: bool, response_time: float):
        """Record a request for a component."""
        if component_name not in self.component_metrics:
            self.register_component(component_name, None)

        metrics = self.component_metrics[component_name]
        metrics.total_requests += 1
        metrics.last_activity = datetime.now()

        if success:
            metrics.successful_requests += 1
        else:
            metrics.failed_requests += 1
            self.total_errors += 1

        # Update response time metrics
        metrics.average_response_time = (
            metrics.average_response_time * (metrics.total_requests - 1) + response_time
        ) / metrics.total_requests
        metrics.max_response_time = max(metrics.max_response_time, response_time)
        metrics.min_response_time = min(metrics.min_response_time, response_time)

        self.total_requests += 1

    async def collect_system_metrics(self) -> PerformanceSnapshot:
        """Collect current system performance metrics."""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Component-specific metrics
            workflow_executions = 0
            discord_messages = 0
            command_executions = 0

            # Get metrics from registered components
            if self.workflow_optimizer and self.workflow_optimizer():
                workflow_stats = self.workflow_optimizer().get_optimization_stats()
                workflow_executions = workflow_stats.get("performance", {}).get(
                    "total_executions", 0
                )

            if self.discord_optimizer and self.discord_optimizer():
                discord_stats = self.discord_optimizer().get_optimization_stats()
                discord_messages = discord_stats.get("performance", {}).get("messages_received", 0)
                command_executions = discord_stats.get("performance", {}).get(
                    "commands_executed", 0
                )

            # Calculate response time
            response_time_ms = 0.0
            if self.component_metrics:
                avg_response_times = [
                    metrics.average_response_time
                    for metrics in self.component_metrics.values()
                    if metrics.total_requests > 0
                ]
                response_time_ms = (
                    sum(avg_response_times) / len(avg_response_times) if avg_response_times else 0.0
                )

            return PerformanceSnapshot(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_mb=memory.used / 1024 / 1024,
                disk_usage_percent=disk.percent,
                active_connections=len(psutil.net_connections()),
                workflow_executions=workflow_executions,
                discord_messages=discord_messages,
                command_executions=command_executions,
                error_count=self.total_errors,
                response_time_ms=response_time_ms,
            )

        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return PerformanceSnapshot(
                timestamp=datetime.now(),
                cpu_percent=0.0,
                memory_mb=0.0,
                disk_usage_percent=0.0,
                active_connections=0,
                workflow_executions=0,
                discord_messages=0,
                command_executions=0,
                error_count=0,
                response_time_ms=0.0,
            )

    async def check_alerts(self, snapshot: PerformanceSnapshot):
        """Check for performance alerts."""
        alerts = []

        if snapshot.cpu_percent > self.alert_thresholds["cpu_percent"]:
            alerts.append(f"High CPU usage: {snapshot.cpu_percent:.1f}%")

        if snapshot.memory_mb > self.alert_thresholds["memory_mb"]:
            alerts.append(f"High memory usage: {snapshot.memory_mb:.1f}MB")

        if snapshot.response_time_ms > self.alert_thresholds["response_time_ms"]:
            alerts.append(f"High response time: {snapshot.response_time_ms:.1f}ms")

        # Check error rate
        if self.total_requests > 0:
            error_rate = self.total_errors / self.total_requests
            if error_rate > self.alert_thresholds["error_rate"]:
                alerts.append(f"High error rate: {error_rate:.1%}")

        if alerts:
            logger.warning(f"Performance alerts: {'; '.join(alerts)}")
            await self._handle_alerts(alerts)

    async def _handle_alerts(self, alerts: list[str]):
        """Handle performance alerts."""
        # Log alerts
        for alert in alerts:
            logger.warning(f"PERFORMANCE ALERT: {alert}")

        # Save alert to file
        alert_data = {
            "timestamp": datetime.now().isoformat(),
            "alerts": alerts,
            "system_state": await self.get_current_status(),
        }

        alert_file = self.project_root / "logs" / "performance_alerts.json"
        alert_file.parent.mkdir(exist_ok=True)

        # Append to alerts file
        if alert_file.exists():
            with open(alert_file) as f:
                existing_alerts = json.load(f)
        else:
            existing_alerts = []

        existing_alerts.append(alert_data)

        with open(alert_file, "w") as f:
            json.dump(existing_alerts, f, indent=2)

    async def monitoring_loop(self):
        """Main monitoring loop."""
        logger.info("Starting real-time performance monitoring...")

        while self.is_monitoring:
            try:
                # Collect metrics
                snapshot = await self.collect_system_metrics()

                # Store snapshot
                self.performance_history.append(snapshot)

                # Keep only last 1000 snapshots
                if len(self.performance_history) > 1000:
                    self.performance_history = self.performance_history[-1000:]

                # Check for alerts
                await self.check_alerts(snapshot)

                # Log current status
                logger.debug(
                    f"Performance snapshot: CPU {snapshot.cpu_percent:.1f}%, "
                    f"Memory {snapshot.memory_mb:.1f}MB, "
                    f"Response time {snapshot.response_time_ms:.1f}ms"
                )

                # Wait for next interval
                await asyncio.sleep(self.monitoring_interval)

            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                await asyncio.sleep(self.monitoring_interval)

    async def start_monitoring(self):
        """Start real-time monitoring."""
        if self.is_monitoring:
            logger.warning("Monitoring already started")
            return

        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self.monitoring_loop())
        logger.info("Real-time performance monitoring started")

    async def stop_monitoring(self):
        """Stop real-time monitoring."""
        if not self.is_monitoring:
            logger.warning("Monitoring not started")
            return

        self.is_monitoring = False

        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass

        logger.info("Real-time performance monitoring stopped")

    async def get_current_status(self) -> dict[str, Any]:
        """Get current system status."""
        snapshot = await self.collect_system_metrics()

        return {
            "timestamp": snapshot.timestamp.isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "system_metrics": snapshot.to_dict(),
            "component_metrics": {
                name: metrics.to_dict() for name, metrics in self.component_metrics.items()
            },
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "error_rate": self.total_errors / self.total_requests if self.total_requests > 0 else 0,
            "monitoring_active": self.is_monitoring,
        }

    def get_performance_summary(self) -> dict[str, Any]:
        """Get performance summary."""
        if not self.performance_history:
            return {"message": "No performance data available"}

        recent_snapshots = self.performance_history[-10:]  # Last 10 snapshots

        return {
            "monitoring_duration": (datetime.now() - self.start_time).total_seconds(),
            "total_snapshots": len(self.performance_history),
            "recent_averages": {
                "cpu_percent": sum(s.cpu_percent for s in recent_snapshots)
                / len(recent_snapshots),
                "memory_mb": sum(s.memory_mb for s in recent_snapshots) / len(recent_snapshots),
                "response_time_ms": sum(s.response_time_ms for s in recent_snapshots)
                / len(recent_snapshots),
            },
            "component_summary": {
                name: {
                    "total_requests": metrics.total_requests,
                    "success_rate": metrics.successful_requests / metrics.total_requests
                    if metrics.total_requests > 0
                    else 0,
                    "avg_response_time": metrics.average_response_time,
                }
                for name, metrics in self.component_metrics.items()
            },
        }

    def save_performance_report(self) -> bool:
        """Save comprehensive performance report."""
        try:
            report = {
                "report_time": datetime.now().isoformat(),
                "monitoring_summary": self.get_performance_summary(),
                "component_metrics": {
                    name: metrics.to_dict() for name, metrics in self.component_metrics.items()
                },
                "recent_snapshots": [
                    snapshot.to_dict()
                    for snapshot in self.performance_history[-50:]
                ],
            }

            report_path = self.project_root / "logs" / "performance_report.json"
            report_path.parent.mkdir(exist_ok=True)

            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)

            logger.info(f"Performance report saved: {report_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save performance report: {e}")
            return False
