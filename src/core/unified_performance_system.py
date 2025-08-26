#!/usr/bin/env python3
"""Unified Performance System - Consolidated Orchestrator."""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import Any, Dict

from .performance.monitoring.monitoring_manager import MonitoringManager
from .performance.performance_benchmarking import PerformanceBenchmarkingManager
from .performance.performance_reporting import PerformanceReportingManager


logger = logging.getLogger(__name__)


class UnifiedPerformanceSystem:
    """Unified orchestrator satisfying legacy and V2 interfaces."""

    def __init__(self) -> None:
        self.monitoring = MonitoringManager()
        self.benchmarking = PerformanceBenchmarkingManager()
        self.reporting = PerformanceReportingManager()
        self.reporting.start_reporting()
        self.is_running = False
        logger.info("Unified Performance System initialized")

    # ------------------------------------------------------------------
    # Lifecycle management
    # ------------------------------------------------------------------
    def start_system(self) -> bool:
        """Start performance monitoring."""
        self.is_running = True
        self.monitoring.collect_system_metrics()
        return True

    def stop_system(self) -> bool:
        """Stop performance system."""
        self.is_running = False
        return True

    # ------------------------------------------------------------------
    # Benchmarking and reporting
    # ------------------------------------------------------------------
    def run_benchmark(self, benchmark_type: str = "cpu", duration: int = 0) -> Any:
        self.benchmarking.start_benchmarking()
        result = self.benchmarking.run_benchmark(benchmark_type, {"duration": duration})
        self.benchmarking.stop_benchmarking()
        return result

    def generate_report(self) -> Dict[str, Any]:
        metrics = []
        validation_results = []
        benchmarks = self.benchmarking.benchmark_history
        report = self.reporting.generate_performance_report(
            metrics, validation_results, benchmarks
        )
        return asdict(report)

    # ------------------------------------------------------------------
    # Monitoring helpers
    # ------------------------------------------------------------------
    def add_metric(self, name: str, value: Any) -> None:
        self.monitoring.add_metric(name, value)

    def get_active_alerts(self) -> list:
        return self.monitoring.get_alerts()

    def clear_alerts(self) -> None:
        self.monitoring.clear_alerts()

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------
    def get_system_status(self) -> Dict[str, Any]:
        return {
            "system_status": "running" if self.is_running else "stopped",
            "total_benchmarks": len(self.benchmarking.benchmark_history),
            "active_alerts": len(self.monitoring.get_alerts()),
        }

    def shutdown(self) -> bool:
        self.clear_alerts()
        return self.stop_system()


def create_performance_system() -> UnifiedPerformanceSystem:
    return UnifiedPerformanceSystem()


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    sys = UnifiedPerformanceSystem()
    sys.start_system()
    res = sys.run_benchmark("cpu", duration=0)
    print("benchmark", res.success)
    print("report", sys.generate_report())
    print("status", sys.get_system_status())
    sys.stop_system()

