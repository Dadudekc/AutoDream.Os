"""
Predictive Analytics Orchestrator - V2 Compliant
===============================================

Main orchestrator for predictive analytics system.
V2 Compliance: ≤400 lines, ≤10 functions, orchestrates components
"""

from datetime import timedelta

from .anomaly_detector import AnomalyDetector
from .capacity_forecaster import CapacityForecaster
from .predictive_core import PredictiveEngineCore
from .predictive_models import (
    AnomalyDetection,
    CapacityForecast,
    PerformanceMetrics,
    ResourceUtilization,
    SystemHealth,
)
from .system_health_assessor import SystemHealthAssessor


class PredictiveAnalyticsOrchestrator:
    """Main orchestrator for predictive analytics system."""

    def __init__(self):
        """Initialize predictive analytics orchestrator."""
        self.core = PredictiveEngineCore()
        self.anomaly_detector = AnomalyDetector()
        self.capacity_forecaster = CapacityForecaster()
        self.health_assessor = SystemHealthAssessor()

    def add_performance_metrics(self, metrics: PerformanceMetrics) -> None:
        """Add performance metrics to the system."""
        self.core.add_performance_metrics(metrics)

    def get_comprehensive_prediction(self, time_horizon: timedelta) -> dict:
        """Get comprehensive prediction for all metrics."""
        predictions = {}

        # Get individual predictions
        predictions["cpu"] = self.core.predict_cpu_usage(time_horizon)
        predictions["memory"] = self.core.predict_memory_usage(time_horizon)
        predictions["response_time"] = self.core.predict_response_time(time_horizon)

        return predictions

    def get_anomaly_report(self) -> list[AnomalyDetection]:
        """Get current anomaly detection report."""
        return self.anomaly_detector.detect_anomalies(self.core.metrics_history)

    def get_capacity_forecast(
        self, resource_type: str, time_horizon: timedelta
    ) -> CapacityForecast:
        """Get capacity forecast for a specific resource."""
        return self.capacity_forecaster.forecast_capacity(
            resource_type, time_horizon, self.core.metrics_history
        )

    def get_system_health(self) -> SystemHealth:
        """Get current system health assessment."""
        return self.health_assessor.assess_system_health(self.core.metrics_history)

    def get_resource_utilization(self, resource_name: str) -> ResourceUtilization:
        """Get resource utilization information."""
        return self.capacity_forecaster.get_resource_utilization(
            resource_name, self.core.metrics_history
        )

    def get_system_summary(self) -> dict:
        """Get comprehensive system summary."""
        time_horizon = timedelta(hours=1)

        # Get all predictions
        predictions = self.get_comprehensive_prediction(time_horizon)

        # Get anomalies
        anomalies = self.get_anomaly_report()

        # Get system health
        health = self.get_system_health()

        # Get capacity forecasts for key resources
        capacity_forecasts = {}
        for resource in ["cpu", "memory", "disk"]:
            capacity_forecasts[resource] = self.get_capacity_forecast(resource, time_horizon)

        return {
            "predictions": predictions,
            "anomalies": anomalies,
            "system_health": health,
            "capacity_forecasts": capacity_forecasts,
            "metrics_count": len(self.core.metrics_history),
            "anomaly_threshold": self.anomaly_detector.get_threshold(),
        }

    def update_anomaly_threshold(self, new_threshold: float) -> None:
        """Update anomaly detection threshold."""
        self.anomaly_detector.update_threshold(new_threshold)

    def get_metrics_count(self) -> int:
        """Get number of metrics in history."""
        return len(self.core.metrics_history)

    def clear_metrics_history(self) -> None:
        """Clear metrics history."""
        self.core.metrics_history.clear()
