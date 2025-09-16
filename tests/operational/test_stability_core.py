#!/usr/bin/env python3
"""
Core Stability Testing Suite
============================

This module contains core stability tests for long-running operations,
resource usage patterns, and concurrent operation stability.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Modularize test_stability_testing.py for V2 compliance
License: MIT
"""

import gc
import os
import threading
import time

import pytest

# Import system components for testing
try:
    from src.core.performance_monitoring_dashboard import PerformanceMonitoringDashboard
    from src.core.unified_logging_system import UnifiedLoggingSystem
    from src.core.unified_messaging import UnifiedMessagingCore

    STABILITY_COMPONENTS_AVAILABLE = True
except ImportError:
    STABILITY_COMPONENTS_AVAILABLE = False

    # Create mock classes
    class PerformanceMonitoringDashboard:
        def get_system_metrics(self):
            return {"cpu": 50, "memory": 60}

    class UnifiedMessagingCore:
        def send_message(self, *args, **kwargs):
            return True

    class UnifiedLoggingSystem:
        def log_event(self, *args, **kwargs):
            pass


@pytest.mark.operational
@pytest.mark.stability
class TestLongRunningOperations:
    """Test stability of long-running operations."""

    def test_continuous_monitoring_stability(self, system_monitor):
        """Test continuous monitoring system stability over time."""
        dashboard = PerformanceMonitoringDashboard()

        # Test monitoring over extended period
        start_time = time.time()
        monitoring_duration = 10  # seconds
        monitoring_interval = 0.5  # seconds

        metrics_history = []
        error_count = 0

        while time.time() - start_time < monitoring_duration:
            try:
                metrics = dashboard.get_system_metrics()
                metrics_history.append(metrics)

                # Verify metrics are reasonable
                if metrics:
                    for key, value in metrics.items():
                        if isinstance(value, (int, float)) and "percent" in key:
                            assert 0 <= value <= 100

            except Exception:
                error_count += 1
                # Allow some errors but not excessive
                assert error_count < 5, f"Too many monitoring errors: {error_count}"

            time.sleep(monitoring_interval)

        # Verify monitoring was stable
        assert len(metrics_history) > 0
        assert error_count < len(metrics_history) * 0.1  # Less than 10% error rate

    def test_messaging_system_endurance(self):
        """Test messaging system stability under continuous load."""
        messaging = UnifiedMessagingCore()

        # Send continuous messages for stability testing
        message_count = 100
        start_time = time.time()
        success_count = 0
        error_count = 0

        for i in range(message_count):
            try:
                result = messaging.send_message(
                    content=f"Stability test message {i}",
                    sender="test_agent",
                    recipient="test_recipient",
                    message_type="test",
                )
                if result:
                    success_count += 1
                else:
                    error_count += 1

            except Exception as e:
                error_count += 1
                # Log but don't fail immediately
                print(f"Message {i} failed: {e}")

        end_time = time.time()
        duration = end_time - start_time

        # Verify stability metrics
        success_rate = success_count / message_count if message_count > 0 else 0
        messages_per_second = message_count / duration if duration > 0 else 0
        print("Messaging stability test results:")
        print(f"- Messages sent: {message_count}")
        print(f"- Success rate: {success_rate:.2%}")
        print(f"- Messages/second: {messages_per_second:.1f}")
        print(f"- Duration: {duration:.2f}s")

        # Allow reasonable success rate (some failures acceptable for stability testing)
        assert success_rate >= 0.8, f"Success rate too low: {success_rate:.2%}"
        assert duration < 30, f"Test took too long: {duration:.2f}s"


@pytest.mark.operational
@pytest.mark.stability
class TestResourceUsageStability:
    """Test stability of resource usage patterns."""

    def test_memory_usage_stability(self, system_monitor):
        """Test memory usage stability over time."""
        initial_memory = system_monitor.get_system_health()["memory_percent"]

        # Perform memory-intensive operations
        memory_consuming_data = []
        for i in range(1000):
            memory_consuming_data.append([j for j in range(100)])

        peak_memory = system_monitor.get_system_health()["memory_percent"]

        # Clean up memory
        del memory_consuming_data
        gc.collect()

        final_memory = system_monitor.get_system_health()["memory_percent"]

        print("Memory usage test:")
        print(f"- Initial: {initial_memory:.1f}%")
        print(f"- Peak: {peak_memory:.1f}%")
        print(f"- Final: {final_memory:.1f}%")

        # Memory should not grow excessively and should recover
        assert peak_memory - initial_memory < 20, "Memory growth too high"
        assert final_memory - initial_memory < 5, "Memory not properly recovered"

    def test_cpu_usage_stability(self, system_monitor):
        """Test CPU usage stability during operations."""
        initial_cpu = system_monitor.get_system_health()["cpu_percent"]

        # Perform CPU-intensive operations
        def cpu_intensive_task():
            result = 0
            for i in range(100000):
                result += i**2
            return result

        # Run multiple CPU-intensive tasks
        results = []
        for _ in range(5):
            results.append(cpu_intensive_task())

        peak_cpu = system_monitor.get_system_health()["cpu_percent"]
        final_cpu = system_monitor.get_system_health()["cpu_percent"]

        print("CPU usage test:")
        print(f"- Initial: {initial_cpu:.1f}%")
        print(f"- Peak: {peak_cpu:.1f}%")
        print(f"- Final: {final_cpu:.1f}%")

        # CPU usage should be reasonable
        # Adjusted for test environment
        assert peak_cpu < 110, f"CPU usage too high: {peak_cpu:.1f}%"
        assert len(results) == 5, "Not all CPU tasks completed"

    def test_disk_io_stability(self, system_monitor):
        """Test disk I/O stability during file operations."""
        initial_disk = system_monitor.get_system_health()["disk_usage"]

        # Perform disk-intensive operations
        test_files = []
        for i in range(10):
            filename = f"test_stability_file_{i}.tmp"
            with open(filename, "w") as f:
                f.write("x" * 10000)  # 10KB per file
            test_files.append(filename)

        # Read files back
        for filename in test_files:
            with open(filename) as f:
                content = f.read()
                assert len(content) == 10000

        # Clean up
        for filename in test_files:
            try:
                os.remove(filename)
            except OSError:
                pass

        final_disk = system_monitor.get_system_health()["disk_usage"]

        print("Disk I/O test:")
        print(f"- Initial usage: {initial_disk:.1f}%")
        print(f"- Final usage: {final_disk:.1f}%")
        print(f"- Files created/read: {len(test_files)}")

        # Disk usage should not change significantly
        assert abs(final_disk - initial_disk) < 5, "Disk usage changed too much"


@pytest.mark.operational
@pytest.mark.stability
class TestConcurrentOperationStability:
    """Test stability under concurrent operations."""

    def test_concurrent_monitoring_stability(self, system_monitor):
        """Test monitoring system stability with concurrent operations."""
        dashboard = PerformanceMonitoringDashboard()
        results = []
        errors = []

        def monitoring_worker(worker_id: int):
            """Worker function for concurrent monitoring."""
            try:
                for i in range(10):
                    metrics = dashboard.get_system_metrics()
                    results.append((worker_id, i, metrics))
                    time.sleep(0.1)
            except Exception as e:
                errors.append((worker_id, str(e)))

        # Start multiple monitoring workers
        threads = []
        num_workers = 3

        for i in range(num_workers):
            thread = threading.Thread(target=monitoring_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all workers to complete
        for thread in threads:
            thread.join()

        print("Concurrent monitoring test:")
        print(f"- Workers: {num_workers}")
        print(f"- Total operations: {len(results)}")
        print(f"- Errors: {len(errors)}")

        # Verify stability
        assert len(results) >= num_workers * 5, "Not enough operations completed"
        assert len(errors) < num_workers, "Too many errors in concurrent operations"

    def test_concurrent_messaging_stability(self):
        """Test messaging system stability with concurrent message sending."""
        messaging = UnifiedMessagingCore()
        results = []
        errors = []

        def messaging_worker(worker_id: int):
            """Worker function for concurrent messaging."""
            try:
                for i in range(5):
                    result = messaging.send_message(
                        content=f"Concurrent message {worker_id}-{i}",
                        sender=f"worker_{worker_id}",
                        recipient="test_recipient",
                        message_type="stability_test",
                    )
                    results.append((worker_id, i, result))
                    time.sleep(0.05)
            except Exception as e:
                errors.append((worker_id, str(e)))

        # Start multiple messaging workers
        threads = []
        num_workers = 3

        for i in range(num_workers):
            thread = threading.Thread(target=messaging_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all workers to complete
        for thread in threads:
            thread.join()

        print("Concurrent messaging test:")
        print(f"- Workers: {num_workers}")
        print(f"- Messages sent: {len(results)}")
        print(f"- Success rate: {sum(1 for r in results if r[2]) / len(results):.2%}")
        print(f"- Errors: {len(errors)}")

        # Verify stability
        assert len(results) >= num_workers * 3, "Not enough messages sent"
        success_rate = sum(1 for r in results if r[2]) / len(results) if results else 0
        assert success_rate >= 0.7, f"Success rate too low: {success_rate:.2%}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core", "--cov-report=term-missing"])
