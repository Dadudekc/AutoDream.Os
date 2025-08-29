#!/usr/bin/env python3
"""
🔍 Performance Dashboard - Agent_Cellphone_V2

Real-time performance monitoring dashboard and visualization system.
Following V2 coding standards: ≤500 LOC, OOP design, SRP.

Author: Performance & Monitoring Specialist
License: MIT
"""

import logging
import threading
import time

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import json

# Configure logging
logger = logging.getLogger(__name__)


class DashboardView(Enum):
    """Dashboard view types"""

    SYSTEM_OVERVIEW = "system_overview"
    AGENT_PERFORMANCE = "agent_performance"
    METRICS_DETAIL = "metrics_detail"
    ALERTS = "alerts"
    HISTORICAL = "historical"


class AlertLevel(Enum):
    """Alert severity levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class DashboardAlert:
    """Dashboard alert information"""

    id: str
    level: AlertLevel
    message: str
    timestamp: datetime
    source: str
    context: Dict[str, Any] = field(default_factory=dict)
    acknowledged: bool = False


@dataclass
class DashboardData:
    """Dashboard data structure"""

    timestamp: datetime
    system_metrics: Dict[str, float] = field(default_factory=dict)
    agent_metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    alerts: List[DashboardAlert] = field(default_factory=list)
    performance_summary: Dict[str, Any] = field(default_factory=dict)


class PerformanceDashboard:
    """
    Performance Dashboard - Single responsibility: Real-time performance monitoring and visualization.

    Follows V2 standards: ≤500 LOC, OOP design, SRP.
    """

    def __init__(
        self,
        agent_manager=None,
        performance_tracker=None,
        config_manager=None,
        message_router=None,
    ):
        """Initialize the performance dashboard"""
        self.agent_manager = agent_manager
        self.performance_tracker = performance_tracker
        self.config_manager = config_manager
        self.message_router = message_router

        # Dashboard state
        self.running = False
        self.current_view = DashboardView.SYSTEM_OVERVIEW
        self.refresh_interval = 5  # seconds

        # Data storage
        self.performance_snapshots: List[Dict[str, Any]] = []
        self.system_metrics: Dict[str, float] = {}
        self.agent_metrics: Dict[str, Dict[str, float]] = {}
        self.alerts: List[DashboardAlert] = []

        # Threading
        self.dashboard_thread: Optional[threading.Thread] = None
        self.lock = threading.RLock()

        # Callbacks
        self.update_callbacks: List[Callable] = []
        self.alert_callbacks: List[Callable] = []

        # Configuration
        self.max_snapshots = 1000
        self.alert_retention_hours = 24

        # Initialize if components are available
        if self.performance_tracker:
            self._setup_performance_tracking()

        logger.info("PerformanceDashboard initialized")

    def start(self):
        """Start the performance dashboard"""
        if self.running:
            logger.warning("Dashboard already running")
            return

        self.running = True
        self.dashboard_thread = threading.Thread(
            target=self._dashboard_loop, daemon=True
        )
        self.dashboard_thread.start()
        logger.info("Performance dashboard started")

    def stop(self):
        """Stop the performance dashboard"""
        self.running = False
        if self.dashboard_thread:
            self.dashboard_thread.join(timeout=5)
        logger.info("Performance dashboard stopped")

    def set_view(self, view: DashboardView):
        """Set the current dashboard view"""
        self.current_view = view
        logger.debug(f"Dashboard view changed to: {view.value}")

    def set_refresh_interval(self, interval: int):
        """Set the dashboard refresh interval in seconds"""
        self.refresh_interval = max(1, interval)
        logger.debug(f"Dashboard refresh interval set to: {self.refresh_interval}s")

    def get_dashboard_data(self) -> DashboardData:
        """Get current dashboard data"""
        with self.lock:
            return DashboardData(
                timestamp=datetime.now(),
                system_metrics=self.system_metrics.copy(),
                agent_metrics=self.agent_metrics.copy(),
                alerts=self.alerts.copy(),
                performance_summary=self._get_performance_summary(),
            )

    def get_agent_performance(self, agent_id: str) -> Dict[str, Any]:
        """Get performance data for a specific agent"""
        if not self.performance_tracker:
            return {}

        return self.performance_tracker.get_agent_performance_summary(agent_id)

    def get_system_performance(self) -> Dict[str, Any]:
        """Get overall system performance summary"""
        if not self.performance_tracker:
            return {}

        # Get recent snapshots
        snapshots = self.performance_tracker.get_performance_snapshots(10)
        if not snapshots:
            return {}

        # Aggregate system metrics
        system_summary = {}
        for snapshot in snapshots:
            for metric_name, value in snapshot.system_metrics.items():
                if metric_name not in system_summary:
                    system_summary[metric_name] = []
                system_summary[metric_name].append(value)

        # Calculate averages
        for metric_name, values in system_summary.items():
            if values:
                system_summary[metric_name] = sum(values) / len(values)

        return system_summary

    def add_alert(
        self,
        level: AlertLevel,
        message: str,
        source: str,
        context: Dict[str, Any] = None,
    ):
        """Add a new dashboard alert"""
        alert = DashboardAlert(
            id=f"alert_{int(time.time())}",
            level=level,
            message=message,
            timestamp=datetime.now(),
            source=source,
            context=context or {},
        )

        with self.lock:
            self.alerts.append(alert)

            # Maintain alert history
            self._cleanup_old_alerts()

        # Notify alert callbacks
        self._notify_alert_callbacks(alert)

        logger.info(f"Alert added: {level.value} - {message}")

    def acknowledge_alert(self, alert_id: str):
        """Acknowledge an alert"""
        with self.lock:
            for alert in self.alerts:
                if alert.id == alert_id:
                    alert.acknowledged = True
                    logger.debug(f"Alert acknowledged: {alert_id}")
                    break

    def get_alerts(
        self, level: Optional[AlertLevel] = None, acknowledged: Optional[bool] = None
    ) -> List[DashboardAlert]:
        """Get filtered alerts"""
        with self.lock:
            filtered_alerts = self.alerts

            if level is not None:
                filtered_alerts = [a for a in filtered_alerts if a.level == level]

            if acknowledged is not None:
                filtered_alerts = [
                    a for a in filtered_alerts if a.acknowledged == acknowledged
                ]

            return filtered_alerts.copy()

    def add_update_callback(self, callback: Callable):
        """Add callback for dashboard updates"""
        if callback not in self.update_callbacks:
            self.update_callbacks.append(callback)

    def add_alert_callback(self, callback: Callable):
        """Add callback for alert updates"""
        if callback not in self.alert_callbacks:
            self.alert_callbacks.append(callback)

    def export_dashboard_data(
        self, filepath: str, time_range: Optional[timedelta] = None
    ):
        """Export dashboard data to JSON file"""
        with self.lock:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "current_view": self.current_view.value,
                "performance_snapshots": [],
                "system_metrics": self.system_metrics,
                "agent_metrics": self.agent_metrics,
                "alerts": [],
            }

            # Export snapshots
            snapshots_to_export = self.performance_snapshots
            if time_range:
                cutoff_time = datetime.now() - time_range
                snapshots_to_export = [
                    s
                    for s in snapshots_to_export
                    if s.get("timestamp", datetime.now()) >= cutoff_time
                ]

            export_data["performance_snapshots"] = snapshots_to_export[
                -100:
            ]  # Last 100

            # Export alerts
            for alert in self.alerts:
                export_data["alerts"].append(
                    {
                        "id": alert.id,
                        "level": alert.level.value,
                        "message": alert.message,
                        "timestamp": alert.timestamp.isoformat(),
                        "source": alert.source,
                        "context": alert.context,
                        "acknowledged": alert.acknowledged,
                    }
                )

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Exported dashboard data to {filepath}")

    def _setup_performance_tracking(self):
        """Setup performance tracking integration"""
        if self.performance_tracker:
            # Add callbacks for real-time updates
            self.performance_tracker.add_metric_callback(self._on_metric_update)
            self.performance_tracker.add_snapshot_callback(self._on_snapshot_update)
            logger.info("Performance tracking integration configured")

    def _dashboard_loop(self):
        """Main dashboard update loop"""
        while self.running:
            try:
                # Update dashboard data
                self._update_dashboard_data()

                # Check for performance issues
                self._check_performance_issues()

                # Notify update callbacks
                self._notify_update_callbacks()

                time.sleep(self.refresh_interval)

            except Exception as e:
                logger.error(f"Error in dashboard loop: {e}")
                time.sleep(10)

    def _update_dashboard_data(self):
        """Update dashboard data from various sources"""
        with self.lock:
            # Update system metrics
            if self.performance_tracker:
                # Get latest system metrics from profiler if available
                try:
                    from .performance_monitor import PerformanceMonitor

                    profiler = PerformanceMonitor()
                    self.system_metrics.update(profiler.get_system_metrics())
                except ImportError:
                    # Fallback to basic system metrics
                    self.system_metrics.update(self._get_basic_system_metrics())

            # Update agent metrics
            if self.agent_manager:
                self._update_agent_metrics()

    def _update_agent_metrics(self):
        """Update agent performance metrics"""
        try:
            # This would integrate with the actual agent manager
            # For now, we'll use placeholder data
            if hasattr(self.agent_manager, "get_agents"):
                agents = self.agent_manager.get_agents()
                for agent_id in agents:
                    if self.performance_tracker:
                        agent_summary = (
                            self.performance_tracker.get_agent_performance_summary(
                                agent_id
                            )
                        )
                        if agent_summary:
                            self.agent_metrics[agent_id] = agent_summary
        except Exception as e:
            logger.debug(f"Could not update agent metrics: {e}")

    def _get_basic_system_metrics(self) -> Dict[str, float]:
        """Get basic system metrics as fallback"""
        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
            }
        except ImportError:
            return {
                "cpu_percent": 0.0,
                "memory_percent": 0.0,
                "memory_available_gb": 0.0,
            }

    def _check_performance_issues(self):
        """Check for performance issues and generate alerts"""
        # Check CPU usage
        cpu_percent = self.system_metrics.get("cpu_percent", 0)
        if cpu_percent > 90:
            self.add_alert(
                AlertLevel.CRITICAL,
                f"High CPU usage: {cpu_percent:.1f}%",
                "system_monitor",
                {"cpu_percent": cpu_percent},
            )
        elif cpu_percent > 80:
            self.add_alert(
                AlertLevel.WARNING,
                f"Elevated CPU usage: {cpu_percent:.1f}%",
                "system_monitor",
                {"cpu_percent": cpu_percent},
            )

        # Check memory usage
        memory_percent = self.system_metrics.get("memory_percent", 0)
        if memory_percent > 95:
            self.add_alert(
                AlertLevel.CRITICAL,
                f"Critical memory usage: {memory_percent:.1f}%",
                "system_monitor",
                {"memory_percent": memory_percent},
            )
        elif memory_percent > 85:
            self.add_alert(
                AlertLevel.WARNING,
                f"High memory usage: {memory_percent:.1f}%",
                "system_monitor",
                {"memory_percent": memory_percent},
            )

        # Check agent performance
        if self.agent_metrics:
            for agent_id, metrics in self.agent_metrics.items():
                self._check_agent_performance(agent_id, metrics)

    def _check_agent_performance(self, agent_id: str, metrics: Dict[str, Any]):
        """Check individual agent performance"""
        # Check response time
        if "response_time" in metrics:
            response_time = metrics["response_time"].get("latest", 0)
            if response_time > 5.0:  # 5 seconds threshold
                self.add_alert(
                    AlertLevel.WARNING,
                    f"Agent {agent_id} slow response: {response_time:.2f}s",
                    "agent_monitor",
                    {"agent_id": agent_id, "response_time": response_time},
                )

        # Check error rate
        if "error_rate" in metrics:
            error_rate = metrics["error_rate"].get("latest", 0)
            if error_rate > 0.1:  # 10% error rate threshold
                self.add_alert(
                    AlertLevel.ERROR,
                    f"Agent {agent_id} high error rate: {error_rate:.1%}",
                    "agent_monitor",
                    {"agent_id": agent_id, "error_rate": error_rate},
                )

    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary"""
        summary = {
            "total_alerts": len(self.alerts),
            "unacknowledged_alerts": len(
                [a for a in self.alerts if not a.acknowledged]
            ),
            "active_agents": len(self.agent_metrics),
            "system_health": self._calculate_system_health(),
        }

        return summary

    def _calculate_system_health(self) -> float:
        """Calculate overall system health score (0-100)"""
        health_score = 100.0

        # Deduct points for high resource usage
        cpu_percent = self.system_metrics.get("cpu_percent", 0)
        if cpu_percent > 80:
            health_score -= (cpu_percent - 80) * 0.5

        memory_percent = self.system_metrics.get("memory_percent", 0)
        if memory_percent > 80:
            health_score -= (memory_percent - 80) * 0.5

        # Deduct points for alerts
        critical_alerts = len(
            [a for a in self.alerts if a.level == AlertLevel.CRITICAL]
        )
        error_alerts = len([a for a in self.alerts if a.level == AlertLevel.ERROR])
        warning_alerts = len([a for a in self.alerts if a.level == AlertLevel.WARNING])

        health_score -= critical_alerts * 20
        health_score -= error_alerts * 10
        health_score -= warning_alerts * 5

        return max(0.0, health_score)

    def _cleanup_old_alerts(self):
        """Remove old alerts"""
        cutoff_time = datetime.now() - timedelta(hours=self.alert_retention_hours)
        self.alerts = [a for a in self.alerts if a.timestamp >= cutoff_time]

    def _on_metric_update(self, metric):
        """Handle performance metric updates"""
        # This would integrate with the performance tracker
        logger.debug(f"Metric update received: {metric}")

    def _on_snapshot_update(self, snapshot):
        """Handle performance snapshot updates"""
        with self.lock:
            self.performance_snapshots.append(
                {
                    "timestamp": snapshot.timestamp,
                    "metrics": snapshot.metrics,
                    "agent_metrics": snapshot.agent_metrics,
                    "system_metrics": snapshot.system_metrics,
                }
            )

            # Maintain snapshot history
            if len(self.performance_snapshots) > self.max_snapshots:
                self.performance_snapshots = self.performance_snapshots[
                    -self.max_snapshots :
                ]

    def _notify_update_callbacks(self):
        """Notify dashboard update callbacks"""
        for callback in self.update_callbacks:
            try:
                callback(self.get_dashboard_data())
            except Exception as e:
                logger.error(f"Error in update callback: {e}")

    def _notify_alert_callbacks(self, alert: DashboardAlert):
        """Notify alert update callbacks"""
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")

    def cleanup(self):
        """Cleanup dashboard resources"""
        self.stop()
        logger.info("PerformanceDashboard cleaned up")
