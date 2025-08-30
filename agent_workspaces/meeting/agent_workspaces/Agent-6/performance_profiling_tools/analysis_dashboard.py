#!/usr/bin/env python3
"""
Performance Analysis Dashboard
Contract: PERF-005 - Advanced Performance Profiling Tools
Agent: Agent-6 (Performance Optimization Manager)
Description: Interactive dashboard for analyzing performance profiling data
"""

import json
import time
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceAnalysisDashboard:
    """
    Performance Analysis Dashboard
    
    Features:
    - Real-time performance metrics visualization
    - Historical trend analysis
    - Performance bottleneck identification
    - Automated performance insights
    - Customizable performance thresholds
    - Export capabilities for reports
    """
    
    def __init__(self, profiler_data_file: Optional[str] = None):
        self.profiler_data_file = profiler_data_file
        self.performance_data: Dict[str, Any] = {}
        self.analysis_results: Dict[str, Any] = {}
        self.performance_thresholds = {
            'critical_cpu': 95.0,
            'warning_cpu': 80.0,
            'critical_memory': 90.0,
            'warning_memory': 75.0,
            'critical_function_time': 5.0,
            'warning_function_time': 1.0
        }
        
        if profiler_data_file:
            self.load_profiler_data(profiler_data_file)
        
        logger.info("Performance Analysis Dashboard initialized")
    
    def load_profiler_data(self, data_file: str) -> bool:
        """
        Load profiling data from file
        
        Args:
            data_file: Path to profiling data file
            
        Returns:
            True if data loaded successfully
        """
        try:
            with open(data_file, 'r') as f:
                self.performance_data = json.load(f)
            logger.info(f"Loaded profiling data from {data_file}")
            return True
        except Exception as e:
            logger.error(f"Error loading profiling data: {e}")
            return False
    
    def analyze_performance_trends(self) -> Dict[str, Any]:
        """
        Analyze performance trends over time
        
        Returns:
            Dictionary containing trend analysis
        """
        if not self.performance_data:
            return {'error': 'No performance data available'}
        
        trends = {
            'cpu_trends': self._analyze_cpu_trends(),
            'memory_trends': self._analyze_memory_trends(),
            'function_performance_trends': self._analyze_function_trends(),
            'system_health_score': self._calculate_system_health_score()
        }
        
        self.analysis_results['trends'] = trends
        return trends
    
    def _analyze_cpu_trends(self) -> Dict[str, Any]:
        """Analyze CPU usage trends"""
        if 'system_metrics' not in self.performance_data:
            return {'error': 'No system metrics available'}
        
        cpu_values = [m['cpu_percent'] for m in self.performance_data['system_metrics']]
        
        if not cpu_values:
            return {'error': 'No CPU data available'}
        
        return {
            'current_cpu': cpu_values[-1] if cpu_values else 0,
            'average_cpu': statistics.mean(cpu_values),
            'max_cpu': max(cpu_values),
            'min_cpu': min(cpu_values),
            'cpu_variance': statistics.variance(cpu_values) if len(cpu_values) > 1 else 0,
            'cpu_trend': self._calculate_trend_direction(cpu_values),
            'high_cpu_periods': len([v for v in cpu_values if v > self.performance_thresholds['warning_cpu']]),
            'critical_cpu_periods': len([v for v in cpu_values if v > self.performance_thresholds['critical_cpu']])
        }
    
    def _analyze_memory_trends(self) -> Dict[str, Any]:
        """Analyze memory usage trends"""
        if 'system_metrics' not in self.performance_data:
            return {'error': 'No system metrics available'}
        
        memory_values = [m['memory_percent'] for m in self.performance_data['system_metrics']]
        
        if not memory_values:
            return {'error': 'No memory data available'}
        
        return {
            'current_memory': memory_values[-1] if memory_values else 0,
            'average_memory': statistics.mean(memory_values),
            'max_memory': max(memory_values),
            'min_memory': min(memory_values),
            'memory_variance': statistics.variance(memory_values) if len(memory_values) > 1 else 0,
            'memory_trend': self._calculate_trend_direction(memory_values),
            'high_memory_periods': len([v for v in memory_values if v > self.performance_thresholds['warning_memory']]),
            'critical_memory_periods': len([v for v in memory_values if v > self.performance_thresholds['critical_memory']])
        }
    
    def _analyze_function_trends(self) -> Dict[str, Any]:
        """Analyze function performance trends"""
        if 'function_metrics' not in self.performance_data:
            return {'error': 'No function metrics available'}
        
        function_data = {}
        for metric in self.performance_data['function_metrics']:
            func_name = metric['function_name']
            if func_name not in function_data:
                function_data[func_name] = []
            function_data[func_name].append(metric['total_time'])
        
        trends = {}
        for func_name, times in function_data.items():
            trends[func_name] = {
                'average_time': statistics.mean(times),
                'max_time': max(times),
                'min_time': min(times),
                'total_calls': len(times),
                'performance_trend': self._calculate_trend_direction(times),
                'is_bottleneck': any(t > self.performance_thresholds['warning_function_time'] for t in times)
            }
        
        return trends
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values"""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear regression slope
        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * v for i, v in enumerate(values))
        x_sq_sum = sum(i * i for i in range(n))
        
        try:
            slope = (n * xy_sum - x_sum * y_sum) / (n * x_sq_sum - x_sum * x_sum)
            
            if slope > 0.01:
                return 'increasing'
            elif slope < -0.01:
                return 'decreasing'
            else:
                return 'stable'
        except ZeroDivisionError:
            return 'stable'
    
    def _calculate_system_health_score(self) -> Dict[str, Any]:
        """Calculate overall system health score"""
        if not self.performance_data:
            return {'score': 0, 'status': 'No data available'}
        
        score = 100
        issues = []
        
        # Check CPU health
        if 'system_metrics' in self.performance_data:
            cpu_values = [m['cpu_percent'] for m in self.performance_data['system_metrics']]
            if cpu_values:
                avg_cpu = statistics.mean(cpu_values)
                if avg_cpu > self.performance_thresholds['critical_cpu']:
                    score -= 30
                    issues.append(f"Critical CPU usage: {avg_cpu:.1f}%")
                elif avg_cpu > self.performance_thresholds['warning_cpu']:
                    score -= 15
                    issues.append(f"High CPU usage: {avg_cpu:.1f}%")
        
        # Check memory health
        if 'system_metrics' in self.performance_data:
            memory_values = [m['memory_percent'] for m in self.performance_data['system_metrics']]
            if memory_values:
                avg_memory = statistics.mean(memory_values)
                if avg_memory > self.performance_thresholds['critical_memory']:
                    score -= 30
                    issues.append(f"Critical memory usage: {avg_memory:.1f}%")
                elif avg_memory > self.performance_thresholds['warning_memory']:
                    score -= 15
                    issues.append(f"High memory usage: {avg_memory:.1f}%")
        
        # Check function performance
        if 'function_metrics' in self.performance_data:
            slow_functions = [
                m for m in self.performance_data['function_metrics']
                if m['total_time'] > self.performance_thresholds['warning_function_time']
            ]
            if slow_functions:
                score -= min(20, len(slow_functions) * 5)
                issues.append(f"{len(slow_functions)} slow functions detected")
        
        # Determine status
        if score >= 90:
            status = 'Excellent'
        elif score >= 75:
            status = 'Good'
        elif score >= 60:
            status = 'Fair'
        elif score >= 40:
            status = 'Poor'
        else:
            status = 'Critical'
        
        return {
            'score': max(0, score),
            'status': status,
            'issues': issues,
            'recommendations': self._generate_health_recommendations(score, issues)
        }
    
    def _generate_health_recommendations(self, score: int, issues: List[str]) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        if score < 60:
            recommendations.append("Immediate attention required - system performance is poor")
        
        if any("CPU" in issue for issue in issues):
            recommendations.append("Consider CPU optimization, load balancing, or resource scaling")
        
        if any("memory" in issue.lower() for issue in issues):
            recommendations.append("Review memory usage patterns and implement memory optimization")
        
        if any("slow functions" in issue.lower() for issue in issues):
            recommendations.append("Profile and optimize slow-performing functions")
        
        if not recommendations:
            recommendations.append("System performance is within acceptable parameters")
        
        return recommendations
    
    def identify_performance_bottlenecks(self) -> Dict[str, Any]:
        """
        Identify performance bottlenecks in the system
        
        Returns:
            Dictionary containing bottleneck analysis
        """
        bottlenecks = {
            'cpu_bottlenecks': [],
            'memory_bottlenecks': [],
            'function_bottlenecks': [],
            'system_bottlenecks': []
        }
        
        # Analyze CPU bottlenecks
        if 'system_metrics' in self.performance_data:
            cpu_issues = [
                {
                    'timestamp': m['timestamp'],
                    'cpu_percent': m['cpu_percent'],
                    'severity': 'critical' if m['cpu_percent'] > self.performance_thresholds['critical_cpu'] else 'warning'
                }
                for m in self.performance_data['system_metrics']
                if m['cpu_percent'] > self.performance_thresholds['warning_cpu']
            ]
            bottlenecks['cpu_bottlenecks'] = cpu_issues
        
        # Analyze memory bottlenecks
        if 'system_metrics' in self.performance_data:
            memory_issues = [
                {
                    'timestamp': m['timestamp'],
                    'memory_percent': m['memory_percent'],
                    'severity': 'critical' if m['memory_percent'] > self.performance_thresholds['critical_memory'] else 'warning'
                }
                for m in self.performance_data['system_metrics']
                if m['memory_percent'] > self.performance_thresholds['warning_memory']
            ]
            bottlenecks['memory_bottlenecks'] = memory_issues
        
        # Analyze function bottlenecks
        if 'function_metrics' in self.performance_data:
            function_issues = [
                {
                    'function_name': m['function_name'],
                    'execution_time': m['total_time'],
                    'severity': 'critical' if m['total_time'] > self.performance_thresholds['critical_function_time'] else 'warning'
                }
                for m in self.performance_data['function_metrics']
                if m['total_time'] > self.performance_thresholds['warning_function_time']
            ]
            bottlenecks['function_bottlenecks'] = function_issues
        
        # Overall system bottlenecks
        total_issues = (
            len(bottlenecks['cpu_bottlenecks']) +
            len(bottlenecks['memory_bottlenecks']) +
            len(bottlenecks['function_bottlenecks'])
        )
        
        if total_issues > 10:
            bottlenecks['system_bottlenecks'].append({
                'type': 'multiple_bottlenecks',
                'description': f"System experiencing {total_issues} performance issues",
                'severity': 'critical'
            })
        
        self.analysis_results['bottlenecks'] = bottlenecks
        return bottlenecks
    
    def generate_performance_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive performance summary
        
        Returns:
            Dictionary containing performance summary
        """
        if not self.performance_data:
            return {'error': 'No performance data available'}
        
        # Analyze trends
        trends = self.analyze_performance_trends()
        
        # Identify bottlenecks
        bottlenecks = self.identify_performance_bottlenecks()
        
        # Calculate key metrics
        summary = {
            'analysis_timestamp': datetime.now().isoformat(),
            'data_summary': {
                'total_functions_profiled': len(self.performance_data.get('function_metrics', [])),
                'total_system_metrics': len(self.performance_data.get('system_metrics', [])),
                'monitoring_duration': self._calculate_monitoring_duration()
            },
            'performance_overview': {
                'system_health_score': trends.get('system_health_score', {}),
                'cpu_performance': trends.get('cpu_trends', {}),
                'memory_performance': trends.get('memory_trends', {}),
                'function_performance': trends.get('function_performance_trends', {})
            },
            'bottleneck_analysis': bottlenecks,
            'recommendations': self._generate_comprehensive_recommendations(trends, bottlenecks)
        }
        
        self.analysis_results['summary'] = summary
        return summary
    
    def _calculate_monitoring_duration(self) -> str:
        """Calculate total monitoring duration"""
        if 'system_metrics' not in self.performance_data or not self.performance_data['system_metrics']:
            return "Unknown"
        
        metrics = self.performance_data['system_metrics']
        if len(metrics) < 2:
            return "Insufficient data"
        
        start_time = datetime.fromisoformat(metrics[0]['timestamp'])
        end_time = datetime.fromisoformat(metrics[-1]['timestamp'])
        duration = end_time - start_time
        
        return str(duration)
    
    def _generate_comprehensive_recommendations(self, trends: Dict, bottlenecks: Dict) -> List[str]:
        """Generate comprehensive performance recommendations"""
        recommendations = []
        
        # System health recommendations
        health_score = trends.get('system_health_score', {})
        if health_score.get('score', 100) < 75:
            recommendations.extend(health_score.get('recommendations', []))
        
        # CPU recommendations
        cpu_trends = trends.get('cpu_trends', {})
        if cpu_trends.get('average_cpu', 0) > 70:
            recommendations.append("Consider implementing CPU load balancing or scaling")
        
        # Memory recommendations
        memory_trends = trends.get('memory_trends', {})
        if memory_trends.get('average_memory', 0) > 80:
            recommendations.append("Review memory allocation and implement memory optimization strategies")
        
        # Function performance recommendations
        function_trends = trends.get('function_performance_trends', {})
        slow_functions = [f for f, data in function_trends.items() if data.get('is_bottleneck', False)]
        if slow_functions:
            recommendations.append(f"Optimize slow-performing functions: {', '.join(slow_functions)}")
        
        # Bottleneck-specific recommendations
        if bottlenecks.get('cpu_bottlenecks'):
            recommendations.append("Address CPU bottlenecks through resource optimization or scaling")
        
        if bottlenecks.get('memory_bottlenecks'):
            recommendations.append("Address memory bottlenecks through memory management optimization")
        
        if not recommendations:
            recommendations.append("System performance is optimal - continue monitoring for early detection")
        
        return recommendations
    
    def export_analysis_report(self, output_file: Optional[str] = None) -> str:
        """
        Export complete analysis report
        
        Args:
            output_file: Optional output file path
            
        Returns:
            Path to exported report
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"performance_analysis_report_{timestamp}.json"
        
        # Generate summary if not already done
        if 'summary' not in self.analysis_results:
            self.generate_performance_summary()
        
        # Export complete analysis
        export_data = {
            'export_metadata': {
                'exported_at': datetime.now().isoformat(),
                'dashboard_version': '1.0.0',
                'analysis_timestamp': self.analysis_results.get('summary', {}).get('analysis_timestamp', '')
            },
            'performance_data': self.performance_data,
            'analysis_results': self.analysis_results
        }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Exported analysis report to {output_file}")
        return output_file
    
    def get_dashboard_status(self) -> Dict[str, Any]:
        """Get current dashboard status"""
        return {
            'data_loaded': bool(self.performance_data),
            'analysis_completed': bool(self.analysis_results),
            'data_points': len(self.performance_data.get('system_metrics', [])),
            'functions_profiled': len(self.performance_data.get('function_metrics', [])),
            'last_analysis': self.analysis_results.get('summary', {}).get('analysis_timestamp', 'Never')
        }


if __name__ == "__main__":
    # Example usage
    dashboard = PerformanceAnalysisDashboard()
    
    # Simulate some performance data
    sample_data = {
        'function_metrics': [
            {
                'function_name': 'test_function',
                'total_time': 0.5,
                'timestamp': datetime.now().isoformat()
            }
        ],
        'system_metrics': [
            {
                'cpu_percent': 45.0,
                'memory_percent': 60.0,
                'timestamp': datetime.now().isoformat()
            }
        ]
    }
    
    # Load sample data
    dashboard.performance_data = sample_data
    
    # Generate analysis
    summary = dashboard.generate_performance_summary()
    print("Performance Analysis Summary:")
    print(json.dumps(summary, indent=2))
    
    # Export report
    report_file = dashboard.export_analysis_report()
    print(f"\nReport exported to: {report_file}")
