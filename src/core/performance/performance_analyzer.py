#!/usr/bin/env python3
"""
Performance Analyzer - Agent Cellphone V2
========================================

Analyzes performance metrics and generates insights.

Author: Agent-8 (SSOT Maintenance & System Integration Specialist)
License: MIT
"""

import statistics
from typing import Dict, List, Any
from datetime import datetime, timedelta
from collections import defaultdict

from .metrics_models import PerformanceMetric
from .performance_collector import PerformanceCollector


class PerformanceAnalyzer:
    """Analyzes performance metrics and generates insights."""
    
    def __init__(self, collector: PerformanceCollector):
        """Initialize the performance analyzer."""
        self.collector = collector
    
    def calculate_statistics(self, metrics: List[PerformanceMetric]) -> Dict[str, float]:
        """Calculate statistical measures for a list of metrics."""
        if not metrics:
            return {}
        
        values = [m.value for m in metrics]
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "total": sum(values)
        }
    
    def analyze_response_times(self, operation_name: str, 
                             time_window: timedelta = timedelta(hours=1)) -> Dict[str, Any]:
        """Analyze response times for a specific operation."""
        end_time = datetime.now()
        start_time = end_time - time_window
        
        metrics = self.collector.get_metrics(
            name=f"{operation_name}_response_time",
            start_time=start_time,
            end_time=end_time
        )
        
        if not metrics:
            return {"operation": operation_name, "no_data": True}
        
        stats = self.calculate_statistics(metrics)
        
        # Calculate percentiles
        values = [m.value for m in metrics]
        values.sort()
        
        percentiles = {}
        for p in [50, 75, 90, 95, 99]:
            index = int(len(values) * p / 100)
            percentiles[f"p{p}"] = values[index] if index < len(values) else values[-1]
        
        return {
            "operation": operation_name,
            "time_window": str(time_window),
            "statistics": stats,
            "percentiles": percentiles,
            "trend": self._calculate_trend(metrics)
        }
    
    def analyze_throughput(self, operation_name: str,
                          time_window: timedelta = timedelta(hours=1)) -> Dict[str, Any]:
        """Analyze throughput for a specific operation."""
        end_time = datetime.now()
        start_time = end_time - time_window
        
        metrics = self.collector.get_metrics(
            name=f"{operation_name}_throughput",
            start_time=start_time,
            end_time=end_time
        )
        
        if not metrics:
            return {"operation": operation_name, "no_data": True}
        
        # Group metrics by time intervals for throughput calculation
        interval_seconds = 60  # 1-minute intervals
        intervals = defaultdict(list)
        
        for metric in metrics:
            interval_start = int(metric.timestamp.timestamp() // interval_seconds) * interval_seconds
            intervals[interval_start].append(metric.value)
        
        # Calculate throughput per interval
        throughput_per_interval = []
        for interval_start, values in intervals.items():
            throughput_per_interval.append({
                "timestamp": datetime.fromtimestamp(interval_start),
                "throughput": sum(values)
            })
        
        # Sort by timestamp
        throughput_per_interval.sort(key=lambda x: x["timestamp"])
        
        return {
            "operation": operation_name,
            "time_window": str(time_window),
            "throughput_per_interval": throughput_per_interval,
            "average_throughput": statistics.mean([t["throughput"] for t in throughput_per_interval]),
            "peak_throughput": max([t["throughput"] for t in throughput_per_interval]),
            "trend": self._calculate_trend(metrics)
        }
    
    def _calculate_trend(self, metrics: List[PerformanceMetric]) -> str:
        """Calculate trend direction for metrics."""
        if len(metrics) < 2:
            return "insufficient_data"
        
        # Split metrics into two halves
        mid_point = len(metrics) // 2
        first_half = metrics[:mid_point]
        second_half = metrics[mid_point:]
        
        first_avg = statistics.mean([m.value for m in first_half])
        second_avg = statistics.mean([m.value for m in second_half])
        
        change_percent = ((second_avg - first_avg) / first_avg) * 100
        
        if change_percent > 5:
            return "improving"
        elif change_percent < -5:
            return "degrading"
        else:
            return "stable"
    
    def generate_performance_report(self, time_window: timedelta = timedelta(hours=1)) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        end_time = datetime.now()
        start_time = end_time - time_window
        
        all_metrics = self.collector.get_metrics(start_time=start_time, end_time=end_time)
        
        # Group metrics by name
        metrics_by_name = defaultdict(list)
        for metric in all_metrics:
            metrics_by_name[metric.name].append(metric)
        
        # Analyze each metric group
        analysis_results = {}
        for name, metrics in metrics_by_name.items():
            if "response_time" in name:
                operation = name.replace("_response_time", "")
                analysis_results[name] = self.analyze_response_times(operation, time_window)
            elif "throughput" in name:
                operation = name.replace("_throughput", "")
                analysis_results[name] = self.analyze_throughput(operation, time_window)
            else:
                analysis_results[name] = self.calculate_statistics(metrics)
        
        return {
            "report_timestamp": datetime.now(),
            "time_window": str(time_window),
            "total_metrics": len(all_metrics),
            "metric_groups": len(metrics_by_name),
            "analysis": analysis_results,
            "summary": self._generate_summary(analysis_results)
        }
    
    def _generate_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of performance analysis."""
        summary = {
            "total_operations": 0,
            "operations_with_issues": 0,
            "performance_score": 100.0
        }
        
        for name, result in analysis_results.items():
            if "no_data" in result:
                continue
            
            summary["total_operations"] += 1
            
            # Check for performance issues
            if "statistics" in result:
                stats = result["statistics"]
                if "mean" in stats and stats["mean"] > 5.0:  # Response time > 5s
                    summary["operations_with_issues"] += 1
                    summary["performance_score"] -= 10
            
            if "average_throughput" in result:
                throughput = result["average_throughput"]
                if throughput < 100:  # Throughput < 100
                    summary["operations_with_issues"] += 1
                    summary["performance_score"] -= 10
        
        summary["performance_score"] = max(0.0, summary["performance_score"])
        summary["health_status"] = self._get_health_status(summary["performance_score"])
        
        return summary
    
    def _get_health_status(self, performance_score: float) -> str:
        """Get health status based on performance score."""
        if performance_score >= 90:
            return "EXCELLENT"
        elif performance_score >= 75:
            return "GOOD"
        elif performance_score >= 60:
            return "FAIR"
        else:
            return "POOR"
