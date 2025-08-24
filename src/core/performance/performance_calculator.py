#!/usr/bin/env python3
"""
Performance Calculator - V2 Core Performance System

This module handles performance calculations and scoring.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import statistics

from src.utils.stability_improvements import stability_manager, safe_import
from typing import List, Dict, Any
from .performance_types import (
    PerformanceBenchmark, PerformanceLevel, OptimizationTarget,
    PerformanceThresholds
)


class PerformanceCalculator:
    """Handles performance calculations and scoring"""
    
    def __init__(self, thresholds: PerformanceThresholds):
        self.thresholds = thresholds
    
    def calculate_performance_level(self, benchmark: PerformanceBenchmark) -> PerformanceLevel:
        """Calculate performance level for a benchmark"""
        try:
            # Extract key metrics
            metrics = benchmark.metrics
            
            if "error" in metrics:
                return PerformanceLevel.NOT_READY
            
            # Calculate score based on target achievement
            if "avg_response_time" in metrics:
                target = benchmark.target_metrics.get("target", 100.0)
                score = max(0, 1 - (metrics["avg_response_time"] / target))
            elif "throughput" in metrics:
                target = benchmark.target_metrics.get("target", 1000.0)
                score = min(1, metrics["throughput"] / target)
            elif "max_concurrent_users" in metrics:
                target = benchmark.target_metrics.get("target", 100.0)
                score = min(1, metrics["max_concurrent_users"] / target)
            else:
                score = 0.5  # Default score
            
            # Classify based on thresholds
            if score >= self.thresholds.enterprise_ready:
                return PerformanceLevel.ENTERPRISE_READY
            elif score >= self.thresholds.production_ready:
                return PerformanceLevel.PRODUCTION_READY
            elif score >= self.thresholds.development_ready:
                return PerformanceLevel.DEVELOPMENT_READY
            else:
                return PerformanceLevel.NOT_READY
                
        except Exception:
            return PerformanceLevel.NOT_READY
    
    def calculate_overall_performance_level(self, benchmarks: List[PerformanceBenchmark]) -> PerformanceLevel:
        """Calculate overall performance level from multiple benchmarks"""
        if not benchmarks:
            return PerformanceLevel.NOT_READY
        
        # Calculate average score across all benchmarks
        scores = []
        for benchmark in benchmarks:
            if benchmark.performance_level == PerformanceLevel.ENTERPRISE_READY:
                scores.append(1.0)
            elif benchmark.performance_level == PerformanceLevel.PRODUCTION_READY:
                scores.append(0.85)
            elif benchmark.performance_level == PerformanceLevel.DEVELOPMENT_READY:
                scores.append(0.70)
            else:
                scores.append(0.0)
        
        avg_score = sum(scores) / len(scores)
        
        # Classify overall performance
        if avg_score >= self.thresholds.enterprise_ready:
            return PerformanceLevel.ENTERPRISE_READY
        elif avg_score >= self.thresholds.production_ready:
            return PerformanceLevel.PRODUCTION_READY
        elif avg_score >= self.thresholds.development_ready:
            return PerformanceLevel.DEVELOPMENT_READY
        else:
            return PerformanceLevel.NOT_READY
    
    def calculate_enterprise_readiness_score(self, benchmarks: List[PerformanceBenchmark]) -> float:
        """Calculate enterprise readiness score (0.0 to 1.0)"""
        if not benchmarks:
            return 0.0
        
        # Weight different benchmark types
        weights = {
            "response_time": 0.25,
            "throughput": 0.25,
            "scalability": 0.20,
            "reliability": 0.20,
            "latency": 0.10
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for benchmark in benchmarks:
            weight = weights.get(benchmark.benchmark_type.value, 0.1)
            
            if benchmark.performance_level == PerformanceLevel.ENTERPRISE_READY:
                score = 1.0
            elif benchmark.performance_level == PerformanceLevel.PRODUCTION_READY:
                score = 0.85
            elif benchmark.performance_level == PerformanceLevel.DEVELOPMENT_READY:
                score = 0.70
            else:
                score = 0.0
            
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def identify_optimization_opportunities(self, benchmarks: List[PerformanceBenchmark]) -> List[OptimizationTarget]:
        """Identify optimization opportunities from benchmark results"""
        opportunities = []
        
        for benchmark in benchmarks:
            if benchmark.performance_level == PerformanceLevel.NOT_READY:
                if benchmark.benchmark_type.value == "response_time":
                    opportunities.append(OptimizationTarget.RESPONSE_TIME_IMPROVEMENT)
                elif benchmark.benchmark_type.value == "throughput":
                    opportunities.append(OptimizationTarget.THROUGHPUT_INCREASE)
                elif benchmark.benchmark_type.value == "scalability":
                    opportunities.append(OptimizationTarget.SCALABILITY_ENHANCEMENT)
                elif benchmark.benchmark_type.value == "reliability":
                    opportunities.append(OptimizationTarget.RELIABILITY_IMPROVEMENT)
                else:
                    opportunities.append(OptimizationTarget.RESOURCE_EFFICIENCY)
        
        # Remove duplicates while preserving order
        unique_opportunities = []
        for opp in opportunities:
            if opp not in unique_opportunities:
                unique_opportunities.append(opp)
        
        return unique_opportunities
    
    def calculate_percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile value from a list of numbers"""
        if not values:
            return 0.0
        
        try:
            return statistics.quantiles(values, n=100)[percentile - 1]
        except (IndexError, statistics.StatisticsError):
            # Fallback to simple percentile calculation
            sorted_values = sorted(values)
            index = int((percentile / 100) * len(sorted_values))
            return sorted_values[min(index, len(sorted_values) - 1)]
    
    def calculate_scalability_score(self, concurrent_users: List[int], target: float) -> float:
        """Calculate scalability score based on concurrent user performance"""
        if not concurrent_users:
            return 0.0
        
        # Calculate how well the system scales
        max_users = max(concurrent_users)
        avg_users = sum(concurrent_users) / len(concurrent_users)
        
        # Score based on target achievement and consistency
        target_achievement = min(1.0, max_users / target)
        consistency = avg_users / max_users if max_users > 0 else 0.0
        
        # Weighted score
        return (target_achievement * 0.7) + (consistency * 0.3)



