"""
Operational Test Configuration
==============================

Pytest configuration and fixtures for operational tests.

Author: Agent-8 (Operations & Support Specialist)
"""

import pytest
import time
import psutil
import os
import sys
from typing import Dict, Any, Generator

# Add src to path for operational tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

@pytest.fixture(scope="session", autouse=True)
def operational_test_setup():
    """Setup for operational tests."""
    # Set operational test environment
    os.environ.setdefault('OPERATIONAL_TESTING', 'true')
    os.environ.setdefault('TEST_MODE', 'operational')

    # Ensure test directories exist
    test_dirs = [
        'test_results',
        'performance_logs',
        'stability_reports'
    ]

    for test_dir in test_dirs:
        os.makedirs(test_dir, exist_ok=True)

    yield

    # Cleanup after operational tests
    pass

@pytest.fixture
def system_monitor() -> Generator[Dict[str, Any], None, None]:
    """Provide system monitoring capabilities for tests."""

    class OperationalSystemMonitor:
        def __init__(self):
            self.baseline_cpu = psutil.cpu_percent(interval=1)
            self.baseline_memory = psutil.virtual_memory().percent
            self.baseline_disk = psutil.disk_usage('/').percent
            self.start_time = time.time()

        def get_system_health(self) -> Dict[str, Any]:
            """Get comprehensive system health metrics."""
            return {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'network_connections': len(psutil.net_connections()),
                'process_count': len(psutil.pids()),
                'uptime_seconds': time.time() - self.start_time,
                'baseline_cpu': self.baseline_cpu,
                'baseline_memory': self.baseline_memory,
                'baseline_disk': self.baseline_disk
            }

        def check_stability(self) -> bool:
            """Check if system is stable."""
            current = self.get_system_health()

            # Define stability criteria
            stability_criteria = [
                current['cpu_percent'] < 95,  # CPU not overloaded
                current['memory_percent'] < 90,  # Memory not exhausted
                current['disk_usage'] < 95,  # Disk not full
                current['process_count'] > 0,  # System has processes
            ]

            return all(stability_criteria)

        def check_operational_stability(self) -> bool:
            """Check if system is operationally stable."""
            return self.check_stability()

        def get_performance_delta(self) -> Dict[str, float]:
            """Get performance changes from baseline."""
            current = self.get_system_health()

            return {
                'cpu_delta': current['cpu_percent'] - self.baseline_cpu,
                'memory_delta': current['memory_percent'] - self.baseline_memory,
                'disk_delta': current['disk_usage'] - self.baseline_disk,
            }

        def log_operational_metrics(self, operation_name: str) -> None:
            """Log operational metrics for monitoring."""
            health = self.get_system_health()
            delta = self.get_performance_delta()

            log_entry = {
                'timestamp': time.time(),
                'operation': operation_name,
                'system_health': health,
                'performance_delta': delta,
                'stability_status': self.check_operational_stability()
            }

            # In a real system, this would write to a log file
            print(f"Operational metrics logged for {operation_name}")

    monitor = OperationalSystemMonitor()
    yield monitor

@pytest.fixture
def operational_test_config() -> Dict[str, Any]:
    """Configuration for operational tests."""
    return {
        # Test duration settings
        'short_test_duration': 5,  # seconds
        'medium_test_duration': 15,  # seconds
        'long_test_duration': 30,  # seconds

        # Performance thresholds
        'max_cpu_percent': 90,
        'max_memory_percent': 85,
        'max_disk_percent': 90,
        'min_success_rate': 0.8,

        # Operational settings
        'monitoring_interval': 0.5,  # seconds
        'stability_check_interval': 1.0,  # seconds
        'error_retry_count': 3,

        # Resource allocation
        'concurrent_workers': 3,
        'worker_timeout': 10,  # seconds
        'cleanup_timeout': 5,  # seconds
    }

@pytest.fixture
def performance_baseline(system_monitor) -> Dict[str, Any]:
    """Establish performance baseline for tests."""
    # Allow system to stabilize
    time.sleep(2)

    # Get baseline metrics
    baseline = system_monitor.get_system_health()

    # Log baseline
    print(f"Performance baseline established:")
    print(f"  CPU: {baseline['cpu_percent']:.1f}%")
    print(f"  Memory: {baseline['memory_percent']:.1f}%")
    print(f"  Disk: {baseline['disk_usage']:.1f}%")

    return baseline

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup after each operational test."""
    yield

    # Force garbage collection
    import gc
    gc.collect()

    # Brief pause to allow system to stabilize
    time.sleep(0.5)

# Custom pytest markers for operational tests
def pytest_configure(config):
    """Configure pytest markers for operational tests."""
    markers = [
        "operational: Tests for operational functionality and monitoring",
        "stability: Tests for system stability and endurance",
        "monitoring: Tests for monitoring systems and dashboards",
        "recovery: Tests for error recovery and resilience",
        "performance: Tests for performance monitoring and optimization",
        "resource: Tests for resource usage and management",
        "integration: Tests for operational system integration",
    ]

    for marker in markers:
        config.addinivalue_line("markers", marker)
