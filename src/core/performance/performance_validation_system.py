#!/usr/bin/env python3
"""
Performance Validation System - V2 Core Performance Testing & Optimization

This is the refactored main system that orchestrates performance validation.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

from .performance_types import (
    PerformanceBenchmark, SystemPerformanceReport, BenchmarkTargets, 
    PerformanceThresholds, PerformanceLevel, OptimizationTarget
)
from .benchmark_runner import BenchmarkRunner
from .performance_calculator import PerformanceCalculator
from .report_generator import ReportGenerator


class PerformanceValidationSystem:
    """
    Refactored performance validation and optimization system
    
    Responsibilities:
    - Orchestrate performance benchmarking
    - Coordinate between specialized components
    - Provide unified interface for performance testing
    """

    def __init__(self):
        # Initialize components
        self.targets = BenchmarkTargets()
        self.thresholds = PerformanceThresholds()
        self.benchmark_runner = BenchmarkRunner(self.targets)
        self.performance_calculator = PerformanceCalculator(self.thresholds)
        self.report_generator = ReportGenerator()
        
        # Set logger reference
        self.report_generator.logger = logging.getLogger(f"{__name__}.ReportGenerator")
        
        # Performance data storage
        self.benchmarks: Dict[str, PerformanceBenchmark] = {}
        self.performance_reports: List[SystemPerformanceReport] = []
        self.optimization_history: List[Dict[str, Any]] = []
        
        self.logger = logging.getLogger(f"{__name__}.PerformanceValidationSystem")

    def run_comprehensive_benchmark(self) -> str:
        """Run comprehensive performance benchmark suite"""
        try:
            benchmark_id = str(uuid.uuid4())
            start_time = datetime.now()
            
            self.logger.info(f"Starting comprehensive benchmark: {benchmark_id}")
            
            # Run all benchmark types using the benchmark runner
            benchmark_results = []
            
            # Response time benchmark
            response_benchmark = self.benchmark_runner.run_response_time_benchmark()
            benchmark_results.append(response_benchmark)
            
            # Throughput benchmark
            throughput_benchmark = self.benchmark_runner.run_throughput_benchmark()
            benchmark_results.append(throughput_benchmark)
            
            # Scalability benchmark
            scalability_benchmark = self.benchmark_runner.run_scalability_benchmark()
            benchmark_results.append(scalability_benchmark)
            
            # Store benchmarks
            for benchmark in benchmark_results:
                self.benchmarks[benchmark.benchmark_id] = benchmark
            
            # Calculate overall performance using the calculator
            overall_level = self.performance_calculator.calculate_overall_performance_level(benchmark_results)
            enterprise_score = self.performance_calculator.calculate_enterprise_readiness_score(benchmark_results)
            optimization_opportunities = self.performance_calculator.identify_optimization_opportunities(benchmark_results)
            
            # Generate report using the report generator
            report = self.report_generator.generate_performance_report(
                benchmark_results, overall_level, enterprise_score, optimization_opportunities
            )
            
            # Store report
            self.performance_reports.append(report)
            
            end_time = datetime.now()
            total_duration = (end_time - start_time).total_seconds()
            
            self.logger.info(f"Benchmark completed in {total_duration:.2f}s")
            self.logger.info(f"Overall performance: {overall_level.value}")
            self.logger.info(f"Enterprise readiness: {enterprise_score:.1%}")
            
            return report.report_id
            
        except Exception as e:
            self.logger.error(f"Comprehensive benchmark failed: {e}")
            raise

    def run_smoke_test(self) -> bool:
        """Run quick smoke test for basic performance validation"""
        try:
            self.logger.info("Running performance smoke test")
            
            # Run just response time test for quick validation
            benchmark = self.benchmark_runner.run_response_time_benchmark()
            
            # Check if basic performance is acceptable
            if benchmark.performance_level in [PerformanceLevel.ENTERPRISE_READY, PerformanceLevel.PRODUCTION_READY]:
                self.logger.info("Smoke test passed - basic performance acceptable")
                return True
            else:
                self.logger.warning("Smoke test failed - performance below acceptable threshold")
                return False
                
        except Exception as e:
            self.logger.error(f"Smoke test failed with error: {e}")
            return False

    def get_latest_performance_report(self) -> Optional[SystemPerformanceReport]:
        """Get the most recent performance report"""
        if not self.performance_reports:
            return None
        return self.performance_reports[-1]

    def get_benchmark_summary(self) -> Dict[str, Any]:
        """Get summary of all benchmarks"""
        return self.report_generator.generate_benchmark_summary(list(self.benchmarks.values()))

    def get_performance_history(self) -> List[SystemPerformanceReport]:
        """Get performance history"""
        return self.performance_reports.copy()

    def clear_history(self) -> None:
        """Clear performance history"""
        self.benchmarks.clear()
        self.performance_reports.clear()
        self.optimization_history.clear()
        self.logger.info("Performance history cleared")

    def export_report(self, report_id: str, format_type: str = "text") -> str:
        """Export performance report in specified format"""
        try:
            # Find report
            report = None
            for r in self.performance_reports:
                if r.report_id == report_id:
                    report = r
                    break
            
            if not report:
                raise ValueError(f"Report {report_id} not found")
            
            # Export based on format
            if format_type == "text":
                return self.report_generator.format_report_for_display(report)
            elif format_type == "json":
                import json
                return json.dumps(report.__dict__, default=str, indent=2)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
                
        except Exception as e:
            self.logger.error(f"Failed to export report: {e}")
            raise


