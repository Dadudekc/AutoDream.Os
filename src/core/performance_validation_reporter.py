"""Reporting utilities for the Performance Validation System."""
import logging
from typing import List

from .performance.metrics.collector import PerformanceBenchmark
from .performance_validation_core import PerformanceValidationCore


class PerformanceValidationReporter:
    """Generates reports and triggers alerts for benchmark runs."""

    def __init__(self, core: PerformanceValidationCore) -> None:
        self.core = core
        self.logger = logging.getLogger(
            f"{__name__}.PerformanceValidationReporter"
        )

    def generate_report(
        self, benchmarks: List[PerformanceBenchmark]
    ):
        """Create performance report and check alerts."""
        overall_level = self.core.validation_rules.calculate_overall_performance_level(
            benchmarks
        )

        all_recommendations = []
        for benchmark in benchmarks:
            recs = self.core.validation_rules.generate_optimization_recommendations(
                benchmark
            )
            benchmark.optimization_recommendations = recs
            all_recommendations.extend(recs)
            self.core.alert_manager.check_benchmark_for_alerts(benchmark)

        unique_recs = []
        seen = set()
        for rec in all_recommendations:
            if rec not in seen:
                unique_recs.append(rec)
                seen.add(rec)

        report = self.core.report_generator.generate_performance_report(
            benchmarks, overall_level, unique_recs
        )
        return report
