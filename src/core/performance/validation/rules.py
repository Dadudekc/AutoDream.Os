#!/usr/bin/env python3
"""
Performance Validation Rules - V2 Core Performance System
=========================================================

Handles performance validation rules and classification logic.
Follows Single Responsibility Principle - validation rules only.
"""

import logging
from typing import Dict, List, Any, Optional
from enum import Enum

from src.utils.stability_improvements import stability_manager, safe_import
from ..metrics.collector import BenchmarkType, PerformanceLevel, PerformanceBenchmark


class OptimizationTarget(Enum):
    """Performance optimization targets"""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    SCALABILITY = "scalability"
    RELIABILITY = "reliability"
    RESOURCE_EFFICIENCY = "resource_efficiency"


class ValidationRules:
    """
    Performance validation rules and classification system
    
    Responsibilities:
    - Define performance validation rules
    - Classify performance levels based on metrics
    - Generate optimization recommendations
    - Validate benchmark results against targets
    """
    
    def __init__(self):
        self.performance_thresholds = {
            PerformanceLevel.ENTERPRISE_READY: 0.95,  # 95% of targets met
            PerformanceLevel.PRODUCTION_READY: 0.85,  # 85% of targets met
            PerformanceLevel.DEVELOPMENT_READY: 0.70,  # 70% of targets met
            PerformanceLevel.NOT_READY: 0.0,  # Below 70%
        }
        
        self.benchmark_targets = {
            BenchmarkType.RESPONSE_TIME: {"target": 100, "unit": "ms"},
            BenchmarkType.THROUGHPUT: {"target": 1000, "unit": "ops/sec"},
            BenchmarkType.SCALABILITY: {"target": 100, "unit": "concurrent_users"},
            BenchmarkType.RELIABILITY: {"target": 99.9, "unit": "%"},
            BenchmarkType.LATENCY: {"target": 50, "unit": "ms"},
        }
        
        self.logger = logging.getLogger(f"{__name__}.ValidationRules")
    
    def classify_performance_level(self, actual_value: float, target_value: float, 
                                 lower_is_better: bool = True) -> PerformanceLevel:
        """Classify performance level based on actual vs target values"""
        try:
            if target_value == 0:
                return PerformanceLevel.NOT_READY
            
            if lower_is_better:
                # For metrics where lower values are better (response time, latency)
                performance_ratio = target_value / actual_value if actual_value > 0 else 0
            else:
                # For metrics where higher values are better (throughput, reliability)
                performance_ratio = actual_value / target_value
            
            # Classify based on performance ratio
            if performance_ratio >= self.performance_thresholds[PerformanceLevel.ENTERPRISE_READY]:
                return PerformanceLevel.ENTERPRISE_READY
            elif performance_ratio >= self.performance_thresholds[PerformanceLevel.PRODUCTION_READY]:
                return PerformanceLevel.PRODUCTION_READY
            elif performance_ratio >= self.performance_thresholds[PerformanceLevel.DEVELOPMENT_READY]:
                return PerformanceLevel.DEVELOPMENT_READY
            else:
                return PerformanceLevel.NOT_READY
                
        except Exception as e:
            self.logger.error(f"Failed to classify performance level: {e}")
            return PerformanceLevel.NOT_READY
    
    def calculate_overall_performance_level(self, benchmarks: List[PerformanceBenchmark]) -> PerformanceLevel:
        """Calculate overall performance level from multiple benchmarks"""
        try:
            if not benchmarks:
                return PerformanceLevel.NOT_READY
            
            # Count performance levels
            level_counts = {level: 0 for level in PerformanceLevel}
            
            for benchmark in benchmarks:
                level_counts[benchmark.performance_level] += 1
            
            total_benchmarks = len(benchmarks)
            
            # Calculate weighted score
            level_weights = {
                PerformanceLevel.ENTERPRISE_READY: 4,
                PerformanceLevel.PRODUCTION_READY: 3,
                PerformanceLevel.DEVELOPMENT_READY: 2,
                PerformanceLevel.NOT_READY: 1,
            }
            
            weighted_score = sum(
                level_counts[level] * weight 
                for level, weight in level_weights.items()
            )
            
            average_score = weighted_score / total_benchmarks
            
            # Classify overall level based on average score
            if average_score >= 3.8:  # Mostly enterprise ready
                return PerformanceLevel.ENTERPRISE_READY
            elif average_score >= 3.0:  # Mostly production ready
                return PerformanceLevel.PRODUCTION_READY
            elif average_score >= 2.0:  # Mostly development ready
                return PerformanceLevel.DEVELOPMENT_READY
            else:
                return PerformanceLevel.NOT_READY
                
        except Exception as e:
            self.logger.error(f"Failed to calculate overall performance level: {e}")
            return PerformanceLevel.NOT_READY
    
    def validate_benchmark_result(self, benchmark: PerformanceBenchmark) -> Dict[str, Any]:
        """Validate a benchmark result against rules"""
        try:
            validation_result = {
                "benchmark_id": benchmark.benchmark_id,
                "is_valid": True,
                "validation_errors": [],
                "warnings": [],
                "performance_assessment": {},
            }
            
            # Check if benchmark has required metrics
            if not benchmark.metrics:
                validation_result["is_valid"] = False
                validation_result["validation_errors"].append("No metrics found in benchmark")
                return validation_result
            
            # Validate against targets
            target_info = self.benchmark_targets.get(benchmark.benchmark_type)
            if target_info:
                target_value = target_info["target"]
                
                # Get primary metric for this benchmark type
                primary_metric = self._get_primary_metric(benchmark.benchmark_type, benchmark.metrics)
                
                if primary_metric is not None:
                    performance_ratio = self._calculate_performance_ratio(
                        primary_metric, target_value, benchmark.benchmark_type
                    )
                    
                    validation_result["performance_assessment"] = {
                        "primary_metric": primary_metric,
                        "target_value": target_value,
                        "performance_ratio": performance_ratio,
                        "meets_target": performance_ratio >= 1.0,
                    }
                    
                    # Add warnings for poor performance
                    if performance_ratio < 0.5:
                        validation_result["warnings"].append(
                            f"Performance significantly below target ({performance_ratio:.2%})"
                        )
                    elif performance_ratio < 0.8:
                        validation_result["warnings"].append(
                            f"Performance below target ({performance_ratio:.2%})"
                        )
            
            # Validate performance level consistency
            expected_level = self._calculate_expected_performance_level(benchmark)
            if expected_level != benchmark.performance_level:
                validation_result["warnings"].append(
                    f"Performance level mismatch: expected {expected_level.value}, got {benchmark.performance_level.value}"
                )
            
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Failed to validate benchmark result: {e}")
            return {
                "benchmark_id": benchmark.benchmark_id,
                "is_valid": False,
                "validation_errors": [f"Validation failed: {str(e)}"],
                "warnings": [],
                "performance_assessment": {},
            }
    
    def generate_optimization_recommendations(self, benchmark: PerformanceBenchmark) -> List[str]:
        """Generate optimization recommendations based on benchmark results"""
        try:
            recommendations = []
            
            if benchmark.benchmark_type == BenchmarkType.RESPONSE_TIME:
                recommendations.extend(self._get_response_time_recommendations(benchmark))
            elif benchmark.benchmark_type == BenchmarkType.THROUGHPUT:
                recommendations.extend(self._get_throughput_recommendations(benchmark))
            elif benchmark.benchmark_type == BenchmarkType.SCALABILITY:
                recommendations.extend(self._get_scalability_recommendations(benchmark))
            elif benchmark.benchmark_type == BenchmarkType.RELIABILITY:
                recommendations.extend(self._get_reliability_recommendations(benchmark))
            elif benchmark.benchmark_type == BenchmarkType.LATENCY:
                recommendations.extend(self._get_latency_recommendations(benchmark))
            
            # Add general recommendations based on performance level
            if benchmark.performance_level == PerformanceLevel.NOT_READY:
                recommendations.append("Consider major architectural changes")
                recommendations.append("Review system design and implementation")
            elif benchmark.performance_level == PerformanceLevel.DEVELOPMENT_READY:
                recommendations.append("Focus on performance optimization")
                recommendations.append("Consider profiling and bottleneck analysis")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to generate optimization recommendations: {e}")
            return ["Unable to generate recommendations due to error"]
    
    def _get_primary_metric(self, benchmark_type: BenchmarkType, metrics: Dict[str, float]) -> Optional[float]:
        """Get the primary metric for a benchmark type"""
        metric_mappings = {
            BenchmarkType.RESPONSE_TIME: "average_response_time",
            BenchmarkType.THROUGHPUT: "throughput_ops_per_sec",
            BenchmarkType.SCALABILITY: "scalability_score",
            BenchmarkType.RELIABILITY: "success_rate_percent",
            BenchmarkType.LATENCY: "average_latency",
        }
        
        primary_key = metric_mappings.get(benchmark_type)
        return metrics.get(primary_key) if primary_key else None
    
    def _calculate_performance_ratio(self, actual: float, target: float, 
                                   benchmark_type: BenchmarkType) -> float:
        """Calculate performance ratio considering if lower or higher is better"""
        if target == 0:
            return 0.0
        
        # Determine if lower is better for this benchmark type
        lower_is_better_types = {BenchmarkType.RESPONSE_TIME, BenchmarkType.LATENCY}
        
        if benchmark_type in lower_is_better_types:
            return target / actual if actual > 0 else 0.0
        else:
            return actual / target
    
    def _calculate_expected_performance_level(self, benchmark: PerformanceBenchmark) -> PerformanceLevel:
        """Calculate expected performance level based on metrics"""
        target_info = self.benchmark_targets.get(benchmark.benchmark_type)
        if not target_info:
            return PerformanceLevel.NOT_READY
        
        primary_metric = self._get_primary_metric(benchmark.benchmark_type, benchmark.metrics)
        if primary_metric is None:
            return PerformanceLevel.NOT_READY
        
        lower_is_better = benchmark.benchmark_type in {BenchmarkType.RESPONSE_TIME, BenchmarkType.LATENCY}
        
        return self.classify_performance_level(
            primary_metric, target_info["target"], lower_is_better
        )
    
    def _get_response_time_recommendations(self, benchmark: PerformanceBenchmark) -> List[str]:
        """Get response time specific recommendations"""
        recommendations = []
        avg_response = benchmark.metrics.get("average_response_time", 0)
        target = self.benchmark_targets[BenchmarkType.RESPONSE_TIME]["target"]
        
        if avg_response > target:
            recommendations.append("Optimize agent registration process")
            recommendations.append("Consider caching mechanisms")
            recommendations.append("Review database query performance")
            
            if avg_response > target * 2:
                recommendations.append("Consider asynchronous processing")
                recommendations.append("Implement connection pooling")
        
        return recommendations
    
    def _get_throughput_recommendations(self, benchmark: PerformanceBenchmark) -> List[str]:
        """Get throughput specific recommendations"""
        recommendations = []
        throughput = benchmark.metrics.get("throughput_ops_per_sec", 0)
        target = self.benchmark_targets[BenchmarkType.THROUGHPUT]["target"]
        
        if throughput < target:
            recommendations.append("Optimize contract creation process")
            recommendations.append("Consider batch contract creation")
            recommendations.append("Review database write performance")
            
            if throughput < target * 0.5:
                recommendations.append("Consider horizontal scaling")
                recommendations.append("Implement load balancing")
        
        return recommendations
    
    def _get_scalability_recommendations(self, benchmark: PerformanceBenchmark) -> List[str]:
        """Get scalability specific recommendations"""
        recommendations = []
        scalability_score = benchmark.metrics.get("scalability_score", 0)
        
        if scalability_score < 80:
            recommendations.append("Review system architecture for bottlenecks")
            recommendations.append("Consider microservices architecture")
            recommendations.append("Implement proper resource management")
            
            if scalability_score < 50:
                recommendations.append("Consider distributed system design")
                recommendations.append("Implement auto-scaling mechanisms")
        
        return recommendations
    
    def _get_reliability_recommendations(self, benchmark: PerformanceBenchmark) -> List[str]:
        """Get reliability specific recommendations"""
        recommendations = []
        success_rate = benchmark.metrics.get("success_rate_percent", 0)
        target = self.benchmark_targets[BenchmarkType.RELIABILITY]["target"]
        
        if success_rate < target:
            recommendations.append("Implement better error handling")
            recommendations.append("Add retry mechanisms")
            recommendations.append("Improve system monitoring")
            
            if success_rate < target * 0.9:
                recommendations.append("Consider circuit breaker patterns")
                recommendations.append("Implement health checks")
        
        return recommendations
    
    def _get_latency_recommendations(self, benchmark: PerformanceBenchmark) -> List[str]:
        """Get latency specific recommendations"""
        recommendations = []
        avg_latency = benchmark.metrics.get("average_latency", 0)
        target = self.benchmark_targets[BenchmarkType.LATENCY]["target"]
        
        if avg_latency > target:
            recommendations.append("Optimize network communication")
            recommendations.append("Consider edge computing")
            recommendations.append("Implement request/response caching")
            
            if avg_latency > target * 2:
                recommendations.append("Review data serialization")
                recommendations.append("Consider protocol optimization")
        
        return recommendations
