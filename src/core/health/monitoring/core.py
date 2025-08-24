"""
Agent Health Core Monitoring Module

Single Responsibility: Core health monitoring orchestration and coordination.
Follows V2 coding standards: Clean OOP design, SRP compliance, TDD approach.
"""

import asyncio
import json
import logging
import time
import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Callable, Any
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Agent health status levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


class HealthMetricType(Enum):
    """Types of health metrics"""
    RESPONSE_TIME = "response_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    ERROR_RATE = "error_rate"
    TASK_COMPLETION_RATE = "task_completion_rate"
    HEARTBEAT_FREQUENCY = "heartbeat_frequency"
    CONTRACT_SUCCESS_RATE = "contract_success_rate"
    COMMUNICATION_LATENCY = "communication_latency"


@dataclass
class HealthMetric:
    """Individual health metric data"""
    agent_id: str
    metric_type: HealthMetricType
    value: float
    unit: str
    timestamp: datetime
    threshold: Optional[float] = None
    status: HealthStatus = HealthStatus.GOOD


@dataclass
class HealthSnapshot:
    """Complete health snapshot for an agent"""
    agent_id: str
    timestamp: datetime
    overall_status: HealthStatus
    health_score: float  # 0-100
    metrics: Dict[HealthMetricType, HealthMetric] = field(default_factory=dict)
    alerts: List["HealthAlert"] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class HealthAlert:
    """Health alert information"""
    alert_id: str
    agent_id: str
    severity: "AlertSeverity"
    message: str
    metric_type: HealthMetricType
    current_value: float
    threshold: float
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False


@dataclass
class HealthThreshold:
    """Health threshold configuration"""
    metric_type: HealthMetricType
    warning_threshold: float
    critical_threshold: float
    unit: str
    description: str


class AgentHealthCoreMonitor:
    """
    Core agent health monitoring orchestration
    
    Single Responsibility: Coordinate health monitoring activities and manage
    the main monitoring loop. Delegates specific responsibilities to other modules.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the core health monitor"""
        self.config = config or {}
        self.monitoring_active = False
        self.health_data: Dict[str, HealthSnapshot] = {}
        self.alerts: Dict[str, HealthAlert] = {}
        self.thresholds: Dict[HealthMetricType, HealthThreshold] = {}
        self.health_callbacks: Set[Callable] = set()
        self.monitor_thread: Optional[threading.Thread] = None
        self.executor = ThreadPoolExecutor(max_workers=4)

        # Initialize default thresholds
        self._initialize_default_thresholds()

        # Health monitoring intervals
        self.metrics_interval = self.config.get("metrics_interval", 30)  # seconds
        self.health_check_interval = self.config.get("health_check_interval", 60)  # seconds
        self.alert_check_interval = self.config.get("alert_check_interval", 15)  # seconds

        logger.info("AgentHealthCoreMonitor initialized with default thresholds")

    def _initialize_default_thresholds(self):
        """Initialize default health thresholds"""
        default_thresholds = [
            HealthThreshold(
                HealthMetricType.RESPONSE_TIME,
                warning_threshold=1000.0,  # 1 second
                critical_threshold=5000.0,  # 5 seconds
                unit="ms",
                description="Response time threshold",
            ),
            HealthThreshold(
                HealthMetricType.MEMORY_USAGE,
                warning_threshold=80.0,  # 80%
                critical_threshold=95.0,  # 95%
                unit="%",
                description="Memory usage threshold",
            ),
            HealthThreshold(
                HealthMetricType.CPU_USAGE,
                warning_threshold=85.0,  # 85%
                critical_threshold=95.0,  # 95%
                unit="%",
                description="CPU usage threshold",
            ),
            HealthThreshold(
                HealthMetricType.ERROR_RATE,
                warning_threshold=5.0,  # 5%
                critical_threshold=15.0,  # 15%
                unit="%",
                description="Error rate threshold",
            ),
            HealthThreshold(
                HealthMetricType.TASK_COMPLETION_RATE,
                warning_threshold=90.0,  # 90%
                critical_threshold=75.0,  # 75%
                unit="%",
                description="Task completion rate threshold",
            ),
            HealthThreshold(
                HealthMetricType.HEARTBEAT_FREQUENCY,
                warning_threshold=120.0,  # 2 minutes
                critical_threshold=300.0,  # 5 minutes
                unit="seconds",
                description="Heartbeat frequency threshold",
            ),
            HealthThreshold(
                HealthMetricType.CONTRACT_SUCCESS_RATE,
                warning_threshold=85.0,  # 85%
                critical_threshold=70.0,  # 70%
                unit="%",
                description="Contract success rate threshold",
            ),
            HealthThreshold(
                HealthMetricType.COMMUNICATION_LATENCY,
                warning_threshold=500.0,  # 500ms
                critical_threshold=2000.0,  # 2 seconds
                unit="ms",
                description="Communication latency threshold",
            ),
        ]

        for threshold in default_thresholds:
            self.thresholds[threshold.metric_type] = threshold

    def start(self):
        """Start health monitoring"""
        if self.monitoring_active:
            logger.warning("Health monitoring already active")
            return

        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Agent health monitoring started")

    def stop(self):
        """Stop health monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.executor.shutdown(wait=True)
        logger.info("Agent health monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect health metrics
                self._collect_health_metrics()

                # Perform health checks
                self._perform_health_checks()

                # Check for alerts
                self._check_alerts()

                # Update health scores
                self._update_health_scores()

                # Notify subscribers
                self._notify_health_updates()

                time.sleep(self.health_check_interval)

            except Exception as e:
                logger.error(f"Error in health monitoring loop: {e}")
                time.sleep(10)  # Wait before retrying

    def _collect_health_metrics(self):
        """Collect health metrics from all agents"""
        # This would integrate with the actual agent management system
        # For now, we'll simulate metric collection
        pass

    def _perform_health_checks(self):
        """Perform comprehensive health checks"""
        for agent_id, snapshot in self.health_data.items():
            try:
                # Check each metric against thresholds
                for metric_type, metric in snapshot.metrics.items():
                    if metric_type in self.thresholds:
                        threshold = self.thresholds[metric_type]
                        self._evaluate_metric(agent_id, metric, threshold)

                # Update overall health status
                self._update_agent_health_status(agent_id)

            except Exception as e:
                logger.error(f"Error checking health for agent {agent_id}: {e}")

    def _evaluate_metric(
        self, agent_id: str, metric: HealthMetric, threshold: HealthThreshold
    ):
        """Evaluate a metric against its threshold"""
        current_value = metric.value

        # Check for critical threshold
        if current_value >= threshold.critical_threshold:
            self._create_alert(agent_id, "CRITICAL", metric, threshold)
        # Check for warning threshold
        elif current_value >= threshold.warning_threshold:
            self._create_alert(agent_id, "WARNING", metric, threshold)

    def _create_alert(
        self,
        agent_id: str,
        severity: str,
        metric: HealthMetric,
        threshold: HealthThreshold,
    ):
        """Create a health alert"""
        alert_id = (
            f"health_alert_{agent_id}_{metric.metric_type.value}_{int(time.time())}"
        )

        alert = HealthAlert(
            alert_id=alert_id,
            agent_id=agent_id,
            severity=severity,
            message=f"{metric.metric_type.value} threshold exceeded: {metric.value}{metric.unit} >= {threshold.critical_threshold if severity == 'CRITICAL' else threshold.warning_threshold}{threshold.unit}",
            metric_type=metric.metric_type,
            current_value=metric.value,
            threshold=threshold.critical_threshold
            if severity == "CRITICAL"
            else threshold.warning_threshold,
            timestamp=datetime.now(),
        )

        self.alerts[alert_id] = alert
        logger.warning(f"Health alert created: {alert.message}")

    def _update_agent_health_status(self, agent_id: str):
        """Update overall health status for an agent"""
        if agent_id not in self.health_data:
            return

        snapshot = self.health_data[agent_id]
        active_alerts = [alert for alert in snapshot.alerts if not alert.resolved]

        # Determine overall status based on alerts
        if any(alert.severity == "CRITICAL" for alert in active_alerts):
            snapshot.overall_status = HealthStatus.CRITICAL
        elif any(alert.severity == "WARNING" for alert in active_alerts):
            snapshot.overall_status = HealthStatus.WARNING
        elif snapshot.health_score >= 90:
            snapshot.overall_status = HealthStatus.EXCELLENT
        elif snapshot.health_score >= 75:
            snapshot.overall_status = HealthStatus.GOOD
        else:
            snapshot.overall_status = HealthStatus.WARNING

    def _update_health_scores(self):
        """Update health scores for all agents"""
        for agent_id, snapshot in self.health_data.items():
            try:
                # Calculate health score based on metrics and alerts
                score = self._calculate_health_score(snapshot)
                snapshot.health_score = score

                # Generate recommendations
                recommendations = self._generate_health_recommendations(snapshot)
                snapshot.recommendations = recommendations

            except Exception as e:
                logger.error(f"Error updating health score for agent {agent_id}: {e}")

    def _calculate_health_score(self, snapshot: HealthSnapshot) -> float:
        """Calculate health score (0-100) for an agent"""
        if not snapshot.metrics:
            return 100.0  # No metrics available

        total_score = 0
        metric_count = 0

        for metric_type, metric in snapshot.metrics.items():
            if metric_type in self.thresholds:
                threshold = self.thresholds[metric_type]

                # Calculate metric score based on threshold proximity
                if metric.value <= threshold.warning_threshold:
                    score = 100.0  # Excellent
                elif metric.value <= threshold.critical_threshold:
                    # Linear interpolation between warning and critical
                    ratio = (metric.value - threshold.warning_threshold) / (
                        threshold.critical_threshold - threshold.warning_threshold
                    )
                    score = 100.0 - (ratio * 25.0)  # 100 to 75
                else:
                    score = max(
                        0.0,
                        75.0
                        - (
                            (metric.value - threshold.critical_threshold)
                            / threshold.critical_threshold
                        )
                        * 75.0,
                    )

                total_score += score
                metric_count += 1

        # Penalize for active alerts
        active_alerts = [alert for alert in snapshot.alerts if not alert.resolved]
        alert_penalty = 0

        for alert in active_alerts:
            if alert.severity == "CRITICAL":
                alert_penalty += 20
            elif alert.severity == "WARNING":
                alert_penalty += 10

        final_score = (total_score / metric_count) - alert_penalty
        return max(0.0, min(100.0, final_score))

    def _generate_health_recommendations(self, snapshot: HealthSnapshot) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []

        # Check for specific issues and provide recommendations
        for metric_type, metric in snapshot.metrics.items():
            if metric_type == HealthMetricType.RESPONSE_TIME and metric.value > 1000:
                recommendations.append(
                    "Consider optimizing response time by reviewing processing logic"
                )

            elif metric_type == HealthMetricType.MEMORY_USAGE and metric.value > 80:
                recommendations.append(
                    "High memory usage detected - consider memory optimization or cleanup"
                )

            elif metric_type == HealthMetricType.CPU_USAGE and metric.value > 85:
                recommendations.append(
                    "High CPU usage detected - consider load balancing or optimization"
                )

            elif metric_type == HealthMetricType.ERROR_RATE and metric.value > 5:
                recommendations.append(
                    "High error rate detected - review error handling and logging"
                )

        # Add general recommendations based on overall status
        if snapshot.overall_status == HealthStatus.CRITICAL:
            recommendations.append("CRITICAL: Immediate intervention required")
        elif snapshot.overall_status == HealthStatus.WARNING:
            recommendations.append(
                "WARNING: Monitor closely and address issues promptly"
            )

        return recommendations

    def _check_alerts(self):
        """Check and manage health alerts"""
        current_time = datetime.now()

        # Check for expired alerts
        expired_alerts = []
        for alert_id, alert in self.alerts.items():
            # Mark alerts as resolved if conditions improve
            if self._is_alert_resolved(alert):
                alert.resolved = True
                logger.info(f"Alert {alert_id} automatically resolved")

            # Remove very old alerts
            if (current_time - alert.timestamp).days > 7:
                expired_alerts.append(alert_id)

        # Remove expired alerts
        for alert_id in expired_alerts:
            del self.alerts[alert_id]

    def _is_alert_resolved(self, alert: HealthAlert) -> bool:
        """Check if an alert should be automatically resolved"""
        if alert.resolved:
            return True

        # Check if the current metric value is below threshold
        if alert.agent_id in self.health_data:
            snapshot = self.health_data[alert.agent_id]
            if alert.metric_type in snapshot.metrics:
                current_value = snapshot.metrics[alert.metric_type].value
                return current_value < alert.threshold

        return False

    def _notify_health_updates(self):
        """Notify subscribers of health updates"""
        for callback in self.health_callbacks:
            try:
                callback(self.health_data, self.alerts)
            except Exception as e:
                logger.error(f"Error in health update callback: {e}")

    def record_health_metric(
        self,
        agent_id: str,
        metric_type: HealthMetricType,
        value: float,
        unit: str,
        threshold: Optional[float] = None,
    ):
        """Record a health metric for an agent"""
        try:
            # Create or update health snapshot
            if agent_id not in self.health_data:
                self.health_data[agent_id] = HealthSnapshot(
                    agent_id=agent_id,
                    timestamp=datetime.now(),
                    overall_status=HealthStatus.GOOD,
                    health_score=100.0,
                )

            snapshot = self.health_data[agent_id]

            # Create metric
            metric = HealthMetric(
                agent_id=agent_id,
                metric_type=metric_type,
                value=value,
                unit=unit,
                timestamp=datetime.now(),
                threshold=threshold,
            )

            # Update snapshot
            snapshot.metrics[metric_type] = metric
            snapshot.timestamp = datetime.now()

            logger.debug(
                f"Health metric recorded: {agent_id} - {metric_type.value}: {value}{unit}"
            )

        except Exception as e:
            logger.error(f"Error recording health metric: {e}")

    def get_agent_health(self, agent_id: str) -> Optional[HealthSnapshot]:
        """Get health snapshot for a specific agent"""
        return self.health_data.get(agent_id)

    def get_all_agent_health(self) -> Dict[str, HealthSnapshot]:
        """Get health snapshots for all agents"""
        return self.health_data.copy()

    def get_health_alerts(
        self, severity: Optional[str] = None, agent_id: Optional[str] = None
    ) -> List[HealthAlert]:
        """Get health alerts with optional filtering"""
        alerts = list(self.alerts.values())

        if severity:
            alerts = [alert for alert in alerts if alert.severity == severity]

        if agent_id:
            alerts = [alert for alert in alerts if alert.agent_id == agent_id]

        return alerts

    def acknowledge_alert(self, alert_id: str):
        """Acknowledge a health alert"""
        if alert_id in self.alerts:
            self.alerts[alert_id].acknowledged = True
            logger.info(f"Alert {alert_id} acknowledged")

    def resolve_alert(self, alert_id: str):
        """Manually resolve a health alert"""
        if alert_id in self.alerts:
            self.alerts[alert_id].resolved = True
            logger.info(f"Alert {alert_id} manually resolved")

    def subscribe_to_health_updates(self, callback: Callable):
        """Subscribe to health update notifications"""
        self.health_callbacks.add(callback)

    def unsubscribe_from_health_updates(self, callback: Callable):
        """Unsubscribe from health update notifications"""
        self.health_callbacks.discard(callback)

    def set_health_threshold(
        self,
        metric_type: HealthMetricType,
        warning_threshold: float,
        critical_threshold: float,
        unit: str,
        description: str,
    ):
        """Set custom health threshold for a metric type"""
        threshold = HealthThreshold(
            metric_type=metric_type,
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
            unit=unit,
            description=description,
        )

        self.thresholds[metric_type] = threshold
        logger.info(f"Health threshold updated for {metric_type.value}")

    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        total_agents = len(self.health_data)
        active_alerts = len(
            [alert for alert in self.alerts.values() if not alert.resolved]
        )

        status_counts = {
            status.value: len(
                [s for s in self.health_data.values() if s.overall_status == status]
            )
            for status in HealthStatus
        }

        avg_health_score = sum(s.health_score for s in self.health_data.values()) / max(
            total_agents, 1
        )

        return {
            "total_agents": total_agents,
            "active_alerts": active_alerts,
            "status_distribution": status_counts,
            "average_health_score": round(avg_health_score, 2),
            "monitoring_active": self.monitoring_active,
            "last_update": datetime.now().isoformat(),
        }

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            logger.info("Running AgentHealthCoreMonitor smoke test...")

            # Test basic initialization
            logger.info("Testing basic initialization...")
            assert self.monitoring_active is False
            assert len(self.thresholds) > 0
            logger.info("Basic initialization passed")

            # Test metric recording
            logger.info("Testing metric recording...")
            self.record_health_metric(
                "test_agent", HealthMetricType.RESPONSE_TIME, 500.0, "ms"
            )
            assert "test_agent" in self.health_data
            logger.info("Metric recording passed")

            # Test health snapshot retrieval
            logger.info("Testing health snapshot retrieval...")
            health = self.get_agent_health("test_agent")
            assert health is not None
            assert health.agent_id == "test_agent"
            logger.info("Health snapshot retrieval passed")

            # Test alert creation
            logger.info("Testing alert creation...")
            # Start monitoring with shorter intervals for testing
            self.health_check_interval = 1
            self.alert_check_interval = 1
            self.start()
            time.sleep(2)  # Allow monitoring to process

            # Record a critical metric that should trigger an alert
            self.record_health_metric(
                "test_agent", HealthMetricType.RESPONSE_TIME, 6000.0, "ms"
            )
            time.sleep(2)  # Allow alert processing

            alerts = self.get_health_alerts()
            assert len(alerts) > 0, f"Expected alerts but got {len(alerts)}"
            logger.info("Alert creation passed")

            # Stop monitoring
            self.stop()

            # Test health summary
            logger.info("Testing health summary...")
            summary = self.get_health_summary()
            assert "total_agents" in summary
            assert "active_alerts" in summary
            logger.info("Health summary passed")

            # Cleanup
            logger.info("Cleaning up...")
            if "test_agent" in self.health_data:
                del self.health_data["test_agent"]

            logger.info("✅ AgentHealthCoreMonitor smoke test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ AgentHealthCoreMonitor smoke test FAILED: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False

    def shutdown(self):
        """Shutdown the health monitor"""
        self.stop()
        logger.info("AgentHealthCoreMonitor shutdown complete")


def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Health Core Monitor CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")

    args = parser.parse_args()

    if args.test:
        monitor = AgentHealthCoreMonitor()
        success = monitor.run_smoke_test()
        monitor.shutdown()
        exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
