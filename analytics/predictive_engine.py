"""
Predictive Analytics Engine
==========================

Advanced performance prediction models for system load forecasting,
capacity planning, predictive maintenance, and anomaly detection.
"""

from __future__ import annotations

import json
import math
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

# ---------- Core Data Models ----------


@dataclass
class PerformanceMetrics:
    """System performance metrics for prediction models."""

    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_io: float
    network_io: float
    response_time: float
    throughput: float
    error_rate: float
    active_connections: int


@dataclass
class PredictionResult:
    """Result of a predictive analysis."""

    metric_name: str
    predicted_value: float
    confidence: float
    time_horizon: timedelta
    trend: str  # "increasing", "decreasing", "stable"
    anomaly_score: float
    recommendations: list[str] = field(default_factory=list)


@dataclass
class CapacityForecast:
    """Capacity planning forecast."""

    resource_type: str
    current_usage: float
    predicted_usage: float
    time_to_limit: timedelta | None
    scaling_recommendation: str
    confidence: float


# ---------- Prediction Models ----------


class LoadForecastingModel:
    """System load forecasting using time series analysis."""

    def __init__(self, window_size: int = 24):
        self.window_size = window_size
        self.historical_data: list[PerformanceMetrics] = []

    def add_metric(self, metric: PerformanceMetrics) -> None:
        """Add new performance metric to historical data."""
        self.historical_data.append(metric)
        # Keep only recent data
        if len(self.historical_data) > self.window_size * 2:
            self.historical_data = self.historical_data[-self.window_size :]

    def predict_load(self, hours_ahead: int = 1) -> PredictionResult:
        """Predict system load for specified hours ahead."""
        if len(self.historical_data) < 3:
            # Use current data if available, otherwise return zero
            if self.historical_data:
                current_metric = self.historical_data[-1]
                predicted_value = (current_metric.cpu_usage + current_metric.memory_usage) / 2
            else:
                predicted_value = 0.0

            return PredictionResult(
                metric_name="system_load",
                predicted_value=predicted_value,
                confidence=0.0,
                time_horizon=timedelta(hours=hours_ahead),
                trend="stable",
                anomaly_score=0.0,
                recommendations=["Insufficient data for prediction"],
            )

        # Simple linear regression for trend
        recent_data = self.historical_data[-self.window_size :]
        cpu_values = [m.cpu_usage for m in recent_data]
        memory_values = [m.memory_usage for m in recent_data]

        # Calculate trend
        cpu_trend = self._calculate_trend(cpu_values)
        memory_trend = self._calculate_trend(memory_values)

        # Predict future values
        current_cpu = cpu_values[-1]
        current_memory = memory_values[-1]

        predicted_cpu = current_cpu + (cpu_trend * hours_ahead)
        predicted_memory = current_memory + (memory_trend * hours_ahead)

        # Calculate confidence based on data consistency
        confidence = self._calculate_confidence(cpu_values, memory_values)

        # Determine trend direction
        avg_trend = (cpu_trend + memory_trend) / 2
        if avg_trend > 0.05:
            trend = "increasing"
        elif avg_trend < -0.05:
            trend = "decreasing"
        else:
            trend = "stable"

        # Generate recommendations
        recommendations = self._generate_load_recommendations(
            predicted_cpu, predicted_memory, trend
        )

        return PredictionResult(
            metric_name="system_load",
            predicted_value=(predicted_cpu + predicted_memory) / 2,
            confidence=confidence,
            time_horizon=timedelta(hours=hours_ahead),
            trend=trend,
            anomaly_score=self._detect_anomaly(cpu_values, memory_values),
            recommendations=recommendations,
        )

    def _calculate_trend(self, values: list[float]) -> float:
        """Calculate linear trend slope."""
        if len(values) < 2:
            return 0.0

        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x2_sum = sum(i * i for i in range(n))

        slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum)
        return slope

    def _calculate_confidence(self, cpu_values: list[float], memory_values: list[float]) -> float:
        """Calculate prediction confidence based on data consistency."""
        if len(cpu_values) < 3:
            return 0.0

        cpu_std = statistics.stdev(cpu_values)
        memory_std = statistics.stdev(memory_values)

        # Lower standard deviation = higher confidence
        avg_std = (cpu_std + memory_std) / 2
        confidence = max(0.0, 1.0 - (avg_std / 50.0))  # Normalize to 0-1
        return min(1.0, confidence)

    def _detect_anomaly(self, cpu_values: list[float], memory_values: list[float]) -> float:
        """Detect anomalies in recent data."""
        if len(cpu_values) < 5:
            return 0.0

        # Simple anomaly detection using z-score
        cpu_mean = statistics.mean(cpu_values)
        cpu_std = statistics.stdev(cpu_values)
        memory_mean = statistics.mean(memory_values)
        memory_std = statistics.stdev(memory_values)

        latest_cpu = cpu_values[-1]
        latest_memory = memory_values[-1]

        cpu_z = abs((latest_cpu - cpu_mean) / cpu_std) if cpu_std > 0 else 0
        memory_z = abs((latest_memory - memory_mean) / memory_std) if memory_std > 0 else 0

        # Anomaly score is max z-score normalized to 0-1
        max_z = max(cpu_z, memory_z)
        return min(1.0, max_z / 3.0)  # 3-sigma threshold

    def _generate_load_recommendations(
        self, predicted_cpu: float, predicted_memory: float, trend: str
    ) -> list[str]:
        """Generate recommendations based on predicted load."""
        recommendations = []

        if predicted_cpu > 80:
            recommendations.append("Consider CPU scaling - predicted usage > 80%")
        if predicted_memory > 85:
            recommendations.append("Consider memory scaling - predicted usage > 85%")

        if trend == "increasing":
            recommendations.append("Load trend is increasing - monitor closely")
        elif trend == "decreasing":
            recommendations.append("Load trend is decreasing - good performance")

        if predicted_cpu > 90 or predicted_memory > 90:
            recommendations.append(
                "URGENT: Predicted resource exhaustion - immediate scaling required"
            )

        return recommendations


class CapacityPlanningModel:
    """Capacity planning and resource forecasting."""

    def __init__(self):
        self.resource_limits = {"cpu": 100.0, "memory": 100.0, "disk": 100.0, "network": 100.0}

    def forecast_capacity(
        self, current_metrics: PerformanceMetrics, growth_rate: float = 0.1
    ) -> list[CapacityForecast]:
        """Forecast capacity requirements."""
        forecasts = []

        # CPU forecast
        cpu_forecast = self._forecast_resource("CPU", current_metrics.cpu_usage, growth_rate)
        forecasts.append(cpu_forecast)

        # Memory forecast
        memory_forecast = self._forecast_resource(
            "Memory", current_metrics.memory_usage, growth_rate
        )
        forecasts.append(memory_forecast)

        # Disk forecast (using disk_io as proxy)
        disk_forecast = self._forecast_resource("Disk", current_metrics.disk_io, growth_rate)
        forecasts.append(disk_forecast)

        # Network forecast
        network_forecast = self._forecast_resource(
            "Network", current_metrics.network_io, growth_rate
        )
        forecasts.append(network_forecast)

        return forecasts

    def _forecast_resource(
        self, resource_type: str, current_usage: float, growth_rate: float
    ) -> CapacityForecast:
        """Forecast individual resource capacity."""
        # Simple exponential growth model
        predicted_usage = current_usage * (1 + growth_rate)

        # Calculate time to reach 80% capacity
        time_to_limit = None
        if predicted_usage > current_usage:
            time_to_80 = math.log(80.0 / current_usage) / math.log(1 + growth_rate)
            time_to_limit = timedelta(hours=time_to_80)

        # Generate scaling recommendation
        if predicted_usage > 90:
            scaling_rec = "Immediate scaling required"
            confidence = 0.9
        elif predicted_usage > 80:
            scaling_rec = "Plan scaling within 1-2 weeks"
            confidence = 0.8
        elif predicted_usage > 70:
            scaling_rec = "Monitor closely, consider scaling"
            confidence = 0.7
        else:
            scaling_rec = "Current capacity sufficient"
            confidence = 0.6

        return CapacityForecast(
            resource_type=resource_type,
            current_usage=current_usage,
            predicted_usage=predicted_usage,
            time_to_limit=time_to_limit,
            scaling_recommendation=scaling_rec,
            confidence=confidence,
        )


class AnomalyDetectionModel:
    """Anomaly detection for system behavior."""

    def __init__(self, threshold: float = 2.0):
        self.threshold = threshold
        self.baseline_metrics: PerformanceMetrics | None = None

    def detect_anomalies(self, current_metrics: PerformanceMetrics) -> list[PredictionResult]:
        """Detect anomalies in current system metrics."""
        anomalies = []

        if self.baseline_metrics is None:
            self.baseline_metrics = current_metrics
            return anomalies

        # Check each metric for anomalies
        metrics_to_check = [
            ("cpu_usage", current_metrics.cpu_usage, self.baseline_metrics.cpu_usage),
            ("memory_usage", current_metrics.memory_usage, self.baseline_metrics.memory_usage),
            ("response_time", current_metrics.response_time, self.baseline_metrics.response_time),
            ("error_rate", current_metrics.error_rate, self.baseline_metrics.error_rate),
            ("throughput", current_metrics.throughput, self.baseline_metrics.throughput),
        ]

        for metric_name, current, baseline in metrics_to_check:
            if baseline == 0:
                continue

            # Calculate deviation
            deviation = abs(current - baseline) / baseline

            if deviation > self.threshold:
                anomaly_score = min(1.0, deviation / (self.threshold * 2))

                recommendations = self._generate_anomaly_recommendations(
                    metric_name, current, baseline, deviation
                )

                anomalies.append(
                    PredictionResult(
                        metric_name=f"{metric_name}_anomaly",
                        predicted_value=current,
                        confidence=anomaly_score,
                        time_horizon=timedelta(minutes=0),
                        trend="anomaly" if current > baseline else "improvement",
                        anomaly_score=anomaly_score,
                        recommendations=recommendations,
                    )
                )

        return anomalies

    def _generate_anomaly_recommendations(
        self, metric_name: str, current: float, baseline: float, deviation: float
    ) -> list[str]:
        """Generate recommendations for detected anomalies."""
        recommendations = []

        if metric_name == "cpu_usage" and current > baseline:
            recommendations.append("High CPU usage detected - investigate processes")
            recommendations.append("Consider CPU scaling or optimization")

        elif metric_name == "memory_usage" and current > baseline:
            recommendations.append("High memory usage detected - check for leaks")
            recommendations.append("Consider memory scaling")

        elif metric_name == "response_time" and current > baseline:
            recommendations.append("Response time degradation detected")
            recommendations.append("Check database queries and network latency")

        elif metric_name == "error_rate" and current > baseline:
            recommendations.append("Error rate spike detected - investigate logs")
            recommendations.append("Check for recent deployments or changes")

        elif metric_name == "throughput" and current < baseline:
            recommendations.append("Throughput drop detected - check system health")
            recommendations.append("Investigate bottlenecks")

        return recommendations


# ---------- Main Predictive Engine ----------


class PredictiveAnalyticsEngine:
    """Main predictive analytics engine coordinating all models."""

    def __init__(self):
        self.load_forecaster = LoadForecastingModel()
        self.capacity_planner = CapacityPlanningModel()
        self.anomaly_detector = AnomalyDetectionModel()
        self.prediction_history: list[dict[str, Any]] = []

    def analyze_performance(self, metrics: PerformanceMetrics) -> dict[str, Any]:
        """Comprehensive performance analysis with predictions."""
        # Add metrics to forecaster
        self.load_forecaster.add_metric(metrics)

        # Generate predictions
        load_prediction = self.load_forecaster.predict_load(hours_ahead=1)
        capacity_forecasts = self.capacity_planner.forecast_capacity(metrics)
        anomalies = self.anomaly_detector.detect_anomalies(metrics)

        # Compile results
        analysis = {
            "timestamp": metrics.timestamp.isoformat(),
            "current_metrics": {
                "cpu_usage": metrics.cpu_usage,
                "memory_usage": metrics.memory_usage,
                "response_time": metrics.response_time,
                "error_rate": metrics.error_rate,
                "throughput": metrics.throughput,
            },
            "predictions": {
                "load_forecast": {
                    "predicted_value": load_prediction.predicted_value,
                    "confidence": load_prediction.confidence,
                    "trend": load_prediction.trend,
                    "anomaly_score": load_prediction.anomaly_score,
                    "recommendations": load_prediction.recommendations,
                },
                "capacity_forecasts": [
                    {
                        "resource": f.resource_type,
                        "current_usage": f.current_usage,
                        "predicted_usage": f.predicted_usage,
                        "time_to_limit": f.time_to_limit.total_seconds() / 3600
                        if f.time_to_limit
                        else None,
                        "scaling_recommendation": f.scaling_recommendation,
                        "confidence": f.confidence,
                    }
                    for f in capacity_forecasts
                ],
                "anomalies": [
                    {
                        "metric": a.metric_name,
                        "value": a.predicted_value,
                        "confidence": a.confidence,
                        "anomaly_score": a.anomaly_score,
                        "recommendations": a.recommendations,
                    }
                    for a in anomalies
                ],
            },
            "overall_health": self._calculate_overall_health(metrics, load_prediction, anomalies),
        }

        # Store in history
        self.prediction_history.append(analysis)
        if len(self.prediction_history) > 100:  # Keep last 100 analyses
            self.prediction_history = self.prediction_history[-100:]

        return analysis

    def _calculate_overall_health(
        self,
        metrics: PerformanceMetrics,
        load_prediction: PredictionResult,
        anomalies: list[PredictionResult],
    ) -> dict[str, Any]:
        """Calculate overall system health score."""
        # Base health from current metrics
        cpu_health = max(0, 1 - metrics.cpu_usage / 100)
        memory_health = max(0, 1 - metrics.memory_usage / 100)
        response_health = max(0, 1 - min(1, metrics.response_time / 1000))  # 1s threshold
        error_health = max(0, 1 - metrics.error_rate)

        # Weighted health score
        health_score = (
            cpu_health * 0.3 + memory_health * 0.3 + response_health * 0.2 + error_health * 0.2
        )

        # Adjust for anomalies
        if anomalies:
            anomaly_penalty = sum(a.anomaly_score for a in anomalies) / len(anomalies)
            health_score *= 1 - anomaly_penalty * 0.3

        # Determine health status
        if health_score > 0.8:
            status = "excellent"
        elif health_score > 0.6:
            status = "good"
        elif health_score > 0.4:
            status = "fair"
        else:
            status = "poor"

        return {
            "score": round(health_score * 100, 2),
            "status": status,
            "components": {
                "cpu_health": round(cpu_health * 100, 2),
                "memory_health": round(memory_health * 100, 2),
                "response_health": round(response_health * 100, 2),
                "error_health": round(error_health * 100, 2),
            },
        }

    def get_prediction_history(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent prediction history."""
        return self.prediction_history[-limit:]

    def save_analysis(self, filepath: str) -> None:
        """Save current analysis to file."""
        if not self.prediction_history:
            return

        latest_analysis = self.prediction_history[-1]
        with open(filepath, "w") as f:
            json.dump(latest_analysis, f, indent=2, default=str)
