#!/usr/bin/env python3
"""
Advanced Performance Profiling Tools
Contract: PERF-005 - Advanced Performance Profiling Tools
Agent: Agent-6 (Performance Optimization Manager)
Description: Comprehensive performance profiling and analysis system
"""

import time
import cProfile
import pstats
import io
import psutil
import threading
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProfilingMetrics:
    """Data structure for storing profiling metrics"""
    function_name: str
    call_count: int
    total_time: float
    average_time: float
    min_time: float
    max_time: float
    memory_usage: float
    cpu_usage: float
    timestamp: str

@dataclass
class SystemMetrics:
    """System-level performance metrics"""
    cpu_percent: float
    memory_percent: float
    memory_available: float
    disk_io_read: float
    disk_io_write: float
    network_io_sent: float
    network_io_recv: float
    timestamp: str

class PerformanceProfiler:
    """
    Advanced Performance Profiling Tools
    
    Features:
    - Function-level profiling with detailed metrics
    - System resource monitoring
    - Memory usage tracking
    - CPU utilization analysis
    - Automated profiling reports
    - Real-time monitoring capabilities
    """
    
    def __init__(self, output_dir: str = "profiling_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.profiling_data: Dict[str, ProfilingMetrics] = {}
        self.system_metrics: List[SystemMetrics] = []
        self.active_profilers: Dict[str, cProfile.Profile] = {}
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Performance thresholds
        self.performance_thresholds = {
            'function_time_warning': 1.0,  # seconds
            'memory_usage_warning': 80.0,  # percent
            'cpu_usage_warning': 90.0      # percent
        }
        
        logger.info("Performance Profiler initialized")
    
    def start_function_profiling(self, function_name: str) -> str:
        """
        Start profiling a specific function
        
        Args:
            function_name: Name of the function to profile
            
        Returns:
            Profiler ID for stopping the profiler
        """
        profiler_id = f"{function_name}_{int(time.time())}"
        
        if profiler_id in self.active_profilers:
            logger.warning(f"Profiler {profiler_id} already active")
            return profiler_id
        
        profiler = cProfile.Profile()
        profiler.enable()
        self.active_profilers[profiler_id] = profiler
        
        logger.info(f"Started profiling function: {function_name}")
        return profiler_id
    
    def stop_function_profiling(self, profiler_id: str) -> Optional[ProfilingMetrics]:
        """
        Stop profiling and collect metrics
        
        Args:
            profiler_id: ID returned from start_function_profiling
            
        Returns:
            Profiling metrics or None if profiler not found
        """
        if profiler_id not in self.active_profilers:
            logger.error(f"Profiler {profiler_id} not found")
            return None
        
        profiler = self.active_profilers[profiler_id]
        profiler.disable()
        
        # Collect profiling statistics
        stats = pstats.Stats(profiler)
        
        # Get function statistics
        function_stats = {}
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            func_name = f"{func[0]}:{func[1]}:{func[2]}"
            function_stats[func_name] = {
                'call_count': cc,
                'total_time': tt,
                'cumulative_time': ct
            }
        
        # Calculate metrics
        if function_stats:
            main_func = list(function_stats.keys())[0]
            stats_data = function_stats[main_func]
            
            metrics = ProfilingMetrics(
                function_name=main_func,
                call_count=stats_data['call_count'],
                total_time=stats_data['total_time'],
                average_time=stats_data['total_time'] / stats_data['call_count'] if stats_data['call_count'] > 0 else 0,
                min_time=stats_data['total_time'],  # Simplified for now
                max_time=stats_data['total_time'],  # Simplified for now
                memory_usage=psutil.virtual_memory().percent,
                cpu_usage=psutil.cpu_percent(),
                timestamp=datetime.now().isoformat()
            )
            
            # Store metrics
            self.profiling_data[profiler_id] = metrics
            
            # Clean up
            del self.active_profilers[profiler_id]
            
            logger.info(f"Stopped profiling {profiler_id}, collected metrics")
            return metrics
        
        return None
    
    def profile_function(self, func: Callable, *args, **kwargs) -> ProfilingMetrics:
        """
        Profile a function execution
        
        Args:
            func: Function to profile
            *args, **kwargs: Function arguments
            
        Returns:
            Profiling metrics
        """
        function_name = func.__name__
        profiler_id = self.start_function_profiling(function_name)
        
        try:
            start_time = time.time()
            start_memory = psutil.virtual_memory().percent
            start_cpu = psutil.cpu_percent()
            
            # Execute function
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = psutil.virtual_memory().percent
            end_cpu = psutil.cpu_percent()
            
            # Create metrics manually for better accuracy
            execution_time = end_time - start_time
            metrics = ProfilingMetrics(
                function_name=function_name,
                call_count=1,
                total_time=execution_time,
                average_time=execution_time,
                min_time=execution_time,
                max_time=execution_time,
                memory_usage=(start_memory + end_memory) / 2,
                cpu_usage=(start_cpu + end_cpu) / 2,
                timestamp=datetime.now().isoformat()
            )
            
            self.profiling_data[profiler_id] = metrics
            logger.info(f"Profiled function {function_name}: {execution_time:.4f}s")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error profiling function {function_name}: {e}")
            # Clean up profiler
            if profiler_id in self.active_profilers:
                del self.active_profilers[profiler_id]
            raise
    
    def start_system_monitoring(self, interval: float = 1.0):
        """
        Start continuous system monitoring
        
        Args:
            interval: Monitoring interval in seconds
        """
        if self.monitoring_active:
            logger.warning("System monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitoring_thread.start()
        logger.info(f"Started system monitoring with {interval}s interval")
    
    def stop_system_monitoring(self):
        """Stop system monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
        logger.info("Stopped system monitoring")
    
    def _monitoring_loop(self, interval: float):
        """Internal monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                cpu_percent = psutil.cpu_percent()
                memory = psutil.virtual_memory()
                disk_io = psutil.disk_io_counters()
                network_io = psutil.net_io_counters()
                
                metrics = SystemMetrics(
                    cpu_percent=cpu_percent,
                    memory_percent=memory.percent,
                    memory_available=memory.available / (1024**3),  # GB
                    disk_io_read=disk_io.read_bytes / (1024**2) if disk_io else 0,  # MB
                    disk_io_write=disk_io.write_bytes / (1024**2) if disk_io else 0,  # MB
                    network_io_sent=network_io.bytes_sent / (1024**2) if network_io else 0,  # MB
                    network_io_recv=network_io.bytes_recv / (1024**2) if network_io else 0,  # MB
                    timestamp=datetime.now().isoformat()
                )
                
                self.system_metrics.append(metrics)
                
                # Check thresholds and log warnings
                if cpu_percent > self.performance_thresholds['cpu_usage_warning']:
                    logger.warning(f"High CPU usage: {cpu_percent}%")
                
                if memory.percent > self.performance_thresholds['memory_usage_warning']:
                    logger.warning(f"High memory usage: {memory.percent}%")
                
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def generate_profiling_report(self, output_file: Optional[str] = None) -> str:
        """
        Generate comprehensive profiling report
        
        Args:
            output_file: Optional output file path
            
        Returns:
            Path to generated report
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"profiling_report_{timestamp}.json"
        
        report_data = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'profiler_version': '1.0.0',
                'total_functions_profiled': len(self.profiling_data),
                'monitoring_duration': len(self.system_metrics) if self.system_metrics else 0
            },
            'function_metrics': [asdict(metrics) for metrics in self.profiling_data.values()],
            'system_metrics': [asdict(metrics) for metrics in self.system_metrics],
            'performance_analysis': self._analyze_performance(),
            'recommendations': self._generate_recommendations()
        }
        
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Generated profiling report: {output_file}")
        return str(output_file)
    
    def _analyze_performance(self) -> Dict[str, Any]:
        """Analyze collected performance data"""
        if not self.profiling_data:
            return {'status': 'No profiling data available'}
        
        # Calculate performance statistics
        total_time = sum(m.total_time for m in self.profiling_data.values())
        avg_time = total_time / len(self.profiling_data)
        max_time = max(m.total_time for m in self.profiling_data.values())
        
        # Identify performance bottlenecks
        bottlenecks = [
            m.function_name for m in self.profiling_data.values()
            if m.total_time > self.performance_thresholds['function_time_warning']
        ]
        
        return {
            'total_execution_time': total_time,
            'average_function_time': avg_time,
            'slowest_function_time': max_time,
            'performance_bottlenecks': bottlenecks,
            'functions_profiled': len(self.profiling_data)
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        if not self.profiling_data:
            return ["No profiling data available for recommendations"]
        
        # Analyze function performance
        slow_functions = [
            m.function_name for m in self.profiling_data.values()
            if m.total_time > self.performance_thresholds['function_time_warning']
        ]
        
        if slow_functions:
            recommendations.append(f"Consider optimizing slow functions: {', '.join(slow_functions)}")
        
        # Analyze system metrics
        if self.system_metrics:
            avg_cpu = sum(m.cpu_percent for m in self.system_metrics) / len(self.system_metrics)
            avg_memory = sum(m.memory_percent for m in self.system_metrics) / len(self.system_metrics)
            
            if avg_cpu > 70:
                recommendations.append("High average CPU usage detected - consider load balancing or optimization")
            
            if avg_memory > 80:
                recommendations.append("High average memory usage detected - consider memory optimization")
        
        if not recommendations:
            recommendations.append("Performance appears to be within acceptable thresholds")
        
        return recommendations
    
    def clear_data(self):
        """Clear all collected profiling data"""
        self.profiling_data.clear()
        self.system_metrics.clear()
        self.active_profilers.clear()
        logger.info("Cleared all profiling data")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of current profiling status"""
        return {
            'active_profilers': len(self.active_profilers),
            'functions_profiled': len(self.profiling_data),
            'system_metrics_collected': len(self.system_metrics),
            'monitoring_active': self.monitoring_active,
            'output_directory': str(self.output_dir)
        }


# Convenience function for quick profiling
def quick_profile(func: Callable, *args, **kwargs) -> ProfilingMetrics:
    """
    Quick profiling of a function
    
    Args:
        func: Function to profile
        *args, **kwargs: Function arguments
        
    Returns:
        Profiling metrics
    """
    profiler = PerformanceProfiler()
    return profiler.profile_function(func, *args, **kwargs)


if __name__ == "__main__":
    # Example usage
    def example_function():
        """Example function for profiling demonstration"""
        time.sleep(0.1)
        return "Hello, World!"
    
    # Create profiler instance
    profiler = PerformanceProfiler()
    
    # Profile a function
    metrics = profiler.profile_function(example_function)
    print(f"Function profiled: {metrics.function_name}")
    print(f"Execution time: {metrics.total_time:.4f}s")
    
    # Generate report
    report_file = profiler.generate_profiling_report()
    print(f"Report generated: {report_file}")
