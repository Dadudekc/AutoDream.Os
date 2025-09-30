#!/usr/bin/env python3
"""
Predictive Analytics Engine
===========================

Advanced performance prediction models for system load forecasting,
capacity planning, predictive maintenance, and anomaly detection.

V2 COMPLIANT: Modular architecture with separate models and core logic.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List

from .predictive_core import PredictiveEngineCore
from .predictive_models import (
    AnomalyDetection,
    CapacityForecast,
    PerformanceMetrics,
    PredictionResult,
    PredictiveModel,
    ResourceUtilization,
    SystemHealth,
)


class PredictiveEngine:
    """Advanced predictive analytics engine."""

    def __init__(self):
        self.core = PredictiveEngineCore()
        self.models = {}

    def add_performance_metrics(self, metrics: PerformanceMetrics) -> None:
        """Add performance metrics to the engine."""
        self.core.add_performance_metrics(metrics)

    def predict_cpu_usage(self, time_horizon: timedelta) -> PredictionResult:
        """Predict CPU usage for given time horizon."""
        return self.core.predict_cpu_usage(time_horizon)

    def predict_memory_usage(self, time_horizon: timedelta) -> PredictionResult:
        """Predict memory usage for given time horizon."""
        return self.core.predict_memory_usage(time_horizon)

    def predict_response_time(self, time_horizon: timedelta) -> PredictionResult:
        """Predict response time for given time horizon."""
        return self.core.predict_response_time(time_horizon)

    def detect_anomalies(self) -> List[AnomalyDetection]:
        """Detect anomalies in current metrics."""
        return self.core.detect_anomalies()

    def forecast_capacity(self, resource_type: str, time_horizon: timedelta) -> CapacityForecast:
        """Forecast capacity requirements."""
        return self.core.forecast_capacity(resource_type, time_horizon)

    def assess_system_health(self) -> SystemHealth:
        """Assess overall system health."""
        return self.core.assess_system_health()

    def get_resource_utilization(self, resource_name: str) -> ResourceUtilization:
        """Get resource utilization metrics."""
        return self.core.get_resource_utilization(resource_name)

    def create_performance_metrics(
        self,
        timestamp: datetime,
        cpu_usage: float,
        memory_usage: float,
        disk_io: float,
        network_io: float,
        response_time: float,
        throughput: float,
        error_rate: float,
        active_connections: int,
    ) -> PerformanceMetrics:
        """Create performance metrics object."""
        return PerformanceMetrics(
            timestamp=timestamp,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_io=disk_io,
            network_io=network_io,
            response_time=response_time,
            throughput=throughput,
            error_rate=error_rate,
            active_connections=active_connections,
        )

    def get_prediction_summary(self, time_horizon: timedelta) -> Dict[str, Any]:
        """Get summary of all predictions."""
        cpu_prediction = self.predict_cpu_usage(time_horizon)
        memory_prediction = self.predict_memory_usage(time_horizon)
        response_prediction = self.predict_response_time(time_horizon)
        
        anomalies = self.detect_anomalies()
        system_health = self.assess_system_health()
        
        return {
            "cpu_prediction": {
                "value": cpu_prediction.predicted_value,
                "confidence": cpu_prediction.confidence,
                "trend": cpu_prediction.trend,
            },
            "memory_prediction": {
                "value": memory_prediction.predicted_value,
                "confidence": memory_prediction.confidence,
                "trend": memory_prediction.trend,
            },
            "response_prediction": {
                "value": response_prediction.predicted_value,
                "confidence": response_prediction.confidence,
                "trend": response_prediction.trend,
            },
            "anomalies": [
                {
                    "metric": anomaly.metric_name,
                    "severity": anomaly.severity,
                    "score": anomaly.anomaly_score,
                }
                for anomaly in anomalies
            ],
            "system_health": {
                "overall_health": system_health.overall_health,
                "health_score": system_health.health_score,
                "issues": system_health.issues,
            },
        }

    def get_capacity_forecasts(self, time_horizon: timedelta) -> Dict[str, CapacityForecast]:
        """Get capacity forecasts for all resources."""
        return {
            "cpu": self.forecast_capacity("cpu", time_horizon),
            "memory": self.forecast_capacity("memory", time_horizon),
            "disk": self.forecast_capacity("disk", time_horizon),
        }

    def get_resource_utilizations(self) -> Dict[str, ResourceUtilization]:
        """Get utilization metrics for all resources."""
        return {
            "cpu": self.get_resource_utilization("cpu"),
            "memory": self.get_resource_utilization("memory"),
            "disk": self.get_resource_utilization("disk"),
        }

    def export_metrics(self) -> List[Dict[str, Any]]:
        """Export metrics history as JSON-serializable data."""
        return [
            {
                "timestamp": m.timestamp.isoformat(),
                "cpu_usage": m.cpu_usage,
                "memory_usage": m.memory_usage,
                "disk_io": m.disk_io,
                "network_io": m.network_io,
                "response_time": m.response_time,
                "throughput": m.throughput,
                "error_rate": m.error_rate,
                "active_connections": m.active_connections,
            }
            for m in self.core.metrics_history
        ]

    def import_metrics(self, metrics_data: List[Dict[str, Any]]) -> None:
        """Import metrics from JSON data."""
        for data in metrics_data:
            metrics = PerformanceMetrics(
                timestamp=datetime.fromisoformat(data["timestamp"]),
                cpu_usage=data["cpu_usage"],
                memory_usage=data["memory_usage"],
                disk_io=data["disk_io"],
                network_io=data["network_io"],
                response_time=data["response_time"],
                throughput=data["throughput"],
                error_rate=data["error_rate"],
                active_connections=data["active_connections"],
            )
            self.add_performance_metrics(metrics)

    def get_engine_status(self) -> Dict[str, Any]:
        """Get engine status and statistics."""
        return {
            "metrics_count": len(self.core.metrics_history),
            "models_count": len(self.models),
            "anomaly_threshold": self.core.anomaly_threshold,
            "last_metric_time": (
                self.core.metrics_history[-1].timestamp.isoformat()
                if self.core.metrics_history
                else None
            ),
        }

    def configure_anomaly_threshold(self, threshold: float) -> None:
        """Configure anomaly detection threshold."""
        self.core.anomaly_threshold = max(0.0, min(1.0, threshold))

    def clear_metrics_history(self) -> None:
        """Clear metrics history."""
        self.core.metrics_history = []

    def get_metrics_statistics(self) -> Dict[str, Any]:
        """Get statistics about metrics history."""
        if not self.core.metrics_history:
            return {"message": "No metrics available"}
        
        metrics = self.core.metrics_history
        
        return {
            "total_metrics": len(metrics),
            "time_range": {
                "start": metrics[0].timestamp.isoformat(),
                "end": metrics[-1].timestamp.isoformat(),
            },
            "cpu_stats": {
                "min": min(m.cpu_usage for m in metrics),
                "max": max(m.cpu_usage for m in metrics),
                "avg": sum(m.cpu_usage for m in metrics) / len(metrics),
            },
            "memory_stats": {
                "min": min(m.memory_usage for m in metrics),
                "max": max(m.memory_usage for m in metrics),
                "avg": sum(m.memory_usage for m in metrics) / len(metrics),
            },
            "response_time_stats": {
                "min": min(m.response_time for m in metrics),
                "max": max(m.response_time for m in metrics),
                "avg": sum(m.response_time for m in metrics) / len(metrics),
            },
        }