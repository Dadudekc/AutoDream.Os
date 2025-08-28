#!/usr/bin/env python3
"""Performance Optimization Toolkit orchestrator.

This module wires together metric collection, optimisation algorithms and
report generation into a single cohesive workflow.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

# Ensure local modules are importable despite the hyphen in the parent folder
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from metric_collection import MetricCollector
from optimization_algorithms import OptimizationAlgorithms
from report_generation import ReportGenerator


class PerformanceOptimizationToolkit:
    """High level orchestrator for the performance optimisation workflow."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__ + ".PerformanceOptimizationToolkit")
        self.collector = MetricCollector()
        self.optimizer = OptimizationAlgorithms()
        self.reporter = ReportGenerator()
        self.optimization_results: Dict[str, Any] = {}

    # --------------------------------------------------------------------- run
    def execute_comprehensive_optimization(self) -> Dict[str, Any]:
        """Run all optimisation phases and return the raw results."""
        self.logger.info("🚀 Executing comprehensive performance optimisation")

        phases: Dict[str, Dict[str, Any]] = {}

        analysis = self.optimizer.analyze_current_performance(self.collector)
        phases["analysis"] = analysis

        strategies = self.optimizer.develop_optimization_strategies(analysis)
        phases["strategy"] = strategies

        implementation = self.optimizer.implement_enhancements(strategies)
        phases["implementation"] = implementation

        testing = self.optimizer.test_performance_improvements(implementation)
        phases["testing"] = testing

        validation = self.optimizer.validate_optimizations(testing)
        phases["validation"] = validation

        improvements = self.optimizer.calculate_overall_improvements(phases)
        recommendations = self.optimizer.generate_optimization_recommendations(improvements)

        self.optimization_results = {
            "timestamp": datetime.now().isoformat(),
            "phases": phases,
            "overall_improvements": improvements,
            "recommendations": recommendations,
        }
        return self.optimization_results

    # ----------------------------------------------------------------- reporting
    def generate_optimization_report(self) -> Dict[str, Any]:
        """Return a consolidated optimisation report."""
        if not self.optimization_results:
            self.execute_comprehensive_optimization()
        report = self.reporter.generate(self.optimization_results)
        return report


if __name__ == "__main__":  # pragma: no cover - manual execution helper
    logging.basicConfig(level=logging.INFO)
    toolkit = PerformanceOptimizationToolkit()
    toolkit.execute_comprehensive_optimization()
    final_report = toolkit.generate_optimization_report()
    print(final_report)
