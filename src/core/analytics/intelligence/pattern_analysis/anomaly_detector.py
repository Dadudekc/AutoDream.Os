"""
Anomaly Detector - V2 Compliance Module
======================================

Anomaly detection functionality for analytics.

V2 Compliance: < 300 lines, single responsibility, anomaly detection.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import statistics
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Anomaly detection functionality."""

    def __init__(self):
        """Initialize anomaly detector."""
        self.logger = logger

    def detect_anomalies(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies in data."""
        try:
            if not data:
                return []

            # Extract numeric values for anomaly detection
            numeric_values = []
            for item in data:
                for value in item.values():
                    if isinstance(value, (int, float)):
                        numeric_values.append(value)

            if len(numeric_values) < 3:
                return []

            # Detect anomalies using statistical methods
            anomalies = self._detect_statistical_anomalies(numeric_values)

            return anomalies
        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {e}")
            return []

    def _detect_statistical_anomalies(
        self, values: List[float]
    ) -> List[Dict[str, Any]]:
        """Detect anomalies using statistical methods."""
        try:
            if len(values) < 3:
                return []

            # Calculate mean and standard deviation
            mean_val = statistics.mean(values)
            stdev_val = statistics.stdev(values) if len(values) > 1 else 0

            if stdev_val == 0:
                return []

            anomalies = []

            # Find values that are more than 2 standard deviations from mean
            threshold = 2 * stdev_val
            for i, value in enumerate(values):
                if abs(value - mean_val) > threshold:
                    anomalies.append(
                        {
                            "index": i,
                            "value": value,
                            "deviation": round(abs(value - mean_val), 3),
                            "z_score": round((value - mean_val) / stdev_val, 3),
                        }
                    )

            return anomalies[:5]  # Limit to 5 anomalies
        except Exception as e:
            self.logger.error(f"Error detecting statistical anomalies: {e}")
            return []

    def detect_outliers(
        self, values: List[float], method: str = "iqr"
    ) -> List[Dict[str, Any]]:
        """Detect outliers using different methods."""
        try:
            if len(values) < 4:
                return []

            if method == "iqr":
                return self._detect_outliers_iqr(values)
            elif method == "zscore":
                return self._detect_outliers_zscore(values)
            else:
                return self._detect_outliers_iqr(values)
        except Exception as e:
            self.logger.error(f"Error detecting outliers: {e}")
            return []

    def _detect_outliers_iqr(self, values: List[float]) -> List[Dict[str, Any]]:
        """Detect outliers using IQR method."""
        try:
            sorted_values = sorted(values)
            n = len(sorted_values)

            # Calculate quartiles
            q1_idx = n // 4
            q3_idx = 3 * n // 4

            q1 = sorted_values[q1_idx]
            q3 = sorted_values[q3_idx]

            # Calculate IQR
            iqr = q3 - q1

            # Define outlier bounds
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = []
            for i, value in enumerate(values):
                if value < lower_bound or value > upper_bound:
                    outliers.append(
                        {
                            "index": i,
                            "value": value,
                            "lower_bound": lower_bound,
                            "upper_bound": upper_bound,
                        }
                    )

            return outliers
        except Exception as e:
            self.logger.error(f"Error detecting IQR outliers: {e}")
            return []

    def _detect_outliers_zscore(self, values: List[float]) -> List[Dict[str, Any]]:
        """Detect outliers using Z-score method."""
        try:
            if len(values) < 3:
                return []

            mean_val = statistics.mean(values)
            stdev_val = statistics.stdev(values)

            if stdev_val == 0:
                return []

            outliers = []
            threshold = 2.5  # Z-score threshold

            for i, value in enumerate(values):
                z_score = abs((value - mean_val) / stdev_val)
                if z_score > threshold:
                    outliers.append(
                        {
                            "index": i,
                            "value": value,
                            "z_score": round(z_score, 3),
                            "threshold": threshold,
                        }
                    )

            return outliers
        except Exception as e:
            self.logger.error(f"Error detecting Z-score outliers: {e}")
            return []
