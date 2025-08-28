"""Core functionality for the authentication performance monitor."""

import logging
import threading
import time
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from auth_service import AuthService, AuthStatus

    PERFORMANCE_MONITORING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Performance monitoring components not available: {e}")
    AuthService = Any  # type: ignore
    AuthStatus = Any  # type: ignore
    PERFORMANCE_MONITORING_AVAILABLE = False

from .auth_performance_config import get_default_config
from .auth_performance_metrics import (
    collect_performance_metrics,
    analyze_performance,
    check_performance_alerts,
    calculate_performance_baselines,
    calculate_performance_indicators,
)
from .common_performance import PerformanceMetric, PerformanceAlert
from .auth_performance_reporting import PerformanceReport, generate_performance_report


class AuthPerformanceMonitor:
    """V2 Authentication Performance Monitor."""

    def __init__(self, config: Dict[str, Any] | None = None):
        self.logger = self._setup_logging()
        self.config = config or get_default_config()
        self.metrics_history = defaultdict(
            lambda: deque(maxlen=self.config["max_metrics_history"])
        )
        self.alerts_history = deque(maxlen=self.config["max_alerts_history"])
        self.performance_thresholds = self.config["performance_thresholds"]
        self.is_monitoring = False
        self.monitoring_thread = None
        self.monitoring_interval = self.config["monitoring_interval"]
        self.alert_counts = defaultdict(int)
        self.last_alert_time = defaultdict(datetime.now)
        self.baselines: Dict[str, Any] = {}
        self.baseline_calculated = False
        self.logger.info("V2 Authentication Performance Monitor initialized")

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def start_monitoring(self, auth_service: AuthService):
        """Start real-time performance monitoring."""
        if self.is_monitoring:
            self.logger.warning("Performance monitoring already active")
            return
        if not PERFORMANCE_MONITORING_AVAILABLE:
            self.logger.error("Performance monitoring components not available")
            return
        self.auth_service = auth_service
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self.monitoring_thread.start()
        self.logger.info("🚀 Performance monitoring started")

    def stop_monitoring(self):
        """Stop real-time performance monitoring."""
        if not self.is_monitoring:
            return
        self.is_monitoring = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)
        self.logger.info("🛑 Performance monitoring stopped")

    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                collect_performance_metrics(self)
                analyze_performance(self)
                if self.config["enable_performance_alerts"]:
                    check_performance_alerts(self)
                if (
                    self.config["enable_baseline_calculation"]
                    and not self.baseline_calculated
                ):
                    calculate_performance_baselines(self)
                time.sleep(self.monitoring_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval)

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get current performance summary."""
        try:
            summary = {
                "monitoring_active": self.is_monitoring,
                "metrics_tracked": len(self.metrics_history),
                "total_alerts": len(self.alerts_history),
                "baseline_calculated": self.baseline_calculated,
                "current_metrics": {},
                "recent_alerts": [],
                "performance_indicators": {},
            }
            for metric_name, metrics in self.metrics_history.items():
                if metrics:
                    latest = metrics[-1]
                    summary["current_metrics"][metric_name] = {
                        "value": latest.value,
                        "unit": latest.unit,
                        "timestamp": latest.timestamp.isoformat(),
                    }
            recent_alerts = list(self.alerts_history)[-5:]
            summary["recent_alerts"] = [
                {
                    "type": alert.alert_type,
                    "message": alert.message,
                    "severity": alert.severity,
                    "timestamp": alert.timestamp.isoformat(),
                }
                for alert in recent_alerts
            ]
            summary["performance_indicators"] = calculate_performance_indicators(self)
            return summary
        except Exception as e:
            self.logger.error(f"Failed to generate performance summary: {e}")
            return {"error": str(e)}

    def generate_performance_report(
        self, time_period: str = "current"
    ) -> PerformanceReport:
        """Generate comprehensive performance report."""
        return generate_performance_report(self, time_period)

    def cleanup(self):
        """Cleanup performance monitor resources."""
        try:
            self.stop_monitoring()
            self.logger.info("✅ Performance monitor resources cleaned up")
        except Exception as e:
            self.logger.error(f"❌ Performance monitor cleanup failed: {e}")


__all__ = [
    "AuthPerformanceMonitor",
    "PerformanceMetric",
    "PerformanceAlert",
    "PerformanceReport",
]
