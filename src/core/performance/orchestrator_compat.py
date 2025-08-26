#!/usr/bin/env python3
"""Legacy compatibility mixin for :class:`UnifiedPerformanceOrchestrator`.

Provides deprecated methods that wrap newer orchestrator APIs to maintain
backward compatibility with existing callers.
"""

from __future__ import annotations

import warnings
from typing import Any, Dict, List, Optional

from .performance_models import BenchmarkResult, SystemPerformanceReport


class OrchestratorCompatibilityMixin:
    """Deprecated wrappers exposing the legacy interface."""

    def run_benchmarks(self, benchmark_types: Optional[List[str]] = None) -> List[BenchmarkResult]:
        """Run multiple benchmarks sequentially.

        This method mirrors legacy behaviour and is maintained for backward
        compatibility. It emits a ``DeprecationWarning`` advising callers to
        switch to :meth:`run_performance_benchmark`.
        """
        warnings.warn(
            "run_benchmarks() is deprecated; use run_performance_benchmark() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        results: List[BenchmarkResult] = []
        types = benchmark_types or list(self.performance_core.benchmarking_manager.benchmark_configs.keys())
        for b_type in types:
            try:
                results.append(self.run_performance_benchmark(b_type))
            except Exception as exc:  # noqa: BLE001
                self.logger.error(f"Failed to run benchmark '{b_type}': {exc}")
        return results

    def validate_performance(self, rules: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """Validate collected metrics against configured rules.

        The ``rules`` argument is accepted for compatibility but ignored; rules
        should be configured directly on the validation manager. A
        ``DeprecationWarning`` is emitted to guide migration.
        """
        warnings.warn(
            "validate_performance() is deprecated; use validation_manager.validate_metrics() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        metrics = self.performance_core.monitoring_manager.collect_metrics()
        return self.performance_core.validation_manager.validate_metrics(metrics)

    def generate_report(self, report_type: str = "comprehensive") -> SystemPerformanceReport:
        """Generate a performance report.

        ``report_type`` is retained for backward compatibility and has no
        effect. A ``DeprecationWarning`` advises use of the reporting manager
        directly.
        """
        warnings.warn(
            "generate_report() is deprecated; use reporting_manager.generate_performance_report() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        metrics = self.performance_core.monitoring_manager.collect_metrics()
        validation_results = self.performance_core.validation_manager.validate_metrics(metrics)
        benchmark_results = self.run_benchmarks()
        return self.performance_core.reporting_manager.generate_performance_report(
            metrics, validation_results, benchmark_results
        )

    def start(self) -> bool:
        """Deprecated alias for :meth:`start_system`."""
        warnings.warn("start() is deprecated; use start_system()", DeprecationWarning, stacklevel=2)
        return self.start_system()

    def stop(self) -> bool:
        """Deprecated alias for :meth:`stop_system`."""
        warnings.warn("stop() is deprecated; use stop_system()", DeprecationWarning, stacklevel=2)
        return self.stop_system()

    def benchmark(self, types: Optional[List[str]] = None) -> List[BenchmarkResult]:
        """Deprecated alias for :meth:`run_benchmarks`."""
        warnings.warn("benchmark() is deprecated; use run_performance_benchmark()", DeprecationWarning, stacklevel=2)
        return self.run_benchmarks(types)

    def summary(self) -> Dict[str, Any]:
        """Deprecated alias for :meth:`get_performance_summary`."""
        warnings.warn("summary() is deprecated; use get_performance_summary()", DeprecationWarning, stacklevel=2)
        return self.get_performance_summary()

    def validate(self, rules: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """Deprecated alias for :meth:`validate_performance`."""
        warnings.warn("validate() is deprecated; use validate_performance()", DeprecationWarning, stacklevel=2)
        return self.validate_performance(rules)

    def report(self, report_type: str = "comprehensive") -> SystemPerformanceReport:
        """Deprecated alias for :meth:`generate_report`."""
        warnings.warn("report() is deprecated; use generate_report()", DeprecationWarning, stacklevel=2)
        return self.generate_report(report_type)

    def status(self) -> Dict[str, Any]:
        """Deprecated alias for :meth:`get_system_status`."""
        warnings.warn("status() is deprecated; use get_system_status()", DeprecationWarning, stacklevel=2)
        return self.get_system_status()
