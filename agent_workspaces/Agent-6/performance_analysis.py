"""System performance analysis utilities."""

from datetime import datetime
from typing import Any, Dict
import logging

from metric_collection import MetricCollector
from constants import (
    CPU_USAGE_THRESHOLD,
    MEMORY_USAGE_THRESHOLD,
    DISK_USAGE_THRESHOLD,
    NETWORK_LATENCY_THRESHOLD,
)


class PerformanceAnalyzer:
    """Analyze collected metrics and evaluate system state."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__ + ".PerformanceAnalyzer")

    def analyze(self, collector: MetricCollector) -> Dict[str, Any]:
        """Collect metrics and compute analysis details."""
        metrics = collector.collect_all()
        metrics["performance_patterns"] = self._analyze_performance_patterns()
        metrics["baseline_established"] = True
        metrics["analysis_timestamp"] = datetime.now().isoformat()
        metrics["thresholds"] = {
            "cpu": CPU_USAGE_THRESHOLD,
            "memory": MEMORY_USAGE_THRESHOLD,
            "disk": DISK_USAGE_THRESHOLD,
            "network_latency": NETWORK_LATENCY_THRESHOLD,
        }
        self.logger.debug("Performance analysis: %s", metrics)
        return metrics

    def _analyze_performance_patterns(self) -> Dict[str, Any]:
        """Return simple static descriptions of performance patterns."""
        return {
            "cpu_patterns": "Variable usage with peaks during operations",
            "memory_patterns": "Consistent usage with gradual growth",
            "disk_patterns": "Burst I/O during file operations",
            "network_patterns": "Low baseline with activity spikes",
        }
