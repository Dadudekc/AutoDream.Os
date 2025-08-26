#!/usr/bin/env python3
"""
Performance Analyzer - V2 Modular Architecture
==============================================

Handles performance analysis, classification, and optimization recommendations.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, Any, List
from enum import Enum

from ..benchmarking.benchmark_types import BenchmarkResult
from ..validation.validation_types import ValidationRule


logger = logging.getLogger(__name__)


class PerformanceLevel(Enum):
    """Performance classification levels."""
    NOT_READY = "not_ready"
    BASIC = "basic"
    STANDARD = "standard"
    GOOD = "good"
    EXCELLENT = "excellent"
    ENTERPRISE_READY = "enterprise_ready"
    PRODUCTION_READY = "production_ready"


class PerformanceAnalyzer:
    """
    Performance Analyzer - Single responsibility: Analyze performance data
    
    Handles all performance analysis including:
    - Performance level classification
    - Optimization recommendations
    - Metrics analysis and scoring
    - System health assessment
    """

    def __init__(self):
        """Initialize performance analyzer"""
        self.logger = logging.getLogger(f"{__name__}.PerformanceAnalyzer")

    def classify_performance_level(self, metrics: Dict[str, Any]) -> PerformanceLevel:
        """Classify performance level based on metrics"""
        try:
            # Simple scoring algorithm
            score = 0.0
            total_metrics = 0
            
            for metric_name, value in metrics.items():
                if isinstance(value, (int, float)):
                    total_metrics += 1
                    
                    # Normalize value to 0-1 scale (simplified)
                    if "percent" in metric_name.lower():
                        normalized = 1.0 - (value / 100.0)  # Lower is better for percentages
                    elif "ms" in metric_name.lower() or "latency" in metric_name.lower():
                        normalized = 1.0 / (1.0 + value / 1000.0)  # Lower is better for time
                    elif "score" in metric_name.lower():
                        normalized = value  # Already 0-1
                    else:
                        normalized = min(value / 1000.0, 1.0)  # Cap at 1000
                    
                    score += normalized
            
            if total_metrics > 0:
                avg_score = score / total_metrics
                
                if avg_score >= 0.9:
                    return PerformanceLevel.EXCELLENT
                elif avg_score >= 0.8:
                    return PerformanceLevel.GOOD
                elif avg_score >= 0.7:
                    return PerformanceLevel.STANDARD
                elif avg_score >= 0.6:
                    return PerformanceLevel.BASIC
                else:
                    return PerformanceLevel.NOT_READY
            
            return PerformanceLevel.STANDARD
            
        except Exception as e:
            self.logger.error(f"Failed to classify performance level: {e}")
            return PerformanceLevel.NOT_READY

    def generate_optimization_recommendations(self, metrics: Dict[str, Any], 
                                           performance_level: PerformanceLevel) -> List[str]:
        """Generate optimization recommendations based on metrics and performance level"""
        recommendations = []
        
        try:
            # CPU recommendations
            if "cpu_usage_avg" in metrics and metrics["cpu_usage_avg"] > 80.0:
                recommendations.append("Consider CPU optimization or scaling")
            
            # Memory recommendations
            if "memory_usage_avg" in metrics and metrics["memory_usage_avg"] > 75.0:
                recommendations.append("Optimize memory usage or increase memory allocation")
            
            # Response time recommendations
            if "response_time_avg_ms" in metrics and metrics["response_time_avg_ms"] > 200.0:
                recommendations.append("Optimize response time through caching or algorithm improvements")
            
            # Throughput recommendations
            if "throughput_ops_per_sec" in metrics and metrics["throughput_ops_per_sec"] < 500.0:
                recommendations.append("Improve throughput through parallelization or optimization")
            
            # General recommendations based on performance level
            if performance_level == PerformanceLevel.NOT_READY:
                recommendations.append("System requires significant optimization before production use")
            elif performance_level == PerformanceLevel.BASIC:
                recommendations.append("Implement basic performance optimizations")
            elif performance_level == PerformanceLevel.STANDARD:
                recommendations.append("Consider advanced optimization techniques")
            elif performance_level == PerformanceLevel.GOOD:
                recommendations.append("Minor optimizations may provide additional benefits")
            elif performance_level == PerformanceLevel.EXCELLENT:
                recommendations.append("Performance is excellent - maintain current optimization level")
            
            # Default recommendation if none generated
            if not recommendations:
                recommendations.append("Performance is within acceptable parameters")
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations: {e}")
            recommendations.append("Unable to generate optimization recommendations")
        
        return recommendations

    def calculate_overall_performance_level(self, benchmark_history: List[BenchmarkResult]) -> PerformanceLevel:
        """Calculate overall system performance level from benchmark history"""
        try:
            if not benchmark_history:
                return PerformanceLevel.NOT_READY
            
            # Calculate average performance level from recent benchmarks
            recent_benchmarks = benchmark_history[-10:]  # Last 10 benchmarks
            level_scores = {
                PerformanceLevel.NOT_READY: 0,
                PerformanceLevel.BASIC: 1,
                PerformanceLevel.STANDARD: 2,
                PerformanceLevel.GOOD: 3,
                PerformanceLevel.EXCELLENT: 4,
                PerformanceLevel.ENTERPRISE_READY: 5,
                PerformanceLevel.PRODUCTION_READY: 6
            }
            
            total_score = 0
            valid_benchmarks = 0
            
            for benchmark in recent_benchmarks:
                if benchmark.success:
                    # Try to get performance level from benchmark metrics
                    if hasattr(benchmark, 'performance_level'):
                        total_score += level_scores.get(benchmark.performance_level, 0)
                    else:
                        # Calculate from metrics
                        level = self.classify_performance_level(benchmark.metrics)
                        total_score += level_scores.get(level, 0)
                    valid_benchmarks += 1
            
            if valid_benchmarks == 0:
                return PerformanceLevel.NOT_READY
            
            avg_score = total_score / valid_benchmarks
            
            # Map score back to level
            if avg_score >= 5.5:
                return PerformanceLevel.PRODUCTION_READY
            elif avg_score >= 4.5:
                return PerformanceLevel.ENTERPRISE_READY
            elif avg_score >= 3.5:
                return PerformanceLevel.EXCELLENT
            elif avg_score >= 2.5:
                return PerformanceLevel.GOOD
            elif avg_score >= 1.5:
                return PerformanceLevel.STANDARD
            elif avg_score >= 0.5:
                return PerformanceLevel.BASIC
            else:
                return PerformanceLevel.NOT_READY
                
        except Exception as e:
            self.logger.error(f"Failed to calculate overall performance level: {e}")
            return PerformanceLevel.NOT_READY

    def generate_system_recommendations(self, benchmark_history: List[BenchmarkResult], 
                                      alerts: List[str]) -> List[str]:
        """Generate system-wide recommendations"""
        recommendations = []
        
        try:
            # Calculate benchmark statistics
            total_benchmarks = len(benchmark_history)
            successful_benchmarks = len([b for b in benchmark_history if b.success])
            failed_benchmarks = total_benchmarks - successful_benchmarks
            
            # System health recommendations
            if failed_benchmarks > 0:
                failure_rate = failed_benchmarks / total_benchmarks
                if failure_rate > 0.1:  # More than 10% failure rate
                    recommendations.append("High benchmark failure rate detected - investigate system stability")
            
            # Performance level recommendations
            overall_level = self.calculate_overall_performance_level(benchmark_history)
            if overall_level == PerformanceLevel.NOT_READY:
                recommendations.append("System requires immediate performance optimization")
            elif overall_level == PerformanceLevel.BASIC:
                recommendations.append("Implement performance monitoring and optimization")
            
            # Alert recommendations
            if len(alerts) > 10:
                recommendations.append("High number of alerts - review threshold configurations")
            
            # Default recommendation
            if not recommendations:
                recommendations.append("System performance is within acceptable parameters")
            
        except Exception as e:
            self.logger.error(f"Failed to generate system recommendations: {e}")
            recommendations.append("Unable to generate system recommendations")
        
        return recommendations

    def determine_system_health(self, is_running: bool, alerts: List[str], 
                              benchmark_history: List[BenchmarkResult]) -> str:
        """Determine overall system health status"""
        try:
            if not is_running:
                return "stopped"
            
            # Check for critical alerts
            critical_alerts = [alert for alert in alerts[-10:] if "CRITICAL:" in alert]
            if critical_alerts:
                return "critical"
            
            # Check for warnings
            warning_alerts = [alert for alert in alerts[-10:] if "WARNING:" in alert]
            if warning_alerts:
                return "warning"
            
            # Check benchmark success rate
            if benchmark_history:
                successful_benchmarks = len([b for b in benchmark_history if b.success])
                success_rate = successful_benchmarks / len(benchmark_history)
                if success_rate < 0.8:  # Less than 80% success rate
                    return "degraded"
            
            return "healthy"
            
        except Exception as e:
            self.logger.error(f"Failed to determine system health: {e}")
            return "unknown"

    def analyze_metrics_trends(self, metrics_history: List[Any]) -> Dict[str, Any]:
        """Analyze metrics trends over time"""
        try:
            trends = {}
            
            # Group metrics by name
            metrics_by_name = {}
            for metric in metrics_history:
                if hasattr(metric, 'name') and hasattr(metric, 'value'):
                    if metric.name not in metrics_by_name:
                        metrics_by_name[metric.name] = []
                    metrics_by_name[metric.name].append(metric.value)
            
            # Calculate trends for each metric
            for metric_name, values in metrics_by_name.items():
                if len(values) >= 2:
                    # Simple trend analysis
                    first_half = values[:len(values)//2]
                    second_half = values[len(values)//2:]
                    
                    first_avg = sum(first_half) / len(first_half)
                    second_avg = sum(second_half) / len(second_half)
                    
                    if second_avg > first_avg * 1.1:
                        trend = "increasing"
                    elif second_avg < first_avg * 0.9:
                        trend = "decreasing"
                    else:
                        trend = "stable"
                    
                    trends[metric_name] = {
                        "trend": trend,
                        "first_half_avg": first_avg,
                        "second_half_avg": second_avg,
                        "change_percent": ((second_avg - first_avg) / first_avg) * 100 if first_avg > 0 else 0
                    }
            
            return trends
            
        except Exception as e:
            self.logger.error(f"Failed to analyze metrics trends: {e}")
            return {}

    def get_performance_summary(self, metrics_history: List[Any], 
                               benchmark_history: List[BenchmarkResult],
                               alerts: List[str]) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        try:
            # Calculate metrics summary
            metrics_summary = {}
            if metrics_history:
                metrics_by_name = {}
                for metric in metrics_history:
                    if hasattr(metric, 'name') and hasattr(metric, 'value'):
                        if metric.name not in metrics_by_name:
                            metrics_by_name[metric.name] = []
                        metrics_by_name[metric.name].append(metric.value)
                
                for metric_name, values in metrics_by_name.items():
                    if values:
                        metrics_summary[metric_name] = {
                            "count": len(values),
                            "min": min(values),
                            "max": max(values),
                            "avg": sum(values) / len(values),
                            "latest": values[-1]
                        }
            
            # Get recent data
            recent_validation_results = []  # Placeholder
            recent_benchmarks = benchmark_history[-50:] if benchmark_history else []
            recent_alerts = alerts[-20:] if alerts else []
            
            # Determine overall performance level
            overall_level = self.calculate_overall_performance_level(benchmark_history)
            
            # Generate recommendations
            recommendations = self.generate_system_recommendations(benchmark_history, alerts)
            
            # Determine system health
            system_health = self.determine_system_health(True, alerts, benchmark_history)
            
            return {
                "metrics_summary": metrics_summary,
                "validation_results": recent_validation_results,
                "benchmarks": recent_benchmarks,
                "recommendations": recommendations,
                "alerts": recent_alerts,
                "overall_performance_level": overall_level.value,
                "system_health": system_health
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get performance summary: {e}")
            return {"error": str(e)}
