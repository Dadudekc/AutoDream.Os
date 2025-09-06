#!/usr/bin/env python3
"""
Anomaly Detection Engine - KISS Compliant
=========================================

Simple anomaly detection for analytics.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import statistics
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AnomalyDetectionEngine:
    """Simple anomaly detection engine."""

    def __init__(self, config=None):
        """Initialize anomaly detection engine."""
        self.config = config or {}
        self.thresholds = {"z_score": 2.0, "performance": 0.5, "frequency": 0.05}
        self.logger = logger

    def detect_anomalies(self, data: List[float]) -> List[Dict[str, Any]]:
        """Detect anomalies in data."""
        if not data or len(data) < 3:
            return []

        anomalies = []

        # Statistical anomaly detection
        stat_anomalies = self._detect_statistical_anomalies(data)
        anomalies.extend(stat_anomalies)

        # Performance anomaly detection
        perf_anomalies = self._detect_performance_anomalies(data)
        anomalies.extend(perf_anomalies)

        return anomalies

    def _detect_statistical_anomalies(self, data: List[float]) -> List[Dict[str, Any]]:
        """Detect statistical anomalies using z-score."""
        if len(data) < 3:
            return []

        try:
            mean = statistics.mean(data)
            stdev = statistics.stdev(data)

            if stdev == 0:
                return []

            anomalies = []
            for i, value in enumerate(data):
                z_score = abs((value - mean) / stdev)
                if z_score > self.thresholds["z_score"]:
                    anomalies.append(
                        {
                            "index": i,
                            "value": value,
                            "z_score": z_score,
                            "type": "statistical",
                            "severity": "high" if z_score > 3.0 else "medium",
                        }
                    )

            return anomalies
        except Exception as e:
            self.logger.error(f"Error in statistical anomaly detection: {e}")
            return []

    def _detect_performance_anomalies(self, data: List[float]) -> List[Dict[str, Any]]:
        """Detect performance anomalies."""
        if len(data) < 2:
            return []

        anomalies = []
        threshold = self.thresholds["performance"]

        for i in range(1, len(data)):
            change = abs(data[i] - data[i - 1]) / data[i - 1] if data[i - 1] != 0 else 0
            if change > threshold:
                anomalies.append(
                    {
                        "index": i,
                        "value": data[i],
                        "change": change,
                        "type": "performance",
                        "severity": "high" if change > threshold * 2 else "medium",
                    }
                )

        return anomalies

    def get_anomaly_summary(self, anomalies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary of anomalies."""
        if not anomalies:
            return {"total": 0, "by_type": {}, "by_severity": {}}

        by_type = {}
        by_severity = {}

        for anomaly in anomalies:
            anomaly_type = anomaly.get("type", "unknown")
            severity = anomaly.get("severity", "unknown")

            by_type[anomaly_type] = by_type.get(anomaly_type, 0) + 1
            by_severity[severity] = by_severity.get(severity, 0) + 1

        return {
            "total": len(anomalies),
            "by_type": by_type,
            "by_severity": by_severity,
            "timestamp": datetime.now().isoformat(),
        }


__all__ = ["AnomalyDetectionEngine"]
