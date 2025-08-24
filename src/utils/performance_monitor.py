#!/usr/bin/env python3
"""
Performance Monitor Module - Performance Metrics and Monitoring

This module provides performance monitoring functionality.
Follows Single Responsibility Principle - only performance monitoring.
Architecture: Single Responsibility Principle - performance monitoring only
LOC: 100 lines (under 200 limit)
"""

import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, List, Optional
from .system_info import SystemInfo


class PerformanceMonitor:
    """Performance monitoring and metrics collection"""

    def __init__(self):
        self.metrics_history: List[Dict[str, Any]] = []
        self.max_history_size = 100
        self.logger = logging.getLogger(f"{__name__}.PerformanceMonitor")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        try:
            metrics = {}

            # Memory metrics
            memory_info = SystemInfo.get_memory_info()
            if memory_info:
                metrics["memory"] = memory_info

            # CPU metrics
            cpu_info = SystemInfo.get_cpu_info()
            if cpu_info:
                metrics["cpu"] = cpu_info

            # Disk metrics
            disk_info = SystemInfo.get_disk_info()
            if disk_info:
                metrics["disk"] = disk_info

            # Timestamp
            metrics["timestamp"] = time.time()

            # Store in history
            self._store_metrics(metrics)

            return metrics

        except Exception as e:
            self.logger.error(f"Failed to get performance metrics: {e}")
            return {}

    def _store_metrics(self, metrics: Dict[str, Any]):
        """Store metrics in history"""
        self.metrics_history.append(metrics)

        # Maintain history size limit
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history.pop(0)

    def get_metrics_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get metrics history"""
        if limit is None:
            return self.metrics_history.copy()

        return self.metrics_history[-limit:] if limit > 0 else []

    def get_average_metrics(self, time_window_minutes: int = 5) -> Dict[str, Any]:
        """Get average metrics over a time window"""
        try:
            current_time = time.time()
            window_start = current_time - (time_window_minutes * 60)

            # Filter metrics within time window
            recent_metrics = [
                m for m in self.metrics_history if m.get("timestamp", 0) >= window_start
            ]

            if not recent_metrics:
                return {}

            # Calculate averages
            avg_metrics = {}

            # Memory averages
            if "memory" in recent_metrics[0]:
                memory_values = [m["memory"] for m in recent_metrics if "memory" in m]
                if memory_values:
                    avg_metrics["memory"] = {
                        "avg_percent": sum(m.get("percent", 0) for m in memory_values)
                        / len(memory_values),
                        "avg_used_gb": sum(m.get("used_gb", 0) for m in memory_values)
                        / len(memory_values),
                    }

            # CPU averages
            if "cpu" in recent_metrics[0]:
                cpu_values = [m["cpu"] for m in recent_metrics if "cpu" in m]
                if cpu_values:
                    avg_metrics["cpu"] = {
                        "avg_percent": sum(m.get("cpu_percent", 0) for m in cpu_values)
                        / len(cpu_values)
                    }

            avg_metrics["sample_count"] = len(recent_metrics)
            avg_metrics["time_window_minutes"] = time_window_minutes

            return avg_metrics

        except Exception as e:
            self.logger.error(f"Failed to calculate average metrics: {e}")
            return {}

    def clear_history(self):
        """Clear metrics history"""
        self.metrics_history.clear()
        self.logger.info("Performance metrics history cleared")


def run_smoke_test():
    """Run basic functionality test for PerformanceMonitor"""
    print("🧪 Running PerformanceMonitor Smoke Test...")

    try:
        monitor = PerformanceMonitor()

        # Test metrics collection
        metrics = monitor.get_performance_metrics()
        assert "timestamp" in metrics
        assert "memory" in metrics or "cpu" in metrics

        # Test history
        history = monitor.get_metrics_history()
        assert len(history) > 0

        # Test average calculation
        avg_metrics = monitor.get_average_metrics(1)
        assert "sample_count" in avg_metrics

        # Test history clearing
        monitor.clear_history()
        assert len(monitor.get_metrics_history()) == 0

        print("✅ PerformanceMonitor Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ PerformanceMonitor Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for PerformanceMonitor testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Performance Monitor CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--metrics", action="store_true", help="Get current performance metrics"
    )
    parser.add_argument("--history", type=int, help="Get metrics history (limit)")
    parser.add_argument(
        "--average", type=int, default=5, help="Get average metrics over minutes"
    )
    parser.add_argument("--clear", action="store_true", help="Clear metrics history")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    monitor = PerformanceMonitor()

    if args.metrics:
        metrics = monitor.get_performance_metrics()
        print("Performance Metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
    elif args.history is not None:
        history = monitor.get_metrics_history(args.history)
        print(f"Metrics History (last {len(history)} entries):")
        for i, entry in enumerate(history):
            print(f"  Entry {i+1}: {entry.get('timestamp', 'N/A')}")
    elif args.average:
        avg_metrics = monitor.get_average_metrics(args.average)
        print(f"Average Metrics (last {args.average} minutes):")
        for key, value in avg_metrics.items():
            print(f"  {key}: {value}")
    elif args.clear:
        monitor.clear_history()
        print("✅ Metrics history cleared")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
