"""
Performance Monitor Module

Handles performance monitoring and threshold checking for the alert system.
"""

import logging
from typing import Dict, List, Optional
from ..metrics.collector import PerformanceBenchmark, BenchmarkType
from .alert_core import AlertSeverity, AlertFactory


class PerformanceMonitor:
    """Monitors performance metrics for alert conditions"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerformanceMonitor")
        
        # Alert thresholds
        self.alert_thresholds = {
            BenchmarkType.RESPONSE_TIME: {
                "critical": 500,  # 500ms
                "high": 200,      # 200ms
                "medium": 150,    # 150ms
            },
            BenchmarkType.THROUGHPUT: {
                "critical": 100,  # 100 ops/sec
                "high": 500,      # 500 ops/sec
                "medium": 750,    # 750 ops/sec
            },
            BenchmarkType.RELIABILITY: {
                "critical": 95.0,  # 95%
                "high": 98.0,      # 98%
                "medium": 99.0,    # 99%
            },
            BenchmarkType.SCALABILITY: {
                "critical": 30.0,  # 30% scalability score
                "high": 50.0,      # 50% scalability score
                "medium": 70.0,    # 70% scalability score
            },
            BenchmarkType.LATENCY: {
                "critical": 200,   # 200ms
                "high": 100,       # 100ms
                "medium": 75,      # 75ms
            },
        }
    
    def check_benchmark_for_alerts(self, benchmark: PerformanceBenchmark) -> List:
        """Check a benchmark result for alert conditions"""
        try:
            alerts = []
            
            # Check performance level alerts
            if benchmark.performance_level.value in ["NOT_READY", "DEVELOPMENT_READY"]:
                severity = AlertSeverity.CRITICAL if benchmark.performance_level.value == "NOT_READY" else AlertSeverity.HIGH
                alert = AlertFactory.create_performance_level_alert(benchmark, severity)
                alerts.append(alert)
            
            # Check threshold breaches
            threshold_alerts = self._check_threshold_breaches(benchmark)
            alerts.extend(threshold_alerts)
            
            # Check for specific benchmark type issues
            type_specific_alerts = self._check_type_specific_issues(benchmark)
            alerts.extend(type_specific_alerts)
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Failed to check benchmark for alerts: {e}")
            return []
    
    def _check_threshold_breaches(self, benchmark: PerformanceBenchmark) -> List:
        """Check for threshold breaches in benchmark metrics"""
        alerts = []
        
        try:
            thresholds = self.alert_thresholds.get(benchmark.benchmark_type, {})
            if not thresholds:
                return alerts
            
            # Get primary metric for this benchmark type
            primary_metric = self._get_primary_metric_value(benchmark)
            if primary_metric is None:
                return alerts
            
            # Check thresholds (from most severe to least)
            for severity_name in ["critical", "high", "medium"]:
                threshold = thresholds.get(severity_name)
                if threshold is None:
                    continue
                
                if self._is_threshold_breached(benchmark.benchmark_type, primary_metric, threshold):
                    severity = AlertSeverity(severity_name.upper())
                    alert = AlertFactory.create_threshold_alert(benchmark, severity, primary_metric, threshold)
                    alerts.append(alert)
                    break  # Only create one threshold alert per benchmark
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Failed to check threshold breaches: {e}")
            return []
    
    def _check_type_specific_issues(self, benchmark: PerformanceBenchmark) -> List:
        """Check for benchmark type specific issues"""
        alerts = []
        
        try:
            if benchmark.benchmark_type == BenchmarkType.RELIABILITY:
                alerts.extend(self._check_reliability_issues(benchmark))
            elif benchmark.benchmark_type == BenchmarkType.SCALABILITY:
                alerts.extend(self._check_scalability_issues(benchmark))
            elif benchmark.benchmark_type == BenchmarkType.THROUGHPUT:
                alerts.extend(self._check_throughput_issues(benchmark))
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Failed to check type specific issues: {e}")
            return []
    
    def _check_reliability_issues(self, benchmark: PerformanceBenchmark) -> List:
        """Check for reliability specific issues"""
        alerts = []
        
        success_rate = benchmark.metrics.get("success_rate_percent", 100)
        failed_ops = benchmark.metrics.get("failed_operations", 0)
        
        if failed_ops > 0:
            alert = AlertFactory.create_reliability_alert(benchmark, failed_ops, success_rate)
            alerts.append(alert)
        
        return alerts
    
    def _check_scalability_issues(self, benchmark: PerformanceBenchmark) -> List:
        """Check for scalability specific issues"""
        alerts = []
        
        scalability_score = benchmark.metrics.get("scalability_score", 100)
        
        if scalability_score < 50:
            alert = AlertFactory.create_scalability_alert(benchmark, scalability_score)
            alerts.append(alert)
        
        return alerts
    
    def _check_throughput_issues(self, benchmark: PerformanceBenchmark) -> List:
        """Check for throughput specific issues"""
        alerts = []
        
        throughput = benchmark.metrics.get("throughput_ops_per_sec", 0)
        
        if throughput < 100:  # Very low throughput
            alert = AlertFactory.create_throughput_alert(benchmark, throughput)
            alerts.append(alert)
        
        return alerts
    
    def _get_primary_metric_value(self, benchmark: PerformanceBenchmark) -> Optional[float]:
        """Get the primary metric value for a benchmark type"""
        metric_mappings = {
            BenchmarkType.RESPONSE_TIME: "average_response_time",
            BenchmarkType.THROUGHPUT: "throughput_ops_per_sec",
            BenchmarkType.SCALABILITY: "scalability_score",
            BenchmarkType.RELIABILITY: "success_rate_percent",
            BenchmarkType.LATENCY: "average_latency",
        }
        
        primary_key = metric_mappings.get(benchmark.benchmark_type)
        return benchmark.metrics.get(primary_key) if primary_key else None
    
    def _is_threshold_breached(self, benchmark_type: BenchmarkType, 
                             actual_value: float, threshold: float) -> bool:
        """Check if a threshold is breached based on benchmark type"""
        # For response time and latency, higher values are worse
        if benchmark_type in {BenchmarkType.RESPONSE_TIME, BenchmarkType.LATENCY}:
            return actual_value > threshold
        
        # For throughput, reliability, and scalability, lower values are worse
        else:
            return actual_value < threshold

