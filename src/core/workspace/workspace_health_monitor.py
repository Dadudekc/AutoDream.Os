#!/usr/bin/env python3
"""
Workspace Health Monitor - Agent Cellphone V2

Monitors workspace health, performs health checks, and provides health reporting.
Ensures workspace system reliability and performance.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3A - Workspace System Consolidation
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import logging
import time
import threading
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

# Core infrastructure imports
from src.core.managers.performance_manager import PerformanceManager


class HealthStatus(Enum):
    """Workspace health status levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class HealthCheckType(Enum):
    """Types of health checks"""
    PERFORMANCE = "performance"
    RESOURCE_USAGE = "resource_usage"
    AGENT_HEALTH = "agent_health"
    SYSTEM_STABILITY = "system_stability"
    INTEGRATION = "integration"


@dataclass
class HealthCheckResult:
    """Result of a health check"""
    check_type: HealthCheckType
    status: HealthStatus
    score: float
    details: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    recommendations: List[str] = field(default_factory=list)


@dataclass
class WorkspaceHealth:
    """Overall workspace health information"""
    workspace_id: str
    overall_status: HealthStatus
    overall_score: float
    last_health_check: str
    health_checks: Dict[HealthCheckType, HealthCheckResult]
    health_trend: List[Tuple[str, float]]  # timestamp, score
    critical_issues: List[str]
    performance_alerts: List[str]


class WorkspaceHealthMonitor:
    """
    Workspace Health Monitor - TASK 3A

    Monitors workspace health for:
    - Performance metrics
    - Resource usage
    - Agent health
    - System stability
    - Integration status
    """

    def __init__(self, performance_manager: PerformanceManager):
        self.performance_manager = performance_manager
        self.logger = logging.getLogger(f"{__name__}.WorkspaceHealthMonitor")

        # Health tracking
        self.workspace_health: Dict[str, WorkspaceHealth] = {}
        self.health_monitoring_active = False
        self.health_monitor_thread = None
        self.health_monitor_lock = threading.Lock()

        # Health check configuration
        self.health_check_interval = 180  # 3 minutes
        self.last_health_check_run = None
        self.health_thresholds = {
            "excellent": 90.0,
            "good": 80.0,
            "fair": 70.0,
            "poor": 60.0,
            "critical": 50.0
        }

        # Performance alert thresholds
        self.performance_alert_thresholds = {
            "memory_usage": 85.0,
            "cpu_usage": 80.0,
            "agent_count": 20,
            "response_time": 1000,  # milliseconds
            "error_rate": 5.0  # percentage
        }

        self.logger.info("Workspace Health Monitor initialized for TASK 3A")

    def start_health_monitoring(self) -> bool:
        """Start workspace health monitoring"""
        try:
            with self.health_monitor_lock:
                if self.health_monitoring_active:
                    self.logger.warning("Health monitoring already active")
                    return False

                self.health_monitoring_active = True
                self.last_health_check_run = datetime.now()

                # Start health monitoring thread
                self.health_monitor_thread = threading.Thread(
                    target=self._health_monitoring_worker,
                    daemon=True
                )
                self.health_monitor_thread.start()

                # Setup health monitoring
                self._setup_health_monitoring()

                self.logger.info("Workspace health monitoring started successfully")
                return True

        except Exception as e:
            self.logger.error(f"Failed to start health monitoring: {e}")
            self.health_monitoring_active = False
            return False

    def stop_health_monitoring(self) -> bool:
        """Stop workspace health monitoring"""
        try:
            with self.health_monitor_lock:
                if not self.health_monitoring_active:
                    self.logger.warning("Health monitoring not active")
                    return False

                self.health_monitoring_active = False

                # Wait for health monitoring thread
                if self.health_monitor_thread and self.health_monitor_thread.is_alive():
                    self.health_monitor_thread.join(timeout=5.0)

                self.logger.info("Workspace health monitoring stopped")
                return True

        except Exception as e:
            self.logger.error(f"Failed to stop health monitoring: {e}")
            return False

    def _setup_health_monitoring(self):
        """Setup health monitoring with performance manager"""
        try:
            # Add health monitoring metrics
            self.performance_manager.add_metric("workspace_health_score", 0.0, "score", "workspace")
            self.performance_manager.add_metric("workspace_health_checks", 0, "count", "workspace")
            self.performance_manager.add_metric("workspace_critical_issues", 0, "count", "workspace")
            self.performance_manager.add_metric("workspace_performance_alerts", 0, "count", "workspace")

            self.logger.info("Health monitoring setup completed")

        except Exception as e:
            self.logger.error(f"Failed to setup health monitoring: {e}")

    def _health_monitoring_worker(self):
        """Main health monitoring worker thread"""
        try:
            self.logger.info("Health monitoring worker started")

            while self.health_monitoring_active:
                try:
                    # Check if it's time for health checks
                    if self._should_run_health_checks():
                        self._run_workspace_health_checks()
                        self.last_health_check_run = datetime.now()

                    # Sleep between checks
                    time.sleep(60)  # Check every minute

                except Exception as e:
                    self.logger.error(f"Error in health monitoring worker: {e}")
                    time.sleep(120)  # Longer sleep on error

            self.logger.info("Health monitoring worker stopped")

        except Exception as e:
            self.logger.error(f"Fatal error in health monitoring worker: {e}")

    def _should_run_health_checks(self) -> bool:
        """Check if health checks should run"""
        if not self.last_health_check_run:
            return True

        time_since_last = (datetime.now() - self.last_health_check_run).total_seconds()
        return time_since_last >= self.health_check_interval

    def _run_workspace_health_checks(self):
        """Run comprehensive workspace health checks"""
        try:
            self.logger.info("Running workspace health checks")

            for workspace_id in self.workspace_health.keys():
                self._perform_workspace_health_check(workspace_id)

            # Update health monitoring metrics
            self._update_health_monitoring_metrics()

            self.logger.info("Workspace health checks completed")

        except Exception as e:
            self.logger.error(f"Failed to run workspace health checks: {e}")

    def _perform_workspace_health_check(self, workspace_id: str):
        """Perform health check for a specific workspace"""
        try:
            if workspace_id not in self.workspace_health:
                return

            workspace_health = self.workspace_health[workspace_id]
            health_checks = {}

            # Performance health check
            performance_result = self._check_performance_health(workspace_id)
            health_checks[HealthCheckType.PERFORMANCE] = performance_result

            # Resource usage health check
            resource_result = self._check_resource_usage_health(workspace_id)
            health_checks[HealthCheckType.RESOURCE_USAGE] = resource_result

            # Agent health check
            agent_result = self._check_agent_health(workspace_id)
            health_checks[HealthCheckType.AGENT_HEALTH] = agent_result

            # System stability health check
            stability_result = self._check_system_stability_health(workspace_id)
            health_checks[HealthCheckType.SYSTEM_STABILITY] = stability_result

            # Integration health check
            integration_result = self._check_integration_health(workspace_id)
            health_checks[HealthCheckType.INTEGRATION] = integration_result

            # Calculate overall health score
            overall_score = self._calculate_overall_health_score(health_checks)
            overall_status = self._determine_health_status(overall_score)

            # Update workspace health
            workspace_health.health_checks = health_checks
            workspace_health.overall_status = overall_status
            workspace_health.overall_score = overall_score
            workspace_health.last_health_check = datetime.now().isoformat()

            # Add to health trend
            workspace_health.health_trend.append((datetime.now().isoformat(), overall_score))
            if len(workspace_health.health_trend) > 100:  # Keep last 100 entries
                workspace_health.health_trend = workspace_health.health_trend[-100:]

            # Check for critical issues and performance alerts
            self._check_critical_issues(workspace_id, health_checks)
            self._check_performance_alerts(workspace_id, health_checks)

            self.logger.info(f"Health check completed for {workspace_id}: {overall_status.value} ({overall_score:.1f})")

        except Exception as e:
            self.logger.error(f"Failed to perform health check for {workspace_id}: {e}")

    def _check_performance_health(self, workspace_id: str) -> HealthCheckResult:
        """Check performance health for a workspace"""
        try:
            # Get performance metrics from performance manager
            performance_metrics = self.performance_manager.get_metrics()
            
            # Calculate performance score based on available metrics
            score = 85.0  # Default score
            details = {}
            recommendations = []

            # Check for performance-related metrics
            workspace_metrics = [m for m in performance_metrics if f"workspace_{workspace_id}" in m.get("name", "")]
            
            if workspace_metrics:
                # Calculate score based on actual metrics
                total_score = 0
                metric_count = 0
                
                for metric in workspace_metrics:
                    if "health" in metric.get("name", ""):
                        value = metric.get("value", 0)
                        total_score += min(100.0, value)
                        metric_count += 1
                        details[metric.get("name", "")] = value

                if metric_count > 0:
                    score = total_score / metric_count

            # Determine status
            status = self._determine_health_status(score)

            # Generate recommendations
            if score < 80.0:
                recommendations.append("Review performance configuration")
                recommendations.append("Check resource allocation")
            if score < 70.0:
                recommendations.append("Investigate performance bottlenecks")
                recommendations.append("Consider resource scaling")

            return HealthCheckResult(
                check_type=HealthCheckType.PERFORMANCE,
                status=status,
                score=score,
                details=details,
                recommendations=recommendations
            )

        except Exception as e:
            self.logger.error(f"Failed to check performance health for {workspace_id}: {e}")
            return HealthCheckResult(
                check_type=HealthCheckType.PERFORMANCE,
                status=HealthStatus.CRITICAL,
                score=0.0,
                details={"error": str(e)},
                recommendations=["Check system connectivity", "Verify performance manager status"]
            )

    def _check_resource_usage_health(self, workspace_id: str) -> HealthCheckResult:
        """Check resource usage health for a workspace"""
        try:
            # Simulate resource usage check
            score = 90.0  # Default score
            details = {
                "memory_usage": 65.0,
                "cpu_usage": 45.0,
                "storage_usage": 30.0
            }
            recommendations = []

            # Check memory usage
            if details["memory_usage"] > self.performance_alert_thresholds["memory_usage"]:
                score -= 20.0
                recommendations.append("Reduce memory usage")
                recommendations.append("Check for memory leaks")

            # Check CPU usage
            if details["cpu_usage"] > self.performance_alert_thresholds["cpu_usage"]:
                score -= 15.0
                recommendations.append("Optimize CPU-intensive operations")
                recommendations.append("Consider load balancing")

            # Determine status
            status = self._determine_health_status(score)

            return HealthCheckResult(
                check_type=HealthCheckType.RESOURCE_USAGE,
                status=status,
                score=score,
                details=details,
                recommendations=recommendations
            )

        except Exception as e:
            self.logger.error(f"Failed to check resource usage health for {workspace_id}: {e}")
            return HealthCheckResult(
                check_type=HealthCheckType.RESOURCE_USAGE,
                status=HealthStatus.CRITICAL,
                score=0.0,
                details={"error": str(e)},
                recommendations=["Check resource monitoring", "Verify system resources"]
            )

    def _check_agent_health(self, workspace_id: str) -> HealthCheckResult:
        """Check agent health for a workspace"""
        try:
            # Simulate agent health check
            score = 95.0  # Default score
            details = {
                "total_agents": 8,
                "active_agents": 7,
                "healthy_agents": 6,
                "agent_health_ratio": 0.86
            }
            recommendations = []

            # Check agent count
            if details["total_agents"] > self.performance_alert_thresholds["agent_count"]:
                score -= 10.0
                recommendations.append("Consider agent consolidation")
                recommendations.append("Review agent allocation strategy")

            # Check agent health ratio
            if details["agent_health_ratio"] < 0.8:
                score -= 15.0
                recommendations.append("Investigate unhealthy agents")
                recommendations.append("Check agent configurations")

            # Determine status
            status = self._determine_health_status(score)

            return HealthCheckResult(
                check_type=HealthCheckType.AGENT_HEALTH,
                status=status,
                score=score,
                details=details,
                recommendations=recommendations
            )

        except Exception as e:
            self.logger.error(f"Failed to check agent health for {workspace_id}: {e}")
            return HealthCheckResult(
                check_type=HealthCheckType.AGENT_HEALTH,
                status=HealthStatus.CRITICAL,
                score=0.0,
                details={"error": str(e)},
                recommendations=["Check agent monitoring", "Verify agent status"]
            )

    def _check_system_stability_health(self, workspace_id: str) -> HealthCheckResult:
        """Check system stability health for a workspace"""
        try:
            # Simulate system stability check
            score = 92.0  # Default score
            details = {
                "uptime_hours": 48.5,
                "error_count": 2,
                "warning_count": 5,
                "restart_count": 0
            }
            recommendations = []

            # Check error count
            if details["error_count"] > 0:
                score -= 10.0
                recommendations.append("Review error logs")
                recommendations.append("Check system stability")

            # Check warning count
            if details["warning_count"] > 10:
                score -= 5.0
                recommendations.append("Address warning conditions")
                recommendations.append("Review system configuration")

            # Determine status
            status = self._determine_health_status(score)

            return HealthCheckResult(
                check_type=HealthCheckType.SYSTEM_STABILITY,
                status=status,
                score=score,
                details=details,
                recommendations=recommendations
            )

        except Exception as e:
            self.logger.error(f"Failed to check system stability health for {workspace_id}: {e}")
            return HealthCheckResult(
                check_type=HealthCheckType.SYSTEM_STABILITY,
                status=HealthStatus.CRITICAL,
                score=0.0,
                details={"error": str(e)},
                recommendations=["Check system logs", "Verify system status"]
            )

    def _check_integration_health(self, workspace_id: str) -> HealthCheckResult:
        """Check integration health for a workspace"""
        try:
            # Simulate integration health check
            score = 88.0  # Default score
            details = {
                "integrated_systems": 4,
                "integration_status": "active",
                "api_health": "healthy",
                "data_sync_status": "synchronized"
            }
            recommendations = []

            # Check integration status
            if details["integration_status"] != "active":
                score -= 20.0
                recommendations.append("Check integration status")
                recommendations.append("Verify system connectivity")

            # Check API health
            if details["api_health"] != "healthy":
                score -= 15.0
                recommendations.append("Investigate API issues")
                recommendations.append("Check API endpoints")

            # Determine status
            status = self._determine_health_status(score)

            return HealthCheckResult(
                check_type=HealthCheckType.INTEGRATION,
                status=status,
                score=score,
                details=details,
                recommendations=recommendations
            )

        except Exception as e:
            self.logger.error(f"Failed to check integration health for {workspace_id}: {e}")
            return HealthCheckResult(
                check_type=HealthCheckType.INTEGRATION,
                status=HealthStatus.CRITICAL,
                score=0.0,
                details={"error": str(e)},
                recommendations=["Check integration status", "Verify system connectivity"]
            )

    def _calculate_overall_health_score(self, health_checks: Dict[HealthCheckType, HealthCheckResult]) -> float:
        """Calculate overall health score from individual checks"""
        try:
            if not health_checks:
                return 0.0

            total_score = 0.0
            check_count = len(health_checks)

            for check_result in health_checks.values():
                total_score += check_result.score

            return total_score / check_count

        except Exception as e:
            self.logger.error(f"Failed to calculate overall health score: {e}")
            return 0.0

    def _determine_health_status(self, score: float) -> HealthStatus:
        """Determine health status based on score"""
        try:
            if score >= self.health_thresholds["excellent"]:
                return HealthStatus.EXCELLENT
            elif score >= self.health_thresholds["good"]:
                return HealthStatus.GOOD
            elif score >= self.health_thresholds["fair"]:
                return HealthStatus.FAIR
            elif score >= self.health_thresholds["poor"]:
                return HealthStatus.POOR
            else:
                return HealthStatus.CRITICAL

        except Exception as e:
            self.logger.error(f"Failed to determine health status: {e}")
            return HealthStatus.CRITICAL

    def _check_critical_issues(self, workspace_id: str, health_checks: Dict[HealthCheckType, HealthCheckResult]):
        """Check for critical issues in health checks"""
        try:
            workspace_health = self.workspace_health[workspace_id]
            critical_issues = []

            for check_type, check_result in health_checks.items():
                if check_result.status == HealthStatus.CRITICAL:
                    critical_issues.append(f"{check_type.value}: {check_result.score:.1f}")

            workspace_health.critical_issues = critical_issues

        except Exception as e:
            self.logger.error(f"Failed to check critical issues for {workspace_id}: {e}")

    def _check_performance_alerts(self, workspace_id: str, health_checks: Dict[HealthCheckType, HealthCheckResult]):
        """Check for performance alerts in health checks"""
        try:
            workspace_health = self.workspace_health[workspace_id]
            performance_alerts = []

            for check_type, check_result in health_checks.items():
                if check_result.status in [HealthStatus.POOR, HealthStatus.CRITICAL]:
                    performance_alerts.append(f"{check_type.value}: {check_result.status.value}")

            workspace_health.performance_alerts = performance_alerts

        except Exception as e:
            self.logger.error(f"Failed to check performance alerts for {workspace_id}: {e}")

    def _update_health_monitoring_metrics(self):
        """Update health monitoring performance metrics"""
        try:
            if not self.workspace_health:
                return

            total_health_score = 0.0
            total_critical_issues = 0
            total_performance_alerts = 0

            for workspace_health in self.workspace_health.values():
                total_health_score += workspace_health.overall_score
                total_critical_issues += len(workspace_health.critical_issues)
                total_performance_alerts += len(workspace_health.performance_alerts)

            # Calculate averages
            workspace_count = len(self.workspace_health)
            if workspace_count > 0:
                avg_health_score = total_health_score / workspace_count
                self.performance_manager.add_metric("workspace_health_score", avg_health_score, "score", "workspace")

            self.performance_manager.add_metric("workspace_critical_issues", total_critical_issues, "count", "workspace")
            self.performance_manager.add_metric("workspace_performance_alerts", total_performance_alerts, "count", "workspace")

        except Exception as e:
            self.logger.error(f"Failed to update health monitoring metrics: {e}")

    def register_workspace(self, workspace_id: str):
        """Register a workspace for health monitoring"""
        try:
            if workspace_id not in self.workspace_health:
                workspace_health = WorkspaceHealth(
                    workspace_id=workspace_id,
                    overall_status=HealthStatus.GOOD,
                    overall_score=85.0,
                    last_health_check=datetime.now().isoformat(),
                    health_checks={},
                    health_trend=[],
                    critical_issues=[],
                    performance_alerts=[]
                )

                self.workspace_health[workspace_id] = workspace_health
                self.logger.info(f"Registered workspace {workspace_id} for health monitoring")

        except Exception as e:
            self.logger.error(f"Failed to register workspace {workspace_id}: {e}")

    def get_workspace_health(self, workspace_id: str) -> Optional[WorkspaceHealth]:
        """Get health information for a specific workspace"""
        try:
            return self.workspace_health.get(workspace_id)
        except Exception as e:
            self.logger.error(f"Failed to get workspace health for {workspace_id}: {e}")
            return None

    def get_overall_health_status(self) -> Dict[str, Any]:
        """Get overall health status for all workspaces"""
        try:
            if not self.workspace_health:
                return {"error": "No workspaces registered"}

            total_workspaces = len(self.workspace_health)
            healthy_workspaces = sum(1 for w in self.workspace_health.values() if w.overall_status in [HealthStatus.EXCELLENT, HealthStatus.GOOD])
            critical_workspaces = sum(1 for w in self.workspace_health.values() if w.overall_status == HealthStatus.CRITICAL)

            total_health_score = sum(w.overall_score for w in self.workspace_health.values())
            avg_health_score = total_health_score / total_workspaces if total_workspaces > 0 else 0.0

            return {
                "total_workspaces": total_workspaces,
                "healthy_workspaces": healthy_workspaces,
                "critical_workspaces": critical_workspaces,
                "average_health_score": avg_health_score,
                "health_distribution": {
                    status.value: sum(1 for w in self.workspace_health.values() if w.overall_status == status)
                    for status in HealthStatus
                },
                "last_health_check": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Failed to get overall health status: {e}")
            return {"error": str(e)}

    def set_health_check_interval(self, interval_seconds: int):
        """Set the health check interval"""
        try:
            self.health_check_interval = max(60, interval_seconds)  # Minimum 1 minute
            self.logger.info(f"Health check interval set to: {self.health_check_interval} seconds")
        except Exception as e:
            self.logger.error(f"Failed to set health check interval: {e}")

    def set_health_thresholds(self, thresholds: Dict[str, float]):
        """Set health thresholds"""
        try:
            for threshold_name, threshold_value in thresholds.items():
                if threshold_name in self.health_thresholds:
                    self.health_thresholds[threshold_name] = max(0.0, min(100.0, threshold_value))

            self.logger.info("Health thresholds updated")
        except Exception as e:
            self.logger.error(f"Failed to set health thresholds: {e}")

