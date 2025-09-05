"""
Performance Benchmark Reporter
=============================

Reporting engine for performance benchmark results.
V2 Compliance: < 300 lines, single responsibility, report generation.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from .models import BenchmarkResult, PerformanceMetrics, BenchmarkType
from .metrics import BenchmarkMetrics


class BenchmarkReporter:
    """Reporting engine for performance benchmark results."""
    
    def __init__(self, metrics: BenchmarkMetrics):
        """Initialize reporter with metrics collector."""
        self.metrics = metrics
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate summary report of all benchmarks."""
        summary_stats = self.metrics.get_summary_statistics()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_benchmarks': len(self.metrics.results),
            'benchmark_types': list(BenchmarkType),
            'summary_statistics': summary_stats,
            'overall_health': self._calculate_overall_health(summary_stats)
        }
    
    def generate_detailed_report(self, benchmark_type: Optional[BenchmarkType] = None) -> Dict[str, Any]:
        """Generate detailed report for specific benchmark type or all types."""
        if benchmark_type:
            results = self.metrics.get_results_by_type(benchmark_type)
            metrics = self.metrics.get_performance_metrics(benchmark_type)
        else:
            results = self.metrics.results
            metrics = None
        
        return {
            'timestamp': datetime.now().isoformat(),
            'benchmark_type': benchmark_type.value if benchmark_type else 'all',
            'total_results': len(results),
            'results': [
                {
                    'test_name': result.test_name,
                    'value': result.value,
                    'unit': result.unit,
                    'timestamp': result.timestamp.isoformat(),
                    'success': result.success,
                    'error_message': result.error_message,
                    'metadata': result.metadata
                }
                for result in results
            ],
            'performance_metrics': metrics.__dict__ if metrics else None
        }
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate performance-focused report."""
        performance_data = {}
        
        for benchmark_type in BenchmarkType:
            metrics = self.metrics.get_performance_metrics(benchmark_type)
            performance_data[benchmark_type.value] = {
                'average': metrics.average_value,
                'min': metrics.min_value,
                'max': metrics.max_value,
                'median': metrics.median_value,
                'percentile_95': metrics.percentile_95,
                'percentile_99': metrics.percentile_99,
                'success_rate': metrics.success_rate,
                'total_iterations': metrics.total_iterations
            }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'performance_data': performance_data,
            'recommendations': self._generate_performance_recommendations(performance_data)
        }
    
    def generate_error_report(self) -> Dict[str, Any]:
        """Generate error-focused report."""
        error_results = [result for result in self.metrics.results if not result.success]
        
        # Group errors by type
        error_types = {}
        for result in error_results:
            error_type = result.error_message or 'unknown_error'
            if error_type not in error_types:
                error_types[error_type] = []
            error_types[error_type].append(result)
        
        # Calculate error statistics
        error_stats = {}
        for error_type, results in error_types.items():
            error_stats[error_type] = {
                'count': len(results),
                'percentage': (len(results) / len(self.metrics.results) * 100) if self.metrics.results else 0,
                'benchmark_types': list(set(result.benchmark_type.value for result in results)),
                'test_names': list(set(result.test_name for result in results))
            }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_errors': len(error_results),
            'error_rate': (len(error_results) / len(self.metrics.results) * 100) if self.metrics.results else 0,
            'error_types': error_stats,
            'recommendations': self._generate_error_recommendations(error_stats)
        }
    
    def generate_comparison_report(self, baseline_results: List[BenchmarkResult]) -> Dict[str, Any]:
        """Generate comparison report against baseline results."""
        comparison_data = {}
        
        # Group current results by benchmark type
        current_by_type = {}
        for result in self.metrics.results:
            if result.benchmark_type not in current_by_type:
                current_by_type[result.benchmark_type] = []
            current_by_type[result.benchmark_type].append(result)
        
        # Group baseline results by benchmark type
        baseline_by_type = {}
        for result in baseline_results:
            if result.benchmark_type not in baseline_by_type:
                baseline_by_type[result.benchmark_type] = []
            baseline_by_type[result.benchmark_type].append(result)
        
        # Compare each benchmark type
        for benchmark_type in BenchmarkType:
            current_results = current_by_type.get(benchmark_type, [])
            baseline_results_type = baseline_by_type.get(benchmark_type, [])
            
            if not current_results or not baseline_results_type:
                continue
            
            current_avg = sum(r.value for r in current_results if r.success) / len([r for r in current_results if r.success]) if any(r.success for r in current_results) else 0
            baseline_avg = sum(r.value for r in baseline_results_type if r.success) / len([r for r in baseline_results_type if r.success]) if any(r.success for r in baseline_results_type) else 0
            
            if baseline_avg > 0:
                improvement = ((baseline_avg - current_avg) / baseline_avg) * 100
            else:
                improvement = 0
            
            comparison_data[benchmark_type.value] = {
                'current_average': current_avg,
                'baseline_average': baseline_avg,
                'improvement_percentage': improvement,
                'is_improved': improvement > 0
            }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'comparison_data': comparison_data,
            'overall_improvement': self._calculate_overall_improvement(comparison_data)
        }
    
    def _calculate_overall_health(self, summary_stats: Dict[str, Any]) -> str:
        """Calculate overall health rating."""
        if not summary_stats:
            return 'unknown'
        
        # Check error rates
        error_rates = []
        for stats in summary_stats.values():
            if 'success_rate' in stats:
                error_rate = 100 - stats['success_rate']
                error_rates.append(error_rate)
        
        if not error_rates:
            return 'unknown'
        
        avg_error_rate = sum(error_rates) / len(error_rates)
        
        if avg_error_rate > 20:
            return 'poor'
        elif avg_error_rate > 10:
            return 'fair'
        elif avg_error_rate > 5:
            return 'good'
        else:
            return 'excellent'
    
    def _generate_performance_recommendations(self, performance_data: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations."""
        recommendations = []
        
        for benchmark_type, data in performance_data.items():
            if benchmark_type == 'response_time':
                if data['average'] > 1000:  # > 1 second
                    recommendations.append(f"Response time is high ({data['average']:.2f}ms). Consider optimization.")
                elif data['percentile_95'] > 2000:  # > 2 seconds
                    recommendations.append(f"95th percentile response time is very high ({data['percentile_95']:.2f}ms).")
            
            elif benchmark_type == 'memory_usage':
                if data['average'] > 100:  # > 100 MB
                    recommendations.append(f"Memory usage is high ({data['average']:.2f}MB). Consider memory optimization.")
            
            elif benchmark_type == 'cpu_usage':
                if data['average'] > 80:  # > 80%
                    recommendations.append(f"CPU usage is high ({data['average']:.2f}%). Consider load balancing.")
            
            elif benchmark_type == 'error_rate':
                if data['average'] > 5:  # > 5%
                    recommendations.append(f"Error rate is high ({data['average']:.2f}%). Review error handling.")
        
        if not recommendations:
            recommendations.append("Performance metrics look good. Continue monitoring.")
        
        return recommendations
    
    def _generate_error_recommendations(self, error_stats: Dict[str, Any]) -> List[str]:
        """Generate error recommendations."""
        recommendations = []
        
        if not error_stats:
            recommendations.append("No errors detected. Continue monitoring.")
            return recommendations
        
        # Find most common error
        most_common_error = max(error_stats.items(), key=lambda x: x[1]['count'])
        error_type, stats = most_common_error
        
        if stats['count'] > 0:
            recommendations.append(f"Most common error: {error_type} ({stats['count']} occurrences). Focus on fixing this issue.")
        
        # Check error rate
        total_errors = sum(stats['count'] for stats in error_stats.values())
        total_tests = len(self.metrics.results)
        error_rate = (total_errors / total_tests * 100) if total_tests > 0 else 0
        
        if error_rate > 10:
            recommendations.append(f"High error rate ({error_rate:.2f}%). Implement better error handling.")
        
        if not recommendations:
            recommendations.append("Error analysis shows good stability. Continue monitoring.")
        
        return recommendations
    
    def _calculate_overall_improvement(self, comparison_data: Dict[str, Any]) -> float:
        """Calculate overall improvement percentage."""
        if not comparison_data:
            return 0.0
        
        improvements = [data['improvement_percentage'] for data in comparison_data.values()]
        return sum(improvements) / len(improvements) if improvements else 0.0
