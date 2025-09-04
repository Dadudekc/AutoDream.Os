
#!/usr/bin/env python3
"""
Coordination & Communication Performance Monitor - Agent Cellphone V2
==================================================================

Main performance monitoring system for coordination and communication.

Author: Agent-8 (SSOT Maintenance & System Integration Specialist)
License: MIT
"""

import time



class CoordinationPerformanceMonitor:
    """Main performance monitoring system for coordination and communication."""

    def __init__(self):
        """Initialize the performance monitor."""
        self.collector = PerformanceCollector()
        self.analyzer = PerformanceAnalyzer(self.collector)
        self.monitoring_active = True
        self.monitoring_thread = None

        # Start background monitoring
        self._start_background_monitoring()

    def _start_background_monitoring(self):
        """Start background monitoring thread."""

        def monitor_loop():
            while self.monitoring_active:
                try:
                    # Record system health metrics
                    self._record_system_health()
                    time.sleep(60)  # Check every minute
                except Exception as e:
                    get_logger(__name__).info(f"⚠️ Background monitoring error: {e}")
                    time.sleep(60)

        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()

    def _record_system_health(self):
        """Record system health metrics."""
        # Record memory usage (simplified)
        try:
            import psutil

            memory = psutil.virtual_memory()
            self.collector.record_metric("system_memory_usage", memory.percent)
            self.collector.record_metric(
                "system_memory_available", memory.available / (1024**3)
            )  # GB
        except ImportError:
            # psutil not available, skip memory metrics
            pass

        # Record timestamp for monitoring
        self.collector.record_metric("monitoring_heartbeat", time.time())

    def record_operation_start(self, operation_name: str, tags: Dict[str, str] = None):
        """Record the start of an operation."""
        self.collector.record_metric(
            f"{operation_name}_start", time.time(), MetricType.GAUGE, tags=tags
        )

    def record_operation_completion(
        self,
        operation_name: str,
        duration: float,
        success: bool = True,
        tags: Dict[str, str] = None,
    ):
        """Record the completion of an operation."""
        # Record response time
        self.collector.record_timer(
            f"{operation_name}_response_time", duration, tags=tags
        )

        # Record success/failure
        self.collector.record_counter(
            f"{operation_name}_success" if success else f"{operation_name}_failure",
            1.0,
            tags=tags,
        )

        # Record throughput
        self.collector.record_counter(f"{operation_name}_throughput", 1.0, tags=tags)

    def get_performance_report(
        self, time_window: timedelta = timedelta(hours=1)
    ) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        return self.analyzer.generate_performance_report(time_window)

    def get_system_health(self) -> Dict[str, Any]:
        """Get current system health status."""
        return self.analyzer._generate_summary(
            self.analyzer.generate_performance_report(timedelta(minutes=5))["analysis"]
        )

    def stop_monitoring(self):
        """Stop background monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)


# Global performance monitor instance
_performance_monitor = None


def get_performance_monitor() -> CoordinationPerformanceMonitor:
    """Get global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = CoordinationPerformanceMonitor()
    return _performance_monitor
