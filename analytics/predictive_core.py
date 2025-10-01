#!/usr/bin/env python3
"""
Predictive Analytics Core
=========================

Core functionality for predictive analytics engine.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Any, Dict, List

from .predictive_models import (
    AnomalyDetection,
    CapacityForecast,
    ForecastPeriod,
    PerformanceMetrics,
    PredictionResult,
    PredictiveModel,
    ResourceUtilization,
    SystemHealth,
)


class PredictiveEngineCore:
    """Core predictive analytics functionality."""

    def __init__(self):
        self.models = {}
        self.metrics_history = []
        self.anomaly_threshold = 0.8

    def add_performance_metrics(self, metrics: PerformanceMetrics) -> None:
        """Add performance metrics to history."""
        self.metrics_history.append(metrics)
        
        # Keep only last 1000 metrics to prevent memory issues
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]

    def predict_cpu_usage(self, time_horizon: timedelta) -> PredictionResult:
        """Predict CPU usage for given time horizon."""
        if not self.metrics_history:
            return self._create_default_prediction("cpu_usage", time_horizon)
        
        # Get recent CPU usage data
        recent_metrics = self._get_recent_metrics(time_horizon)
        cpu_values = [m.cpu_usage for m in recent_metrics]
        
        if not cpu_values:
            return self._create_default_prediction("cpu_usage", time_horizon)
        
        # Calculate prediction
        predicted_value = self._calculate_trend_prediction(cpu_values)
        confidence = self._calculate_confidence(cpu_values)
        trend = self._determine_trend(cpu_values)
        anomaly_score = self._calculate_anomaly_score(cpu_values)
        
        return PredictionResult(
            metric_name="cpu_usage",
            predicted_value=predicted_value,
            confidence=confidence,
            time_horizon=time_horizon,
            trend=trend,
            anomaly_score=anomaly_score,
            recommendations=self._generate_cpu_recommendations(predicted_value),
        )

    def predict_memory_usage(self, time_horizon: timedelta) -> PredictionResult:
        """Predict memory usage for given time horizon."""
        if not self.metrics_history:
            return self._create_default_prediction("memory_usage", time_horizon)
        
        # Get recent memory usage data
        recent_metrics = self._get_recent_metrics(time_horizon)
        memory_values = [m.memory_usage for m in recent_metrics]
        
        if not memory_values:
            return self._create_default_prediction("memory_usage", time_horizon)
        
        # Calculate prediction
        predicted_value = self._calculate_trend_prediction(memory_values)
        confidence = self._calculate_confidence(memory_values)
        trend = self._determine_trend(memory_values)
        anomaly_score = self._calculate_anomaly_score(memory_values)
        
        return PredictionResult(
            metric_name="memory_usage",
            predicted_value=predicted_value,
            confidence=confidence,
            time_horizon=time_horizon,
            trend=trend,
            anomaly_score=anomaly_score,
            recommendations=self._generate_memory_recommendations(predicted_value),
        )

    def predict_response_time(self, time_horizon: timedelta) -> PredictionResult:
        """Predict response time for given time horizon."""
        if not self.metrics_history:
            return self._create_default_prediction("response_time", time_horizon)
        
        # Get recent response time data
        recent_metrics = self._get_recent_metrics(time_horizon)
        response_values = [m.response_time for m in recent_metrics]
        
        if not response_values:
            return self._create_default_prediction("response_time", time_horizon)
        
        # Calculate prediction
        predicted_value = self._calculate_trend_prediction(response_values)
        confidence = self._calculate_confidence(response_values)
        trend = self._determine_trend(response_values)
        anomaly_score = self._calculate_anomaly_score(response_values)
        
        return PredictionResult(
            metric_name="response_time",
            predicted_value=predicted_value,
            confidence=confidence,
            time_horizon=time_horizon,
            trend=trend,
            anomaly_score=anomaly_score,
            recommendations=self._generate_response_time_recommendations(predicted_value),
        )

    def detect_anomalies(self) -> List[AnomalyDetection]:
        """Detect anomalies in current metrics."""
        if not self.metrics_history:
            return []
        
        anomalies = []
        recent_metrics = self.metrics_history[-10:]  # Last 10 metrics
        
        # Check CPU anomalies
        cpu_values = [m.cpu_usage for m in recent_metrics]
        if cpu_values:
            cpu_anomaly = self._check_metric_anomaly("cpu_usage", cpu_values)
            if cpu_anomaly:
                anomalies.append(cpu_anomaly)
        
        # Check memory anomalies
        memory_values = [m.memory_usage for m in recent_metrics]
        if memory_values:
            memory_anomaly = self._check_metric_anomaly("memory_usage", memory_values)
            if memory_anomaly:
                anomalies.append(memory_anomaly)
        
        # Check response time anomalies
        response_values = [m.response_time for m in recent_metrics]
        if response_values:
            response_anomaly = self._check_metric_anomaly("response_time", response_values)
            if response_anomaly:
                anomalies.append(response_anomaly)
        
        return anomalies

    def forecast_capacity(self, resource_type: str, time_horizon: timedelta) -> CapacityForecast:
        """Forecast capacity requirements."""
        if not self.metrics_history:
            return self._create_default_capacity_forecast(resource_type)
        
        # Get recent metrics for resource type
        recent_metrics = self._get_recent_metrics(time_horizon)
        
        if resource_type == "cpu":
            values = [m.cpu_usage for m in recent_metrics]
        elif resource_type == "memory":
            values = [m.memory_usage for m in recent_metrics]
        else:
            values = [m.disk_io for m in recent_metrics]
        
        if not values:
            return self._create_default_capacity_forecast(resource_type)
        
        current_usage = values[-1] if values else 0.0
        predicted_usage = self._calculate_trend_prediction(values)
        capacity_limit = 100.0  # Assume 100% capacity limit
        utilization_percentage = (predicted_usage / capacity_limit) * 100
        
        # Calculate time to limit
        if predicted_usage > current_usage:
            time_to_limit = self._calculate_time_to_limit(current_usage, predicted_usage, capacity_limit)
        else:
            time_to_limit = timedelta(days=365)  # Far future
        
        # Generate scaling recommendation
        scaling_recommendation = self._generate_scaling_recommendation(utilization_percentage)
        
        return CapacityForecast(
            resource_type=resource_type,
            current_usage=current_usage,
            predicted_usage=predicted_usage,
            capacity_limit=capacity_limit,
            utilization_percentage=utilization_percentage,
            time_to_limit=time_to_limit,
            scaling_recommendation=scaling_recommendation,
        )

    def assess_system_health(self) -> SystemHealth:
        """Assess overall system health."""
        if not self.metrics_history:
            return SystemHealth(
                overall_health="unknown",
                health_score=0.0,
                issues=["No metrics available"],
                recommendations=["Start collecting metrics"],
                last_updated=datetime.now(),
            )
        
        recent_metrics = self.metrics_history[-5:]  # Last 5 metrics
        
        # Calculate health score
        health_score = self._calculate_health_score(recent_metrics)
        
        # Determine overall health
        if health_score >= 0.8:
            overall_health = "healthy"
        elif health_score >= 0.6:
            overall_health = "warning"
        else:
            overall_health = "critical"
        
        # Identify issues
        issues = self._identify_health_issues(recent_metrics)
        
        # Generate recommendations
        recommendations = self._generate_health_recommendations(health_score, issues)
        
        return SystemHealth(
            overall_health=overall_health,
            health_score=health_score,
            issues=issues,
            recommendations=recommendations,
            last_updated=datetime.now(),
        )

    def get_resource_utilization(self, resource_name: str) -> ResourceUtilization:
        """Get resource utilization metrics."""
        if not self.metrics_history:
            return ResourceUtilization(
                resource_name=resource_name,
                current_utilization=0.0,
                peak_utilization=0.0,
                average_utilization=0.0,
                utilization_trend="stable",
                efficiency_score=0.0,
            )
        
        # Get values for resource
        if resource_name == "cpu":
            values = [m.cpu_usage for m in self.metrics_history]
        elif resource_name == "memory":
            values = [m.memory_usage for m in self.metrics_history]
        else:
            values = [m.disk_io for m in self.metrics_history]
        
        if not values:
            return ResourceUtilization(
                resource_name=resource_name,
                current_utilization=0.0,
                peak_utilization=0.0,
                average_utilization=0.0,
                utilization_trend="stable",
                efficiency_score=0.0,
            )
        
        current_utilization = values[-1] if values else 0.0
        peak_utilization = max(values) if values else 0.0
        average_utilization = statistics.mean(values) if values else 0.0
        utilization_trend = self._determine_trend(values)
        efficiency_score = self._calculate_efficiency_score(values)
        
        return ResourceUtilization(
            resource_name=resource_name,
            current_utilization=current_utilization,
            peak_utilization=peak_utilization,
            average_utilization=average_utilization,
            utilization_trend=utilization_trend,
            efficiency_score=efficiency_score,
        )

    def _get_recent_metrics(self, time_horizon: timedelta) -> List[PerformanceMetrics]:
        """Get recent metrics within time horizon."""
        cutoff_time = datetime.now() - time_horizon
        return [m for m in self.metrics_history if m.timestamp >= cutoff_time]

    def _calculate_trend_prediction(self, values: List[float]) -> float:
        """Calculate trend-based prediction."""
        if len(values) < 2:
            return values[0] if values else 0.0
        
        # Simple linear trend
        x_values = list(range(len(values)))
        slope = self._calculate_slope(x_values, values)
        
        # Predict next value
        next_x = len(values)
        predicted_value = values[-1] + slope
        
        return max(0.0, min(100.0, predicted_value))  # Clamp between 0 and 100

    def _calculate_slope(self, x_values: List[int], y_values: List[float]) -> float:
        """Calculate slope of linear regression."""
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0.0
        
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        return slope

    def _calculate_confidence(self, values: List[float]) -> float:
        """Calculate prediction confidence."""
        if len(values) < 2:
            return 0.5
        
        # Calculate coefficient of variation
        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values) if len(values) > 1 else 0.0
        
        if mean_val == 0:
            return 0.5
        
        cv = std_val / mean_val
        confidence = max(0.0, min(1.0, 1.0 - cv))
        return confidence

    def _determine_trend(self, values: List[float]) -> str:
        """Determine trend direction."""
        if len(values) < 2:
            return "stable"
        
        slope = self._calculate_slope(list(range(len(values))), values)
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"

    def _calculate_anomaly_score(self, values: List[float]) -> float:
        """Calculate anomaly score for values."""
        if len(values) < 3:
            return 0.0
        
        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values)
        
        if std_val == 0:
            return 0.0
        
        # Calculate z-score for last value
        last_value = values[-1]
        z_score = abs((last_value - mean_val) / std_val)
        
        # Convert to anomaly score (0-1)
        anomaly_score = min(1.0, z_score / 3.0)  # 3-sigma rule
        return anomaly_score

    def _check_metric_anomaly(self, metric_name: str, values: List[float]) -> AnomalyDetection:
        """Check for anomalies in a specific metric."""
        anomaly_score = self._calculate_anomaly_score(values)
        
        if anomaly_score < self.anomaly_threshold:
            return None
        
        # Determine severity
        if anomaly_score >= 0.9:
            severity = "critical"
        elif anomaly_score >= 0.7:
            severity = "high"
        elif anomaly_score >= 0.5:
            severity = "medium"
        else:
            severity = "low"
        
        # Generate description and action
        description = f"Anomaly detected in {metric_name} with score {anomaly_score:.2f}"
        suggested_action = self._generate_anomaly_action(metric_name, severity)
        
        return AnomalyDetection(
            metric_name=metric_name,
            anomaly_score=anomaly_score,
            severity=severity,
            detected_at=datetime.now(),
            description=description,
            suggested_action=suggested_action,
        )

    def _create_default_prediction(self, metric_name: str, time_horizon: timedelta) -> PredictionResult:
        """Create default prediction when no data available."""
        return PredictionResult(
            metric_name=metric_name,
            predicted_value=50.0,  # Default 50%
            confidence=0.0,
            time_horizon=time_horizon,
            trend="stable",
            anomaly_score=0.0,
            recommendations=["Collect more data for accurate predictions"],
        )

    def _create_default_capacity_forecast(self, resource_type: str) -> CapacityForecast:
        """Create default capacity forecast when no data available."""
        return CapacityForecast(
            resource_type=resource_type,
            current_usage=0.0,
            predicted_usage=50.0,
            capacity_limit=100.0,
            utilization_percentage=50.0,
            time_to_limit=timedelta(days=365),
            scaling_recommendation="Monitor resource usage",
        )

    def _calculate_time_to_limit(self, current: float, predicted: float, limit: float) -> timedelta:
        """Calculate time to reach capacity limit."""
        if predicted <= current:
            return timedelta(days=365)
        
        # Simple linear projection
        rate = (predicted - current) / 24  # Per hour rate
        if rate <= 0:
            return timedelta(days=365)
        
        time_to_limit = (limit - current) / rate
        return timedelta(hours=max(1, min(8760, time_to_limit)))  # Clamp between 1 hour and 1 year

    def _generate_scaling_recommendation(self, utilization_percentage: float) -> str:
        """Generate scaling recommendation based on utilization."""
        if utilization_percentage >= 90:
            return "Scale up immediately"
        elif utilization_percentage >= 75:
            return "Consider scaling up"
        elif utilization_percentage >= 50:
            return "Monitor closely"
        else:
            return "Current capacity sufficient"

    def _calculate_health_score(self, metrics: List[PerformanceMetrics]) -> float:
        """Calculate overall health score."""
        if not metrics:
            return 0.0
        
        scores = []
        
        # CPU health score
        cpu_values = [m.cpu_usage for m in metrics]
        if cpu_values:
            avg_cpu = statistics.mean(cpu_values)
            cpu_score = max(0.0, 1.0 - (avg_cpu / 100.0))
            scores.append(cpu_score)
        
        # Memory health score
        memory_values = [m.memory_usage for m in metrics]
        if memory_values:
            avg_memory = statistics.mean(memory_values)
            memory_score = max(0.0, 1.0 - (avg_memory / 100.0))
            scores.append(memory_score)
        
        # Response time health score
        response_values = [m.response_time for m in metrics]
        if response_values:
            avg_response = statistics.mean(response_values)
            response_score = max(0.0, 1.0 - (avg_response / 1000.0))  # Assume 1000ms is bad
            scores.append(response_score)
        
        return statistics.mean(scores) if scores else 0.0

    def _identify_health_issues(self, metrics: List[PerformanceMetrics]) -> List[str]:
        """Identify health issues from metrics."""
        issues = []
        
        if not metrics:
            return ["No metrics available"]
        
        # Check CPU issues
        cpu_values = [m.cpu_usage for m in metrics]
        if cpu_values and statistics.mean(cpu_values) > 80:
            issues.append("High CPU usage")
        
        # Check memory issues
        memory_values = [m.memory_usage for m in metrics]
        if memory_values and statistics.mean(memory_values) > 80:
            issues.append("High memory usage")
        
        # Check response time issues
        response_values = [m.response_time for m in metrics]
        if response_values and statistics.mean(response_values) > 500:
            issues.append("Slow response times")
        
        return issues

    def _generate_health_recommendations(self, health_score: float, issues: List[str]) -> List[str]:
        """Generate health recommendations."""
        recommendations = []
        
        if health_score < 0.6:
            recommendations.append("System health is critical - immediate attention required")
        
        if "High CPU usage" in issues:
            recommendations.append("Consider CPU optimization or scaling")
        
        if "High memory usage" in issues:
            recommendations.append("Review memory usage and consider optimization")
        
        if "Slow response times" in issues:
            recommendations.append("Investigate performance bottlenecks")
        
        if not recommendations:
            recommendations.append("System is healthy - continue monitoring")
        
        return recommendations

    def _calculate_efficiency_score(self, values: List[float]) -> float:
        """Calculate efficiency score for resource utilization."""
        if not values:
            return 0.0
        
        # Efficiency is higher when utilization is moderate (not too low, not too high)
        avg_utilization = statistics.mean(values)
        
        # Optimal range is 60-80%
        if 60 <= avg_utilization <= 80:
            return 1.0
        elif 40 <= avg_utilization < 60 or 80 < avg_utilization <= 90:
            return 0.7
        else:
            return 0.3

    def _generate_cpu_recommendations(self, predicted_value: float) -> List[str]:
        """Generate CPU-specific recommendations."""
        if predicted_value > 90:
            return ["CPU usage critical - scale up immediately"]
        elif predicted_value > 75:
            return ["High CPU usage predicted - consider scaling"]
        else:
            return ["CPU usage within acceptable range"]

    def _generate_memory_recommendations(self, predicted_value: float) -> List[str]:
        """Generate memory-specific recommendations."""
        if predicted_value > 90:
            return ["Memory usage critical - scale up immediately"]
        elif predicted_value > 75:
            return ["High memory usage predicted - consider scaling"]
        else:
            return ["Memory usage within acceptable range"]

    def _generate_response_time_recommendations(self, predicted_value: float) -> List[str]:
        """Generate response time-specific recommendations."""
        if predicted_value > 1000:
            return ["Response time critical - investigate bottlenecks"]
        elif predicted_value > 500:
            return ["Slow response times predicted - optimize performance"]
        else:
            return ["Response times within acceptable range"]

    def _generate_anomaly_action(self, metric_name: str, severity: str) -> str:
        """Generate action for anomaly detection."""
        if severity == "critical":
            return f"Immediate investigation required for {metric_name}"
        elif severity == "high":
            return f"Priority investigation for {metric_name}"
        elif severity == "medium":
            return f"Monitor {metric_name} closely"
        else:
            return f"Continue monitoring {metric_name}"

