#!/usr/bin/env python3
"""
Validation Analytics Processor
===============================

Processes validation analytics for BI engine enhancement.
Tracks validation success rates, identifies patterns, provides insights.

Part of Agent-5's BI Engine Enhancement mission.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-10-17
Mission: Cycle 4 - BI Engine Analytics Enhancement
"""

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ValidationMetric:
    """Single validation metric data point."""
    
    function_name: str
    success: bool
    timestamp: datetime = field(default_factory=datetime.now)
    execution_time_ms: float = 0.0
    error_message: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


class ValidationAnalyticsProcessor:
    """
    Processes validation metrics for BI analytics.
    
    Features:
    - Success rate tracking per function
    - Performance monitoring
    - Error pattern analysis
    - Trend detection
    - Insights generation
    """
    
    def __init__(self):
        """Initialize analytics processor."""
        self.metrics: List[ValidationMetric] = []
        self.function_stats: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                'total_calls': 0,
                'successes': 0,
                'failures': 0,
                'avg_time_ms': 0.0,
                'errors': []
            }
        )
    
    def record_validation(self, metric: ValidationMetric) -> None:
        """
        Record a validation metric.
        
        Args:
            metric: Validation metric to record
        """
        self.metrics.append(metric)
        
        # Update function stats
        stats = self.function_stats[metric.function_name]
        stats['total_calls'] += 1
        
        if metric.success:
            stats['successes'] += 1
        else:
            stats['failures'] += 1
            if metric.error_message:
                stats['errors'].append(metric.error_message)
        
        # Update average time
        total_time = stats['avg_time_ms'] * (stats['total_calls'] - 1)
        stats['avg_time_ms'] = (total_time + metric.execution_time_ms) / stats['total_calls']
    
    def get_success_rate(self, function_name: Optional[str] = None) -> float:
        """
        Get success rate for function or overall.
        
        Args:
            function_name: Specific function, or None for overall
            
        Returns:
            Success rate as percentage (0-100)
        """
        if function_name:
            stats = self.function_stats.get(function_name)
            if not stats or stats['total_calls'] == 0:
                return 0.0
            return (stats['successes'] / stats['total_calls']) * 100
        
        # Overall success rate
        total = sum(s['total_calls'] for s in self.function_stats.values())
        if total == 0:
            return 0.0
        
        successes = sum(s['successes'] for s in self.function_stats.values())
        return (successes / total) * 100
    
    def get_function_stats(self, function_name: str) -> Dict[str, Any]:
        """Get statistics for specific function."""
        return self.function_stats.get(function_name, {})
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get all function statistics."""
        return dict(self.function_stats)
    
    def get_top_failures(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Get functions with most failures.
        
        Args:
            limit: Number of results to return
            
        Returns:
            List of (function_name, failure_count) tuples
        """
        failures = [
            (func, stats['failures'])
            for func, stats in self.function_stats.items()
            if stats['failures'] > 0
        ]
        return sorted(failures, key=lambda x: x[1], reverse=True)[:limit]
    
    def get_slowest_functions(self, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Get slowest validation functions.
        
        Args:
            limit: Number of results
            
        Returns:
            List of (function_name, avg_time_ms) tuples
        """
        times = [
            (func, stats['avg_time_ms'])
            for func, stats in self.function_stats.items()
            if stats['avg_time_ms'] > 0
        ]
        return sorted(times, key=lambda x: x[1], reverse=True)[:limit]
    
    def generate_insights(self) -> List[str]:
        """
        Generate actionable insights from analytics.
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Overall success rate insight
        overall_success = self.get_success_rate()
        if overall_success < 80:
            insights.append(
                f"⚠️ Overall validation success rate is {overall_success:.1f}% "
                f"(target: 80%+). Review failing validations."
            )
        elif overall_success > 95:
            insights.append(
                f"✅ Excellent validation success rate: {overall_success:.1f}%!"
            )
        
        # Top failures insight
        top_failures = self.get_top_failures(5)
        if top_failures:
            worst_func, worst_count = top_failures[0]
            insights.append(
                f"🔴 {worst_func} has {worst_count} failures - needs investigation"
            )
        
        # Performance insight
        slowest = self.get_slowest_functions(5)
        if slowest:
            slow_func, slow_time = slowest[0]
            if slow_time > 100:  # >100ms is slow
                insights.append(
                    f"🐌 {slow_func} averaging {slow_time:.1f}ms - consider optimization"
                )
        
        # Usage patterns
        total_validations = sum(s['total_calls'] for s in self.function_stats.values())
        if total_validations > 0:
            insights.append(
                f"📊 Total validations processed: {total_validations}"
            )
        
        return insights
    
    def get_summary_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive summary report.
        
        Returns:
            Dictionary with complete analytics summary
        """
        return {
            'overall_success_rate': self.get_success_rate(),
            'total_validations': sum(s['total_calls'] for s in self.function_stats.values()),
            'unique_functions': len(self.function_stats),
            'top_failures': self.get_top_failures(10),
            'slowest_functions': self.get_slowest_functions(10),
            'insights': self.generate_insights(),
            'function_stats': self.get_all_stats()
        }
    
    def export_metrics(self, filepath: str) -> bool:
        """
        Export metrics to JSON file.
        
        Args:
            filepath: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import json
            from pathlib import Path
            
            data = {
                'generated_at': datetime.now().isoformat(),
                'metrics_count': len(self.metrics),
                'summary': self.get_summary_report()
            }
            
            Path(filepath).write_text(json.dumps(data, indent=2))
            return True
        
        except Exception as e:
            print(f"Error exporting metrics: {e}")
            return False


# Global instance for application-wide use
_analytics_processor = ValidationAnalyticsProcessor()


def get_analytics_processor() -> ValidationAnalyticsProcessor:
    """Get global analytics processor instance."""
    return _analytics_processor


def record_validation_metric(function_name: str, success: bool,
                             execution_time_ms: float = 0.0,
                             error_message: Optional[str] = None,
                             **context) -> None:
    """
    Convenience function to record validation metric.
    
    Args:
        function_name: Name of validation function
        success: Whether validation succeeded
        execution_time_ms: Execution time in milliseconds
        error_message: Error message if failed
        **context: Additional context data
    """
    metric = ValidationMetric(
        function_name=function_name,
        success=success,
        execution_time_ms=execution_time_ms,
        error_message=error_message,
        context=context
    )
    _analytics_processor.record_validation(metric)

