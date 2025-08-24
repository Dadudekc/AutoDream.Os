#!/usr/bin/env python3
"""
Performance Validation Data Models - V2 Core Performance Testing & Optimization

Performance validation system data structures and models.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from .enums import BenchmarkType, PerformanceLevel, OptimizationTarget


@dataclass
class PerformanceBenchmark:
    """Performance benchmark result"""
    benchmark_id: str
    benchmark_type: BenchmarkType
    test_name: str
    start_time: str
    end_time: str
    duration: float
    metrics: Dict[str, float]
    target_metrics: Dict[str, float]
    performance_level: PerformanceLevel
    optimization_recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def get_metric_value(self, metric_name: str) -> Optional[float]:
        """Get value for a specific metric"""
        return self.metrics.get(metric_name)
    
    def get_target_value(self, metric_name: str) -> Optional[float]:
        """Get target value for a specific metric"""
        return self.target_metrics.get(metric_name)
    
    def is_target_met(self, metric_name: str) -> bool:
        """Check if target metric is met"""
        actual = self.get_metric_value(metric_name)
        target = self.get_target_value(metric_name)
        if actual is None or target is None:
            return False
        return actual >= target
    
    def get_performance_score(self) -> float:
        """Calculate overall performance score (0-100)"""
        if not self.target_metrics:
            return 0.0
        
        met_targets = sum(1 for metric in self.target_metrics.keys() if self.is_target_met(metric))
        total_targets = len(self.target_metrics)
        
        return (met_targets / total_targets) * 100 if total_targets > 0 else 0.0


@dataclass
class SystemPerformanceReport:
    """System performance report"""
    report_id: str
    timestamp: str
    overall_performance_level: PerformanceLevel
    benchmark_results: List[PerformanceBenchmark]
    optimization_opportunities: List[OptimizationTarget]
    enterprise_readiness_score: float
    recommendations: List[str]
    system_info: Dict[str, Any] = field(default_factory=dict)
    environment: str = "production"
    
    def get_benchmark_by_type(self, benchmark_type: BenchmarkType) -> List[PerformanceBenchmark]:
        """Get benchmarks by type"""
        return [b for b in self.benchmark_results if b.benchmark_type == benchmark_type]
    
    def get_overall_score(self) -> float:
        """Calculate overall performance score"""
        if not self.benchmark_results:
            return 0.0
        
        scores = [benchmark.get_performance_score() for benchmark in self.benchmark_results]
        return sum(scores) / len(scores) if scores else 0.0
    
    def get_critical_issues(self) -> List[str]:
        """Get list of critical performance issues"""
        critical_benchmarks = [
            b for b in self.benchmark_results 
            if b.performance_level == PerformanceLevel.CRITICAL_ISSUES
        ]
        
        issues = []
        for benchmark in critical_benchmarks:
            issues.append(f"{benchmark.test_name}: {benchmark.optimization_recommendations}")
        
        return issues
    
    def get_optimization_priority(self) -> List[OptimizationTarget]:
        """Get optimization targets in priority order"""
        # Simple priority based on performance levels
        priority_map = {
            PerformanceLevel.CRITICAL_ISSUES: 1,
            PerformanceLevel.NOT_READY: 2,
            PerformanceLevel.OPTIMIZATION_NEEDED: 3,
            PerformanceLevel.DEVELOPMENT_READY: 4,
            PerformanceLevel.PRODUCTION_READY: 5,
            PerformanceLevel.ENTERPRISE_READY: 6,
        }
        
        # Group benchmarks by performance level and count
        level_counts = {}
        for benchmark in self.benchmark_results:
            level = benchmark.performance_level
            level_counts[level] = level_counts.get(level, 0) + 1
        
        # Sort by priority (lower number = higher priority)
        sorted_levels = sorted(level_counts.keys(), key=lambda x: priority_map.get(x, 999))
        
        # Map to optimization targets
        priority_targets = []
        for level in sorted_levels:
            if level == PerformanceLevel.CRITICAL_ISSUES:
                priority_targets.extend([
                    OptimizationTarget.RESPONSE_TIME_IMPROVEMENT,
                    OptimizationTarget.RELIABILITY_IMPROVEMENT
                ])
            elif level == PerformanceLevel.NOT_READY:
                priority_targets.extend([
                    OptimizationTarget.SCALABILITY_ENHANCEMENT,
                    OptimizationTarget.RESOURCE_EFFICIENCY
                ])
        
        return priority_targets[:5]  # Return top 5 priorities
