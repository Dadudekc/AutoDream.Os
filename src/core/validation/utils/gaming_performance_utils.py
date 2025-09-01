#!/usr/bin/env python3
"""
Gaming Performance Utils - Agent Cellphone V2
============================================

Utility functions for gaming performance integration system.
Extracted from gaming_performance_integration.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import time
import statistics
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum

from ..models.gaming_performance_models import (
    PerformanceTestType, GamingComponentProfile, PerformanceTestResult,
    PerformanceMetrics, PerformanceAnalysisResult
)


class PerformanceTestConfigurations:
    """Performance test configurations."""
    
    @staticmethod
    def get_test_configurations() -> Dict[PerformanceTestType, Dict[str, Any]]:
        """Get performance test configurations."""
        return {
            PerformanceTestType.LOAD_TEST: {
                "duration_seconds": 60,
                "concurrent_operations": 10,
                "operation_interval": 0.1
            },
            PerformanceTestType.STRESS_TEST: {
                "duration_seconds": 30,
                "concurrent_operations": 50,
                "operation_interval": 0.05
            },
            PerformanceTestType.ENDURANCE_TEST: {
                "duration_seconds": 300,
                "concurrent_operations": 5,
                "operation_interval": 0.2
            },
            PerformanceTestType.SPIKE_TEST: {
                "duration_seconds": 15,
                "concurrent_operations": 100,
                "operation_interval": 0.01
            },
            PerformanceTestType.VOLUME_TEST: {
                "duration_seconds": 120,
                "concurrent_operations": 25,
                "operation_interval": 0.08
            }
        }


class PerformanceCalculations:
    """Performance calculation utilities."""
    
    @staticmethod
    def calculate_performance_score(metrics: Dict[str, float], thresholds: Dict[str, float]) -> float:
        """Calculate performance score based on metrics and thresholds."""
        if not metrics or not thresholds:
            return 0.0
        
        score_components = []
        for metric_name, value in metrics.items():
            if metric_name in thresholds:
                threshold = thresholds[metric_name]
                if threshold > 0:
                    # For metrics where lower is better (response time, latency)
                    if metric_name in ['response_time', 'latency', 'memory_usage', 'cpu_usage', 'error_rate']:
                        score = max(0, (threshold - value) / threshold * 100)
                    else:
                        # For metrics where higher is better (throughput, io_operations)
                        score = min(100, (value / threshold) * 100)
                    score_components.append(score)
        
        return statistics.mean(score_components) if score_components else 0.0
    
    @staticmethod
    def calculate_statistical_metrics(values: List[float]) -> Dict[str, float]:
        """Calculate statistical metrics from a list of values."""
        if not values:
            return {}
        
        return {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "min": min(values),
            "max": max(values),
            "count": len(values)
        }
    
    @staticmethod
    def detect_performance_regression(
        baseline_metrics: Dict[str, float],
        current_metrics: Dict[str, float],
        regression_threshold: float = 0.1
    ) -> Tuple[bool, Dict[str, float]]:
        """Detect performance regression between baseline and current metrics."""
        regression_detected = False
        regression_deltas = {}
        
        for metric_name, baseline_value in baseline_metrics.items():
            if metric_name in current_metrics:
                current_value = current_metrics[metric_name]
                delta = (current_value - baseline_value) / baseline_value if baseline_value > 0 else 0
                regression_deltas[metric_name] = delta
                
                # Check for significant regression
                if abs(delta) > regression_threshold:
                    regression_detected = True
        
        return regression_detected, regression_deltas


class PerformanceRecommendations:
    """Performance recommendation utilities."""
    
    @staticmethod
    def generate_performance_recommendations(
        metrics: Dict[str, float],
        thresholds: Dict[str, float],
        test_type: PerformanceTestType
    ) -> List[str]:
        """Generate performance recommendations based on metrics and thresholds."""
        recommendations = []
        
        for metric_name, value in metrics.items():
            if metric_name in thresholds:
                threshold = thresholds[metric_name]
                
                if metric_name == 'response_time' and value > threshold:
                    recommendations.append(f"Response time {value:.2f}ms exceeds threshold {threshold:.2f}ms. Consider optimizing database queries or caching.")
                
                elif metric_name == 'throughput' and value < threshold:
                    recommendations.append(f"Throughput {value:.2f} ops/sec below threshold {threshold:.2f} ops/sec. Consider horizontal scaling or code optimization.")
                
                elif metric_name == 'memory_usage' and value > threshold:
                    recommendations.append(f"Memory usage {value:.2f}MB exceeds threshold {threshold:.2f}MB. Consider memory optimization or garbage collection tuning.")
                
                elif metric_name == 'cpu_usage' and value > threshold:
                    recommendations.append(f"CPU usage {value:.2f}% exceeds threshold {threshold:.2f}%. Consider CPU optimization or load balancing.")
                
                elif metric_name == 'error_rate' and value > threshold:
                    recommendations.append(f"Error rate {value:.2f}% exceeds threshold {threshold:.2f}%. Review error handling and system stability.")
        
        # Test-specific recommendations
        if test_type == PerformanceTestType.STRESS_TEST:
            recommendations.append("Stress test completed. Monitor system recovery and stability.")
        elif test_type == PerformanceTestType.ENDURANCE_TEST:
            recommendations.append("Endurance test completed. Check for memory leaks and resource exhaustion.")
        elif test_type == PerformanceTestType.SPIKE_TEST:
            recommendations.append("Spike test completed. Verify system can handle traffic spikes gracefully.")
        
        return recommendations


class PerformanceThresholds:
    """Performance thresholds for gaming components."""
    
    @staticmethod
    def get_gaming_component_thresholds() -> Dict[str, Dict[str, float]]:
        """Get performance thresholds for gaming components."""
        return {
            "GamingIntegrationCore": {
                "response_time": 50.0,  # 50ms
                "throughput": 2000.0,  # 2000 ops/sec
                "memory_usage": 100.0,  # 100MB
                "cpu_usage": 30.0,     # 30%
                "error_rate": 0.1,     # 0.1%
                "latency": 25.0,       # 25ms
                "io_operations": 500.0  # 500 ops/sec
            },
            "GamingPerformanceMonitors": {
                "response_time": 100.0,  # 100ms
                "throughput": 1000.0,   # 1000 ops/sec
                "memory_usage": 50.0,   # 50MB
                "cpu_usage": 20.0,      # 20%
                "error_rate": 0.05,     # 0.05%
                "latency": 50.0,        # 50ms
                "io_operations": 200.0  # 200 ops/sec
            },
            "GamingEventHandlers": {
                "response_time": 200.0,  # 200ms
                "throughput": 500.0,    # 500 ops/sec
                "memory_usage": 75.0,   # 75MB
                "cpu_usage": 25.0,      # 25%
                "error_rate": 0.2,      # 0.2%
                "latency": 100.0,       # 100ms
                "io_operations": 100.0  # 100 ops/sec
            }
        }
