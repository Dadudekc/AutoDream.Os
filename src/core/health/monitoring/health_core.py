"""Unified Health Monitoring Core - Consolidated from monitoring/ and monitoring_new/"""

import logging
import threading
import time
from typing import Any, Dict, Optional, Set, Callable

from ..monitoring_new.health_monitoring_new_config import (
    HealthAlert,
    HealthMetricType,
    HealthSnapshot,
    HealthStatus,
    HealthThreshold,
    initialize_default_thresholds,
)
from ..monitoring_new.health_monitoring_new_collector import collect_health_metrics, record_health_metric
from ..monitoring_new.health_monitoring_new_analyzer import (
    acknowledge_alert,
    check_alerts,
    get_agent_health,
    get_all_agent_health,
    get_health_alerts,
    get_health_summary,
    notify_health_updates,
    perform_health_checks,
    update_health_scores,
    update_threshold,
)

logger = logging.getLogger(__name__)


class AgentHealthCoreMonitor:
    """Unified health monitoring orchestrator - consolidated from monitoring/ and monitoring_new/"""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.monitoring_active = False
        self.health_data: Dict[str, HealthSnapshot] = {}
        self.alerts: Dict[str, HealthAlert] = {}
        self.thresholds: Dict[HealthMetricType, HealthThreshold] = (
            initialize_default_thresholds()
        )
        self.health_callbacks: Set[Callable] = set()
        self.monitor_thread: Optional[threading.Thread] = None
        self.metrics_interval = self.config.get("metrics_interval", 30)
        self.health_check_interval = self.config.get("health_check_interval", 60)
        self.alert_check_interval = self.config.get("alert_check_interval", 15)
        logger.info("✅ Unified AgentHealthCoreMonitor initialized with default thresholds")

    def start(self) -> None:
        """Start unified health monitoring"""
        if self.monitoring_active:
            logger.warning("Health monitoring already active")
            return
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("🚀 Unified health monitoring started")

    def stop(self) -> None:
        """Stop unified health monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("⏹️ Unified health monitoring stopped")

    def _monitor_loop(self) -> None:
        """Main monitoring loop for unified health system"""
        while self.monitoring_active:
            try:
                collect_health_metrics()
                perform_health_checks(self.health_data, self.thresholds, self.alerts)
                check_alerts(self.alerts, self.health_data)
                update_health_scores(self.health_data, self.thresholds)
                notify_health_updates(
                    self.health_callbacks, self.health_data, self.alerts
                )
                time.sleep(self.health_check_interval)
            except Exception as exc:
                logger.error("Error in unified health monitoring loop: %s", exc)
                time.sleep(10)

    # Unified monitoring methods -------------------------------------------------
    def record_health_metric(
        self,
        agent_id: str,
        metric_type: HealthMetricType,
        value: float,
        unit: str,
        threshold: Optional[float] = None,
    ) -> None:
        """Record health metric using unified system"""
        record_health_metric(
            self.health_data, agent_id, metric_type, value, unit, threshold
        )

    def get_agent_health(self, agent_id: str) -> Optional[HealthSnapshot]:
        """Get agent health using unified system"""
        return get_agent_health(self.health_data, agent_id)

    def get_all_agent_health(self) -> Dict[str, HealthSnapshot]:
        """Get all agent health using unified system"""
        return get_all_agent_health(self.health_data)

    def get_health_alerts(
        self, severity: Optional[str] = None, agent_id: Optional[str] = None
    ) -> list:
        """Get health alerts using unified system"""
        return get_health_alerts(self.alerts, severity, agent_id)

    def acknowledge_alert(self, alert_id: str) -> None:
        """Acknowledge alert using unified system"""
        acknowledge_alert(self.alerts, alert_id)

    def update_threshold(self, threshold: HealthThreshold) -> None:
        """Update threshold using unified system"""
        update_threshold(self.thresholds, threshold)

    def get_health_summary(self) -> Dict[str, Any]:
        """Get health summary using unified system"""
        return get_health_summary(self.health_data, self.alerts, self.monitoring_active)

    def run_smoke_test(self) -> bool:
        """Run smoke test for unified health monitoring system"""
        try:
            logger.info("🧪 Running Unified AgentHealthCoreMonitor smoke test...")
            assert self.monitoring_active is False
            assert len(self.thresholds) > 0
            logger.info("✅ Basic initialization passed")
            
            self.record_health_metric(
                "test_agent", HealthMetricType.RESPONSE_TIME, 500.0, "ms"
            )
            assert "test_agent" in self.health_data
            logger.info("✅ Metric recording passed")
            
            health = self.get_agent_health("test_agent")
            assert health is not None and health.agent_id == "test_agent"
            logger.info("✅ Health snapshot retrieval passed")
            
            self.health_check_interval = 1
            self.alert_check_interval = 1
            self.start()
            time.sleep(2)
            
            self.record_health_metric(
                "test_agent", HealthMetricType.RESPONSE_TIME, 6000.0, "ms"
            )
            time.sleep(2)
            
            alerts = self.get_health_alerts()
            assert len(alerts) > 0
            logger.info("✅ Alert creation passed")
            
            self.stop()
            summary = self.get_health_summary()
            assert "total_agents" in summary
            logger.info("✅ Health summary passed")
            
            if "test_agent" in self.health_data:
                del self.health_data["test_agent"]
            
            logger.info("🎯 Unified AgentHealthCoreMonitor smoke test PASSED")
            return True
            
        except Exception as exc:
            logger.error("❌ Unified AgentHealthCoreMonitor smoke test FAILED: %s", exc)
            return False

    def shutdown(self) -> None:
        """Shutdown unified health monitoring system"""
        self.stop()
        logger.info("🔄 Unified AgentHealthCoreMonitor shutdown complete")


# Unified monitoring orchestrator alias
HealthMonitoringOrchestrator = AgentHealthCoreMonitor

