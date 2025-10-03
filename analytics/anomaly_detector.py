"""
Predictive Anomaly Detection - V2 Compliant
===========================================

Anomaly detection functionality for predictive analytics.
V2 Compliance: ≤400 lines, ≤10 functions, single responsibility
"""

import statistics
from datetime import datetime

from .predictive_models import AnomalyDetection, PerformanceMetrics


class AnomalyDetector:
    """Anomaly detection functionality."""

    def __init__(self, threshold: float = 0.8):
        """Initialize anomaly detector."""
        self.anomaly_threshold = threshold

    def detect_anomalies(self, metrics_history: list[PerformanceMetrics]) -> list[AnomalyDetection]:
        """Detect anomalies in performance metrics."""
        if len(metrics_history) < 10:
            return []

        anomalies = []

        # Check CPU anomalies
        cpu_values = [m.cpu_usage for m in metrics_history]
        cpu_anomaly = self._check_metric_anomaly("cpu_usage", cpu_values)
        if cpu_anomaly:
            anomalies.append(cpu_anomaly)

        # Check memory anomalies
        memory_values = [m.memory_usage for m in metrics_history]
        memory_anomaly = self._check_metric_anomaly("memory_usage", memory_values)
        if memory_anomaly:
            anomalies.append(memory_anomaly)

        # Check response time anomalies
        response_values = [m.response_time for m in metrics_history]
        response_anomaly = self._check_metric_anomaly("response_time", response_values)
        if response_anomaly:
            anomalies.append(response_anomaly)

        return anomalies

    def _check_metric_anomaly(self, metric_name: str, values: list[float]) -> AnomalyDetection:
        """Check for anomalies in a specific metric."""
        if len(values) < 5:
            return None

        anomaly_score = self._calculate_anomaly_score(values)

        if anomaly_score > self.anomaly_threshold:
            severity = self._determine_severity(anomaly_score)
            action = self._generate_anomaly_action(metric_name, severity)

            return AnomalyDetection(
                metric_name=metric_name,
                anomaly_score=anomaly_score,
                severity=severity,
                detected_at=datetime.now(),
                action_required=action,
                description=f"Anomaly detected in {metric_name}",
            )

        return None

    def _calculate_anomaly_score(self, values: list[float]) -> float:
        """Calculate anomaly score for a set of values."""
        if len(values) < 3:
            return 0.0

        # Use statistical methods to detect anomalies
        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values) if len(values) > 1 else 0

        if std_val == 0:
            return 0.0

        # Check for outliers using z-score
        recent_values = values[-5:]  # Last 5 values
        max_z_score = 0

        for value in recent_values:
            z_score = abs((value - mean_val) / std_val)
            max_z_score = max(max_z_score, z_score)

        # Normalize to 0-1 range
        anomaly_score = min(1.0, max_z_score / 3.0)

        return anomaly_score

    def _determine_severity(self, anomaly_score: float) -> str:
        """Determine severity level based on anomaly score."""
        if anomaly_score > 0.9:
            return "critical"
        elif anomaly_score > 0.7:
            return "high"
        elif anomaly_score > 0.5:
            return "medium"
        else:
            return "low"

    def _generate_anomaly_action(self, metric_name: str, severity: str) -> str:
        """Generate recommended action for anomaly."""
        if severity == "critical":
            return f"Immediate investigation required for {metric_name}"
        elif severity == "high":
            return f"Priority investigation needed for {metric_name}"
        elif severity == "medium":
            return f"Monitor {metric_name} closely"
        else:
            return f"Continue monitoring {metric_name}"

    def update_threshold(self, new_threshold: float) -> None:
        """Update anomaly detection threshold."""
        self.anomaly_threshold = max(0.0, min(1.0, new_threshold))

    def get_threshold(self) -> float:
        """Get current anomaly detection threshold."""
        return self.anomaly_threshold
