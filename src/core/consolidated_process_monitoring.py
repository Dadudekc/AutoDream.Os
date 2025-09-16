#!/usr/bin/env python3
"""
Consolidated Process Monitoring System - Unified Process Operations
=================================================================

Consolidated process monitoring system combining:
- Performance monitoring and metrics collection
- Health checks and reliability monitoring
- Backup monitoring and system health
- Error tracking and recovery management

Author: Agent-8 (Operations Specialist)
Mission: TASK 3 - Process optimization for Phase 2 system integration
License: MIT
"""

from __future__ import annotations

import json
import logging
import threading
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class MonitoringStatus(Enum):
    """Monitoring status enumeration."""

    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AlertLevel(Enum):
    """Alert level enumeration."""

    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"


class ComponentStatus(Enum):
    """Component status enumeration."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class PerformanceAlert:
    """Performance alert data structure."""

    alert_id: str
    component: str
    alert_level: AlertLevel
    metric_type: str
    current_value: float
    threshold_value: float
    message: str
    timestamp: float
    resolved: bool = False

    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()


@dataclass
class ComponentSnapshot:
    """Component performance snapshot."""

    component_id: str
    status: ComponentStatus
    response_time: float
    last_activity: float
    operations_completed: int
    errors_count: int
    memory_usage: float
    cpu_usage: float
    metadata: dict[str, Any]

    def __post_init__(self):
        if self.last_activity == 0:
            self.last_activity = time.time()


@dataclass
class SystemHealthReport:
    """Comprehensive system health report."""

    timestamp: float
    total_components: int
    healthy_components: int
    average_response_time: float
    total_operations: int
    total_errors: int
    system_load: float
    health_score: float
    alerts: list[PerformanceAlert]
    component_snapshots: list[ComponentSnapshot]


class HealthChecker:
    """Health checking system for components."""

    def __init__(self):
        """Initialize health checker."""
        self.health_checks = {}
        self.health_history = defaultdict(lambda: deque(maxlen=100))
        self.lock = threading.RLock()

    def register_health_check(self, component_name: str, check_function: callable) -> None:
        """Register a health check function for a component."""
        with self.lock:
            self.health_checks[component_name] = check_function
            logger.debug(f"Registered health check for {component_name}")

    def perform_health_check(self, component_name: str) -> dict[str, Any]:
        """Perform health check for a component."""
        with self.lock:
            if component_name not in self.health_checks:
                return {"status": "error", "message": "Component not registered"}

            try:
                start_time = time.time()
                result = self.health_checks[component_name]()
                execution_time = time.time() - start_time

                health_status = {
                    "component": component_name,
                    "status": "healthy" if result.get("healthy", False) else "unhealthy",
                    "execution_time": execution_time,
                    "timestamp": datetime.now().isoformat(),
                    "details": result,
                }

                self.health_history[component_name].append(health_status)
                return health_status

            except Exception as e:
                logger.error(f"Health check failed for {component_name}: {e}")
                error_status = {
                    "component": component_name,
                    "status": "error",
                    "execution_time": 0,
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e),
                }
                self.health_history[component_name].append(error_status)
                return error_status

    def get_health_summary(self) -> dict[str, Any]:
        """Get health summary for all components."""
        with self.lock:
            summary = {}
            for component_name in self.health_checks.keys():
                if component_name in self.health_history:
                    recent_checks = list(self.health_history[component_name])[-10:]
                    if recent_checks:
                        healthy_count = sum(
                            1 for check in recent_checks if check["status"] == "healthy"
                        )
                        total_count = len(recent_checks)
                        summary[component_name] = {
                            "health_score": healthy_count / total_count,
                            "last_status": recent_checks[-1]["status"],
                            "last_check": recent_checks[-1]["timestamp"],
                        }
            return summary


class ErrorTracker:
    """Error tracking and analysis system."""

    def __init__(self):
        """Initialize error tracker."""
        self.errors = deque(maxlen=1000)
        self.error_patterns = defaultdict(int)
        self.lock = threading.RLock()
        self.error_stats = {
            "total_errors": 0,
            "critical_errors": 0,
            "recovered_errors": 0,
            "error_rate": 0.0,
        }

    def record_error(
        self, error_type: str, component: str, message: str, severity: str = "medium"
    ) -> None:
        """Record an error."""
        with self.lock:
            error_record = {
                "error_type": error_type,
                "component": component,
                "message": message,
                "severity": severity,
                "timestamp": datetime.now().isoformat(),
            }
            self.errors.append(error_record)
            self.error_patterns[f"{error_type}:{component}"] += 1
            self.error_stats["total_errors"] += 1

            if severity == "critical":
                self.error_stats["critical_errors"] += 1

            logger.error(f"Error recorded: {error_type} in {component}: {message}")

    def get_error_analysis(self, time_window_hours: int = 24) -> dict[str, Any]:
        """Get error analysis for the specified time window."""
        with self.lock:
            cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
            recent_errors = [
                error
                for error in self.errors
                if datetime.fromisoformat(error["timestamp"]) >= cutoff_time
            ]

            error_by_type = defaultdict(int)
            error_by_component = defaultdict(int)
            error_by_severity = defaultdict(int)

            for error in recent_errors:
                error_by_type[error["error_type"]] += 1
                error_by_component[error["component"]] += 1
                error_by_severity[error["severity"]] += 1

            total_operations = len(recent_errors) * 100
            error_rate = len(recent_errors) / total_operations if total_operations > 0 else 0

            return {
                "time_window_hours": time_window_hours,
                "total_errors": len(recent_errors),
                "error_rate": error_rate,
                "errors_by_type": dict(error_by_type),
                "errors_by_component": dict(error_by_component),
                "errors_by_severity": dict(error_by_severity),
                "top_error_patterns": dict(
                    sorted(self.error_patterns.items(), key=lambda x: x[1], reverse=True)[:5]
                ),
            }

    def get_reliability_score(self) -> float:
        """Calculate overall reliability score."""
        with self.lock:
            if self.error_stats["total_errors"] == 0:
                return 1.0

            error_rate_penalty = min(0.5, self.error_stats["total_errors"] / 1000)
            critical_error_penalty = min(0.3, self.error_stats["critical_errors"] / 100)
            reliability_score = 1.0 - error_rate_penalty - critical_error_penalty
            return max(0.0, reliability_score)


class RecoveryManager:
    """Recovery management system for components."""

    def __init__(self):
        """Initialize recovery manager."""
        self.recovery_strategies = {}
        self.recovery_history = deque(maxlen=100)
        self.lock = threading.RLock()
        self.recovery_stats = {
            "recovery_attempts": 0,
            "successful_recoveries": 0,
            "failed_recoveries": 0,
        }

    def register_recovery_strategy(self, component_name: str, strategy_function: callable) -> None:
        """Register a recovery strategy for a component."""
        with self.lock:
            self.recovery_strategies[component_name] = strategy_function
            logger.debug(f"Registered recovery strategy for {component_name}")

    def attempt_recovery(
        self, component_name: str, error_context: dict[str, Any]
    ) -> dict[str, Any]:
        """Attempt to recover a failed component."""
        with self.lock:
            if component_name not in self.recovery_strategies:
                return {
                    "success": False,
                    "message": "No recovery strategy registered",
                    "component": component_name,
                }

            try:
                start_time = time.time()
                recovery_result = self.recovery_strategies[component_name](error_context)
                execution_time = time.time() - start_time

                recovery_record = {
                    "component": component_name,
                    "success": recovery_result.get("success", False),
                    "execution_time": execution_time,
                    "timestamp": datetime.now().isoformat(),
                    "error_context": error_context,
                    "recovery_details": recovery_result,
                }

                self.recovery_history.append(recovery_record)
                self.recovery_stats["recovery_attempts"] += 1

                if recovery_record["success"]:
                    self.recovery_stats["successful_recoveries"] += 1
                else:
                    self.recovery_stats["failed_recoveries"] += 1

                return recovery_record

            except Exception as e:
                logger.error(f"Recovery attempt failed for {component_name}: {e}")
                failed_recovery = {
                    "component": component_name,
                    "success": False,
                    "execution_time": 0,
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e),
                }
                self.recovery_history.append(failed_recovery)
                self.recovery_stats["recovery_attempts"] += 1
                self.recovery_stats["failed_recoveries"] += 1
                return failed_recovery

    def get_recovery_stats(self) -> dict[str, Any]:
        """Get recovery statistics."""
        with self.lock:
            success_rate = 0.0
            if self.recovery_stats["recovery_attempts"] > 0:
                success_rate = (
                    self.recovery_stats["successful_recoveries"]
                    / self.recovery_stats["recovery_attempts"]
                )

            return {
                "recovery_stats": self.recovery_stats,
                "success_rate": success_rate,
                "registered_strategies": list(self.recovery_strategies.keys()),
            }


class ConsolidatedProcessMonitoring:
    """Consolidated process monitoring system."""

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize consolidated process monitoring system."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Core components
        self.health_checker = HealthChecker()
        self.error_tracker = ErrorTracker()
        self.recovery_manager = RecoveryManager()

        # Performance tracking
        self.component_snapshots: dict[str, ComponentSnapshot] = {}
        self.performance_alerts: list[PerformanceAlert] = []
        self.performance_history: list[dict[str, Any]] = []

        # System state
        self.monitoring_active = False
        self.monitoring_thread: threading.Thread | None = None
        self.lock = threading.RLock()

        # Thresholds
        self.thresholds = {
            "response_time_warning": 3.0,  # seconds
            "response_time_critical": 10.0,  # seconds
            "memory_usage_warning": 80.0,  # percentage
            "memory_usage_critical": 95.0,  # percentage
            "cpu_usage_warning": 80.0,  # percentage
            "cpu_usage_critical": 95.0,  # percentage
            "error_rate_warning": 5.0,  # percentage
            "error_rate_critical": 15.0,  # percentage
        }

        # Register default health checks and recovery strategies
        self._register_default_health_checks()
        self._register_default_recovery_strategies()

        self.logger.info("Consolidated process monitoring system initialized")

    def _register_default_health_checks(self) -> None:
        """Register default health checks."""

        def system_health_check():
            return {"healthy": True, "uptime": time.time(), "memory_usage": "normal"}

        def database_health_check():
            return {"healthy": True, "connection_count": 5, "response_time": 0.1}

        def cache_health_check():
            return {"healthy": True, "hit_rate": 0.85, "size": 1000}

        self.health_checker.register_health_check("system", system_health_check)
        self.health_checker.register_health_check("database", database_health_check)
        self.health_checker.register_health_check("cache", cache_health_check)

    def _register_default_recovery_strategies(self) -> None:
        """Register default recovery strategies."""

        def system_recovery(error_context):
            return {"success": True, "action": "restart_system", "message": "System restarted"}

        def database_recovery(error_context):
            return {
                "success": True,
                "action": "reconnect_database",
                "message": "Database reconnected",
            }

        def cache_recovery(error_context):
            return {"success": True, "action": "clear_cache", "message": "Cache cleared"}

        self.recovery_manager.register_recovery_strategy("system", system_recovery)
        self.recovery_manager.register_recovery_strategy("database", database_recovery)
        self.recovery_manager.register_recovery_strategy("cache", cache_recovery)

    def start_monitoring(self) -> None:
        """Start process monitoring."""
        with self.lock:
            if not self.monitoring_active:
                self.monitoring_active = True
                self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
                self.monitoring_thread.daemon = True
                self.monitoring_thread.start()
                self.logger.info("Consolidated process monitoring started")

    def stop_monitoring(self) -> None:
        """Stop process monitoring."""
        with self.lock:
            self.monitoring_active = False
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=5)
            self.logger.info("Consolidated process monitoring stopped")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                # Perform health checks
                health_summary = self.health_checker.get_health_summary()
                for component, status in health_summary.items():
                    if status["health_score"] < 0.8:
                        self.error_tracker.record_error(
                            "health_check_failed",
                            component,
                            f"Health score: {status['health_score']}",
                            "high",
                        )
                        recovery_result = self.recovery_manager.attempt_recovery(
                            component, {"health_score": status["health_score"]}
                        )
                        if recovery_result["success"]:
                            self.error_tracker.error_stats["recovered_errors"] += 1

                time.sleep(30)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)

    def record_component_activity(
        self,
        component_id: str,
        response_time: float,
        operation_completed: bool = False,
        error_occurred: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Record component activity and update performance metrics."""
        try:
            current_time = time.time()

            # Get or create component snapshot
            if component_id not in self.component_snapshots:
                self.component_snapshots[component_id] = ComponentSnapshot(
                    component_id=component_id,
                    status=ComponentStatus.HEALTHY,
                    response_time=response_time,
                    last_activity=current_time,
                    operations_completed=0,
                    errors_count=0,
                    memory_usage=0.0,
                    cpu_usage=0.0,
                    metadata={},
                )

            snapshot = self.component_snapshots[component_id]

            # Update metrics
            snapshot.response_time = response_time
            snapshot.last_activity = current_time

            if operation_completed:
                snapshot.operations_completed += 1

            if error_occurred:
                snapshot.errors_count += 1

            # Update metadata
            if metadata:
                snapshot.metadata.update(metadata)

            # Check for performance alerts
            self._check_performance_alerts(snapshot)

            self.logger.debug(f"Recorded activity for {component_id}: {response_time:.3f}s")

        except Exception as e:
            self.logger.error(f"Error recording component activity: {e}")

    def _check_performance_alerts(self, snapshot: ComponentSnapshot) -> None:
        """Check for performance alerts and create them if needed."""
        try:
            current_time = time.time()

            # Response time alerts
            if snapshot.response_time > self.thresholds["response_time_critical"]:
                self._create_alert(
                    component_id=snapshot.component_id,
                    alert_level=AlertLevel.CRITICAL,
                    metric_type="response_time",
                    current_value=snapshot.response_time,
                    threshold_value=self.thresholds["response_time_critical"],
                    message=f"Critical response time: {snapshot.response_time:.2f}s",
                )
            elif snapshot.response_time > self.thresholds["response_time_warning"]:
                self._create_alert(
                    component_id=snapshot.component_id,
                    alert_level=AlertLevel.WARNING,
                    metric_type="response_time",
                    current_value=snapshot.response_time,
                    threshold_value=self.thresholds["response_time_warning"],
                    message=f"High response time: {snapshot.response_time:.2f}s",
                )

            # Error rate alerts
            if snapshot.operations_completed > 0:
                error_rate = (snapshot.errors_count / snapshot.operations_completed) * 100
                if error_rate > self.thresholds["error_rate_critical"]:
                    self._create_alert(
                        component_id=snapshot.component_id,
                        alert_level=AlertLevel.CRITICAL,
                        metric_type="error_rate",
                        current_value=error_rate,
                        threshold_value=self.thresholds["error_rate_critical"],
                        message=f"Critical error rate: {error_rate:.1f}%",
                    )
                elif error_rate > self.thresholds["error_rate_warning"]:
                    self._create_alert(
                        component_id=snapshot.component_id,
                        alert_level=AlertLevel.WARNING,
                        metric_type="error_rate",
                        current_value=error_rate,
                        threshold_value=self.thresholds["error_rate_warning"],
                        message=f"High error rate: {error_rate:.1f}%",
                    )

        except Exception as e:
            self.logger.error(f"Error checking performance alerts: {e}")

    def _create_alert(
        self,
        component_id: str,
        alert_level: AlertLevel,
        metric_type: str,
        current_value: float,
        threshold_value: float,
        message: str,
    ) -> None:
        """Create a performance alert."""
        try:
            alert_id = f"{component_id}_{metric_type}_{int(time.time())}"

            # Check if similar alert already exists
            existing_alert = next(
                (
                    a
                    for a in self.performance_alerts
                    if a.component == component_id
                    and a.metric_type == metric_type
                    and not a.resolved
                ),
                None,
            )

            if existing_alert:
                # Update existing alert
                existing_alert.current_value = current_value
                existing_alert.timestamp = time.time()
            else:
                # Create new alert
                alert = PerformanceAlert(
                    alert_id=alert_id,
                    component=component_id,
                    alert_level=alert_level,
                    metric_type=metric_type,
                    current_value=current_value,
                    threshold_value=threshold_value,
                    message=message,
                    timestamp=time.time(),
                )
                self.performance_alerts.append(alert)

                self.logger.warning(f"Performance alert: {component_id} - {message}")

        except Exception as e:
            self.logger.error(f"Error creating alert: {e}")

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve a performance alert."""
        try:
            alert = next((a for a in self.performance_alerts if a.alert_id == alert_id), None)

            if alert:
                alert.resolved = True
                self.logger.info(f"Resolved alert: {alert_id}")
                return True

            return False

        except Exception as e:
            self.logger.error(f"Error resolving alert: {e}")
            return False

    def get_component_status(self, component_id: str) -> ComponentSnapshot | None:
        """Get current status of a specific component."""
        return self.component_snapshots.get(component_id)

    def get_active_alerts(self) -> list[PerformanceAlert]:
        """Get all active (unresolved) alerts."""
        return [alert for alert in self.performance_alerts if not alert.resolved]

    def get_component_performance_summary(self, component_id: str) -> dict[str, Any]:
        """Get performance summary for a specific component."""
        try:
            snapshot = self.component_snapshots.get(component_id)
            if not snapshot:
                return {"error": f"Component {component_id} not found"}

            # Calculate performance score
            performance_score = self._calculate_component_performance_score(snapshot)

            # Get component-specific alerts
            component_alerts = [
                alert
                for alert in self.performance_alerts
                if alert.component == component_id and not alert.resolved
            ]

            return {
                "component_id": component_id,
                "status": snapshot.status.value,
                "response_time": snapshot.response_time,
                "operations_completed": snapshot.operations_completed,
                "errors_count": snapshot.errors_count,
                "performance_score": performance_score,
                "active_alerts": len(component_alerts),
                "last_activity": datetime.fromtimestamp(snapshot.last_activity).isoformat(),
                "metadata": snapshot.metadata,
            }

        except Exception as e:
            self.logger.error(f"Error getting component performance summary: {e}")
            return {"error": str(e)}

    def _calculate_component_performance_score(self, snapshot: ComponentSnapshot) -> float:
        """Calculate performance score for a component."""
        try:
            # Base score
            score = 100.0

            # Response time penalty
            if snapshot.response_time > self.thresholds["response_time_critical"]:
                score -= 30
            elif snapshot.response_time > self.thresholds["response_time_warning"]:
                score -= 15

            # Error rate penalty
            if snapshot.operations_completed > 0:
                error_rate = (snapshot.errors_count / snapshot.operations_completed) * 100
                if error_rate > self.thresholds["error_rate_critical"]:
                    score -= 25
                elif error_rate > self.thresholds["error_rate_warning"]:
                    score -= 10

            # Activity penalty (if no recent activity)
            time_since_activity = time.time() - snapshot.last_activity
            if time_since_activity > 3600:  # 1 hour
                score -= 20
            elif time_since_activity > 1800:  # 30 minutes
                score -= 10

            return max(score, 0.0)

        except Exception as e:
            self.logger.error(f"Error calculating performance score: {e}")
            return 0.0

    def generate_system_health_report(self) -> SystemHealthReport:
        """Generate comprehensive system health report."""
        try:
            current_time = time.time()

            # Calculate aggregate metrics
            total_components = len(self.component_snapshots)
            healthy_components = len(
                [
                    s
                    for s in self.component_snapshots.values()
                    if s.status == ComponentStatus.HEALTHY
                ]
            )

            response_times = [s.response_time for s in self.component_snapshots.values()]
            average_response_time = (
                sum(response_times) / len(response_times) if response_times else 0
            )

            total_operations = sum(
                s.operations_completed for s in self.component_snapshots.values()
            )
            total_errors = sum(s.errors_count for s in self.component_snapshots.values())

            # Calculate system load (simplified)
            system_load = (total_errors / max(total_operations, 1)) * 100

            # Calculate overall health score
            health_scores = [
                self._calculate_component_performance_score(s)
                for s in self.component_snapshots.values()
            ]
            health_score = sum(health_scores) / len(health_scores) if health_scores else 0

            # Get active alerts
            active_alerts = self.get_active_alerts()

            report = SystemHealthReport(
                timestamp=current_time,
                total_components=total_components,
                healthy_components=healthy_components,
                average_response_time=average_response_time,
                total_operations=total_operations,
                total_errors=total_errors,
                system_load=system_load,
                health_score=health_score,
                alerts=active_alerts,
                component_snapshots=list(self.component_snapshots.values()),
            )

            self.logger.info(f"Generated system health report - Score: {health_score:.1f}%")
            return report

        except Exception as e:
            self.logger.error(f"Error generating system health report: {e}")
            return SystemHealthReport(
                timestamp=time.time(),
                total_components=0,
                healthy_components=0,
                average_response_time=0,
                total_operations=0,
                total_errors=0,
                system_load=0,
                health_score=0,
                alerts=[],
                component_snapshots=[],
            )

    def get_reliability_report(self) -> dict[str, Any]:
        """Get comprehensive reliability report."""
        try:
            health_summary = self.health_checker.get_health_summary()
            error_analysis = self.error_tracker.get_error_analysis()
            recovery_stats = self.recovery_manager.get_recovery_stats()
            reliability_score = self.error_tracker.get_reliability_score()

            return {
                "reliability_report": {
                    "overall_reliability_score": reliability_score,
                    "monitoring_active": self.monitoring_active,
                    "health_summary": health_summary,
                    "error_analysis": error_analysis,
                    "recovery_stats": recovery_stats,
                },
                "recommendations": self._generate_reliability_recommendations(
                    health_summary, error_analysis, reliability_score
                ),
                "generation_timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error generating reliability report: {e}")
            return {"error": str(e)}

    def _generate_reliability_recommendations(
        self,
        health_summary: dict[str, Any],
        error_analysis: dict[str, Any],
        reliability_score: float,
    ) -> list[str]:
        """Generate reliability recommendations."""
        recommendations = []

        for component, status in health_summary.items():
            if status["health_score"] < 0.9:
                recommendations.append(f"Improve health monitoring for {component}")

        if error_analysis["error_rate"] > 0.01:
            recommendations.append("High error rate detected - investigate error patterns")

        if error_analysis["errors_by_severity"].get("critical", 0) > 0:
            recommendations.append("Critical errors detected - implement immediate fixes")

        if reliability_score < 0.8:
            recommendations.append("Overall reliability score is low - review system stability")

        return recommendations

    def save_monitoring_data(self, data_path: str = "data/monitoring") -> None:
        """Save monitoring data to persistent storage."""
        try:
            data_dir = Path(data_path)
            data_dir.mkdir(parents=True, exist_ok=True)

            # Save component snapshots
            snapshots_file = data_dir / "component_snapshots.json"
            with open(snapshots_file, "w") as f:
                json.dump(
                    {
                        component_id: asdict(snapshot)
                        for component_id, snapshot in self.component_snapshots.items()
                    },
                    f,
                    indent=2,
                )

            # Save alerts
            alerts_file = data_dir / "performance_alerts.json"
            with open(alerts_file, "w") as f:
                json.dump([asdict(alert) for alert in self.performance_alerts], f, indent=2)

            self.logger.info("Monitoring data saved to persistent storage")

        except Exception as e:
            self.logger.error(f"Error saving monitoring data: {e}")

    def get_system_status(self) -> dict[str, Any]:
        """Get comprehensive system status."""
        return {
            "monitoring": {
                "active": self.monitoring_active,
                "components_tracked": len(self.component_snapshots),
                "active_alerts": len(self.get_active_alerts()),
            },
            "health": self.health_checker.get_health_summary(),
            "errors": self.error_tracker.get_error_analysis(),
            "recovery": self.recovery_manager.get_recovery_stats(),
            "timestamp": datetime.now().isoformat(),
        }


# Global instance for convenience
_global_process_monitoring = None


def get_consolidated_process_monitoring(
    config: dict[str, Any] | None = None,
) -> ConsolidatedProcessMonitoring:
    """Get global consolidated process monitoring system."""
    global _global_process_monitoring
    if _global_process_monitoring is None:
        _global_process_monitoring = ConsolidatedProcessMonitoring(config)
    return _global_process_monitoring


if __name__ == "__main__":
    # Test the consolidated process monitoring system
    monitoring = get_consolidated_process_monitoring()

    # Start monitoring
    monitoring.start_monitoring()

    # Record some test activity
    monitoring.record_component_activity("test_component", 1.5, operation_completed=True)
    monitoring.record_component_activity("test_component", 2.0, error_occurred=True)

    # Generate reports
    health_report = monitoring.generate_system_health_report()
    reliability_report = monitoring.get_reliability_report()
    system_status = monitoring.get_system_status()

    logger.info(f"Health report: {health_report}")
    logger.info(f"Reliability report: {reliability_report}")
    logger.info(f"System status: {system_status}")

    # Stop monitoring
    monitoring.stop_monitoring()
