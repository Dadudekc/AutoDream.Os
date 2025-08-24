#!/usr/bin/env python3
"""
Performance Validation Core - V2 Core Performance Testing & Optimization

Core performance validation system implementation.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import uuid

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import asdict

from .enums import BenchmarkType, PerformanceLevel, OptimizationTarget
from .data_models import PerformanceBenchmark, SystemPerformanceReport


class PerformanceValidationSystem:
    """
    Core performance validation and optimization system
    
    Single responsibility: Performance validation and benchmarking only.
    Follows V2 standards: OOP, SRP, clean production-grade code.
    """

    def __init__(self):
        """Initialize performance validation system"""
        self.benchmarks: Dict[str, PerformanceBenchmark] = {}
        self.performance_reports: List[SystemPerformanceReport] = []
        self.optimization_history: List[Dict[str, Any]] = []
        
        # Benchmark targets
        self.benchmark_targets = {
            BenchmarkType.RESPONSE_TIME: {"target": 100, "unit": "ms"},
            BenchmarkType.THROUGHPUT: {"target": 1000, "unit": "ops/sec"},
            BenchmarkType.SCALABILITY: {"target": 100, "unit": "concurrent_users"},
            BenchmarkType.RELIABILITY: {"target": 99.9, "unit": "%"},
            BenchmarkType.LATENCY: {"target": 50, "unit": "ms"},
        }
        
        # Performance thresholds
        self.performance_thresholds = {
            PerformanceLevel.ENTERPRISE_READY: 0.95,
            PerformanceLevel.PRODUCTION_READY: 0.85,
            PerformanceLevel.DEVELOPMENT_READY: 0.70,
            PerformanceLevel.NOT_READY: 0.0,
        }
        
        self.logger = logging.getLogger(f"{__name__}.PerformanceValidationSystem")
        self.logger.info("Performance validation system initialized")

    def run_benchmark(self, benchmark_type: BenchmarkType, test_name: str, 
                     metrics: Dict[str, float]) -> PerformanceBenchmark:
        """Run a single performance benchmark"""
        try:
            benchmark_id = str(uuid.uuid4())
            start_time = datetime.now()
            
            self.logger.info(f"Running {benchmark_type.value} benchmark: {test_name}")
            
            # Get target metrics for this benchmark type
            target_metrics = self._get_target_metrics(benchmark_type)
            
            # Calculate performance level
            performance_level = self._calculate_performance_level(metrics, target_metrics)
            
            # Generate optimization recommendations
            recommendations = self._generate_recommendations(metrics, target_metrics, performance_level)
            
            # Create benchmark result
            benchmark = PerformanceBenchmark(
                benchmark_id=benchmark_id,
                benchmark_type=benchmark_type,
                test_name=test_name,
                start_time=start_time.isoformat(),
                end_time=datetime.now().isoformat(),
                duration=(datetime.now() - start_time).total_seconds(),
                metrics=metrics,
                target_metrics=target_metrics,
                performance_level=performance_level,
                optimization_recommendations=recommendations
            )
            
            # Store benchmark
            self.benchmarks[benchmark_id] = benchmark
            
            self.logger.info(f"Benchmark completed: {benchmark_id}")
            return benchmark
            
        except Exception as e:
            self.logger.error(f"Benchmark failed: {e}")
            raise

    def generate_performance_report(self, benchmark_ids: List[str]) -> SystemPerformanceReport:
        """Generate comprehensive performance report from benchmarks"""
        try:
            # Get benchmarks
            benchmarks = [self.benchmarks[bid] for bid in benchmark_ids if bid in self.benchmarks]
            
            if not benchmarks:
                raise ValueError("No valid benchmark IDs provided")
            
            # Calculate overall performance level
            overall_level = self._calculate_overall_performance_level(benchmarks)
            
            # Calculate enterprise readiness score
            enterprise_score = self._calculate_enterprise_readiness_score(benchmarks)
            
            # Identify optimization opportunities
            optimization_opportunities = self._identify_optimization_opportunities(benchmarks)
            
            # Generate recommendations
            recommendations = self._generate_overall_recommendations(benchmarks, overall_level)
            
            # Create report
            report = SystemPerformanceReport(
                report_id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat(),
                overall_performance_level=overall_level,
                benchmark_results=benchmarks,
                optimization_opportunities=optimization_opportunities,
                enterprise_readiness_score=enterprise_score,
                recommendations=recommendations
            )
            
            # Store report
            self.performance_reports.append(report)
            
            self.logger.info(f"Performance report generated: {report.report_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            raise

    def _get_target_metrics(self, benchmark_type: BenchmarkType) -> Dict[str, float]:
        """Get target metrics for a benchmark type"""
        if benchmark_type == BenchmarkType.RESPONSE_TIME:
            return {"response_time": 100.0}
        elif benchmark_type == BenchmarkType.THROUGHPUT:
            return {"throughput": 1000.0}
        elif benchmark_type == BenchmarkType.SCALABILITY:
            return {"concurrent_users": 100.0}
        elif benchmark_type == BenchmarkType.RELIABILITY:
            return {"uptime": 99.9}
        elif benchmark_type == BenchmarkType.LATENCY:
            return {"latency": 50.0}
        else:
            return {}

    def _calculate_performance_level(self, metrics: Dict[str, float], 
                                   targets: Dict[str, float]) -> PerformanceLevel:
        """Calculate performance level based on metrics vs targets"""
        if not targets:
            return PerformanceLevel.NOT_READY
        
        # Calculate percentage of targets met
        met_targets = 0
        total_targets = len(targets)
        
        for metric_name, target_value in targets.items():
            actual_value = metrics.get(metric_name, 0)
            if metric_name == "uptime":  # Higher is better
                if actual_value >= target_value:
                    met_targets += 1
            else:  # Lower is better (response time, latency)
                if actual_value <= target_value:
                    met_targets += 1
        
        percentage_met = met_targets / total_targets if total_targets > 0 else 0.0
        
        # Determine performance level
        if percentage_met >= 0.95:
            return PerformanceLevel.ENTERPRISE_READY
        elif percentage_met >= 0.85:
            return PerformanceLevel.PRODUCTION_READY
        elif percentage_met >= 0.70:
            return PerformanceLevel.DEVELOPMENT_READY
        else:
            return PerformanceLevel.NOT_READY

    def _calculate_overall_performance_level(self, benchmarks: List[PerformanceBenchmark]) -> PerformanceLevel:
        """Calculate overall performance level from multiple benchmarks"""
        if not benchmarks:
            return PerformanceLevel.NOT_READY
        
        # Count benchmarks by performance level
        level_counts = {}
        for benchmark in benchmarks:
            level = benchmark.performance_level
            level_counts[level] = level_counts.get(level, 0) + 1
        
        # Determine overall level based on majority
        total_benchmarks = len(benchmarks)
        for level in [PerformanceLevel.ENTERPRISE_READY, PerformanceLevel.PRODUCTION_READY, 
                     PerformanceLevel.DEVELOPMENT_READY]:
            if level_counts.get(level, 0) / total_benchmarks >= 0.6:  # 60% threshold
                return level
        
        return PerformanceLevel.NOT_READY

    def _calculate_enterprise_readiness_score(self, benchmarks: List[PerformanceBenchmark]) -> float:
        """Calculate enterprise readiness score (0-100)"""
        if not benchmarks:
            return 0.0
        
        scores = [benchmark.get_performance_score() for benchmark in benchmarks]
        return sum(scores) / len(scores) if scores else 0.0

    def _identify_optimization_opportunities(self, benchmarks: List[PerformanceBenchmark]) -> List[OptimizationTarget]:
        """Identify optimization opportunities from benchmarks"""
        opportunities = set()
        
        for benchmark in benchmarks:
            if benchmark.performance_level in [PerformanceLevel.NOT_READY, PerformanceLevel.CRITICAL_ISSUES]:
                if benchmark.benchmark_type == BenchmarkType.RESPONSE_TIME:
                    opportunities.add(OptimizationTarget.RESPONSE_TIME_IMPROVEMENT)
                elif benchmark.benchmark_type == BenchmarkType.THROUGHPUT:
                    opportunities.add(OptimizationTarget.THROUGHPUT_INCREASE)
                elif benchmark.benchmark_type == BenchmarkType.SCALABILITY:
                    opportunities.add(OptimizationTarget.SCALABILITY_ENHANCEMENT)
                elif benchmark.benchmark_type == BenchmarkType.RELIABILITY:
                    opportunities.add(OptimizationTarget.RELIABILITY_IMPROVEMENT)
        
        return list(opportunities)

    def _generate_recommendations(self, metrics: Dict[str, float], targets: Dict[str, float],
                                performance_level: PerformanceLevel) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if performance_level == PerformanceLevel.NOT_READY:
            for metric_name, target_value in targets.items():
                actual_value = metrics.get(metric_name, 0)
                if metric_name == "uptime":
                    if actual_value < target_value:
                        recommendations.append(f"Increase {metric_name} from {actual_value}% to {target_value}%")
                else:
                    if actual_value > target_value:
                        recommendations.append(f"Reduce {metric_name} from {actual_value} to {target_value}")
        
        return recommendations

    def _generate_overall_recommendations(self, benchmarks: List[PerformanceBenchmark],
                                       overall_level: PerformanceLevel) -> List[str]:
        """Generate overall system recommendations"""
        recommendations = []
        
        if overall_level == PerformanceLevel.NOT_READY:
            recommendations.append("Critical performance issues detected - immediate optimization required")
            recommendations.append("Focus on response time and reliability improvements")
        elif overall_level == PerformanceLevel.DEVELOPMENT_READY:
            recommendations.append("Performance acceptable for development but needs improvement for production")
            recommendations.append("Consider scalability and throughput optimizations")
        elif overall_level == PerformanceLevel.PRODUCTION_READY:
            recommendations.append("Performance suitable for production deployment")
            recommendations.append("Monitor and optimize for enterprise readiness")
        elif overall_level == PerformanceLevel.ENTERPRISE_READY:
            recommendations.append("Excellent performance - suitable for enterprise deployment")
            recommendations.append("Continue monitoring and incremental optimization")
        
        return recommendations

    def get_benchmark_history(self) -> List[PerformanceBenchmark]:
        """Get all benchmark history"""
        return list(self.benchmarks.values())

    def get_performance_reports(self) -> List[SystemPerformanceReport]:
        """Get all performance reports"""
        return self.performance_reports.copy()

    def clear_history(self):
        """Clear benchmark and report history"""
        self.benchmarks.clear()
        self.performance_reports.clear()
        self.optimization_history.clear()
        self.logger.info("Performance validation history cleared")
