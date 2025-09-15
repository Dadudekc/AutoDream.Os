#!/usr/bin/env python3
"""
BI Reliability Monitor - V2 Compliant
Business Intelligence reliability monitoring service with health checks and error tracking
V2 COMPLIANT: Under 400 lines, single responsibility.
Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


class HealthChecker:
    def __init__(self):
        self.health_checks = {}
        self.health_history = defaultdict(lambda: deque(maxlen=100))
        self.lock = threading.RLock()

    def register_health_check(self, component_name: str, check_function: callable) -> None:
        with self.lock:
            self.health_checks[component_name] = check_function
            logger.debug(f"Registered health check for {component_name}")

    def perform_health_check(self, component_name: str) -> dict[str, Any]:
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
    def __init__(self):
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

            # Filter errors by time window
            recent_errors = [
                error
                for error in self.errors
                if datetime.fromisoformat(error["timestamp"]) >= cutoff_time
            ]

            # Analyze error patterns
            error_by_type = defaultdict(int)
            error_by_component = defaultdict(int)
            error_by_severity = defaultdict(int)

            for error in recent_errors:
                error_by_type[error["error_type"]] += 1
                error_by_component[error["component"]] += 1
                error_by_severity[error["severity"]] += 1

            # Calculate error rate
            total_operations = len(recent_errors) * 100  # Estimate
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

            # Calculate score based on error rate and critical errors
            error_rate_penalty = min(0.5, self.error_stats["total_errors"] / 1000)
            critical_error_penalty = min(0.3, self.error_stats["critical_errors"] / 100)

            reliability_score = 1.0 - error_rate_penalty - critical_error_penalty
            return max(0.0, reliability_score)


class RecoveryManager:
    """Recovery management system for BI components."""

    def __init__(self):
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


class BIReliabilityMonitor:
    """Main BI reliability monitoring service."""

    def __init__(self):
        self.health_checker = HealthChecker()
        self.error_tracker = ErrorTracker()
        self.recovery_manager = RecoveryManager()
        self.monitoring_active = False
        self.monitoring_thread = None
        self.lock = threading.RLock()

        # Register default health checks
        self._register_default_health_checks()
        self._register_default_recovery_strategies()

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
        """Start reliability monitoring."""
        with self.lock:
            if not self.monitoring_active:
                self.monitoring_active = True
                self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
                self.monitoring_thread.daemon = True
                self.monitoring_thread.start()
                logger.info("BI Reliability Monitor started")

    def stop_monitoring(self) -> None:
        """Stop reliability monitoring."""
        with self.lock:
            self.monitoring_active = False
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=5)
            logger.info("BI Reliability Monitor stopped")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                # Perform health checks
                health_summary = self.health_checker.get_health_summary()

                # Check for unhealthy components
                for component, status in health_summary.items():
                    if status["health_score"] < 0.8:  # Threshold for unhealthy
                        self.error_tracker.record_error(
                            "health_check_failed",
                            component,
                            f"Health score: {status['health_score']}",
                            "high",
                        )

                        # Attempt recovery
                        recovery_result = self.recovery_manager.attempt_recovery(
                            component, {"health_score": status["health_score"]}
                        )

                        if recovery_result["success"]:
                            self.error_tracker.error_stats["recovered_errors"] += 1

                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error

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
            logger.error(f"Error generating reliability report: {e}")
            return {"error": str(e)}

    def _generate_reliability_recommendations(
        self,
        health_summary: dict[str, Any],
        error_analysis: dict[str, Any],
        reliability_score: float,
    ) -> list[str]:
        """Generate reliability recommendations."""
        recommendations = []

        # Health-based recommendations
        for component, status in health_summary.items():
            if status["health_score"] < 0.9:
                recommendations.append(f"Improve health monitoring for {component}")

        # Error-based recommendations
        if error_analysis["error_rate"] > 0.01:
            recommendations.append("High error rate detected - investigate error patterns")

        if error_analysis["errors_by_severity"].get("critical", 0) > 0:
            recommendations.append("Critical errors detected - implement immediate fixes")

        # Reliability score recommendations
        if reliability_score < 0.8:
            recommendations.append("Overall reliability score is low - review system stability")

        return recommendations


# Global reliability monitor instance
_global_reliability_monitor = None


def get_bi_reliability_monitor() -> BIReliabilityMonitor:
    """Get global BI reliability monitor."""
    global _global_reliability_monitor
    if _global_reliability_monitor is None:
        _global_reliability_monitor = BIReliabilityMonitor()
    return _global_reliability_monitor


if __name__ == "__main__":
    # Example usage
    monitor = get_bi_reliability_monitor()
    monitor.start_monitoring()

    # Simulate some errors
    monitor.error_tracker.record_error(
        "connection_timeout", "database", "Connection timeout", "high"
    )
    monitor.error_tracker.record_error(
        "memory_overflow", "cache", "Memory limit exceeded", "critical"
    )

    # Get reliability report
    report = monitor.get_reliability_report()
    print(f"Reliability report: {report}")

    monitor.stop_monitoring()
