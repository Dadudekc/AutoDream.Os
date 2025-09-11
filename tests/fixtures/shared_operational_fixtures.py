"""
Shared Operational Test Fixtures
================================

Common fixtures and utilities for operational testing across all agents.
Provides standardized mock objects, test data, and helper functions.

Author: Agent-8 (Operations & Support Specialist)
FINAL PYTEST ASSIGNMENT - Shared Resources
"""

import pytest
import time
import psutil
import threading
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, Any, List, Optional, Callable, Generator
import tempfile
import os

# Shared mock classes for cross-agent testing
class SharedMockClasses:
    """Shared mock implementations for consistent testing across agents."""

    @staticmethod
    def create_mock_monitoring_dashboard():
        """Create standardized mock monitoring dashboard."""
        mock_dashboard = Mock()
        mock_dashboard.get_system_metrics.return_value = {
            'cpu_usage': 45.2,
            'memory_usage': 62.8,
            'disk_usage': 38.5,
            'network_io': 125.3,
            'process_count': 87,
            'timestamp': time.time()
        }
        mock_dashboard.check_performance_health.return_value = True
        mock_dashboard.get_performance_alerts.return_value = []
        return mock_dashboard

    @staticmethod
    def create_mock_health_check_system():
        """Create standardized mock health check system."""
        mock_health = Mock()
        mock_health.run_comprehensive_checks.return_value = [
            {'check_name': 'cpu', 'status': 'healthy', 'value': 45.2},
            {'check_name': 'memory', 'status': 'healthy', 'value': 62.8},
            {'check_name': 'disk', 'status': 'healthy', 'value': 38.5}
        ]
        mock_health.get_overall_health_score.return_value = 95.2
        mock_health.get_health_trends.return_value = {
            'cpu_trend': 'stable',
            'memory_trend': 'stable',
            'disk_trend': 'stable'
        }
        return mock_health

    @staticmethod
    def create_mock_logging_system():
        """Create standardized mock logging system."""
        mock_logger = Mock()
        mock_logger.log_event.return_value = None
        mock_logger.get_recent_logs.return_value = [
            {'level': 'INFO', 'message': 'Test log entry', 'timestamp': time.time()}
        ]
        mock_logger.get_error_count.return_value = 0
        return mock_logger

    @staticmethod
    def create_mock_database_connection():
        """Create standardized mock database connection."""
        mock_db = Mock()
        mock_db.connect.return_value = True
        mock_db.disconnect.return_value = True
        mock_db.execute_query.return_value = [{'id': 1, 'name': 'test'}]
        mock_db.commit.return_value = True
        mock_db.rollback.return_value = True
        return mock_db

    @staticmethod
    def create_mock_message_queue():
        """Create standardized mock message queue."""
        mock_queue = Mock()
        mock_queue.send_message.return_value = True
        mock_queue.receive_message.return_value = {'id': '123', 'content': 'test message'}
        mock_queue.get_queue_length.return_value = 5
        mock_queue.clear_queue.return_value = True
        return mock_queue

# Shared test data generators
class SharedTestData:
    """Shared test data generators for consistent testing."""

    @staticmethod
    def generate_user_data(count: int = 10) -> List[Dict[str, Any]]:
        """Generate sample user data for testing."""
        users = []
        for i in range(count):
            users.append({
                'id': f'user_{i}',
                'name': f'Test User {i}',
                'email': f'user{i}@test.com',
                'role': 'user',
                'active': True,
                'created_at': time.time() - (i * 86400)  # Days ago
            })
        return users

    @staticmethod
    def generate_transaction_data(count: int = 20) -> List[Dict[str, Any]]:
        """Generate sample transaction data for testing."""
        transactions = []
        for i in range(count):
            transactions.append({
                'id': f'txn_{i}',
                'user_id': f'user_{i % 5}',
                'amount': round(10.0 + (i * 1.5), 2),
                'currency': 'USD',
                'status': 'completed' if i % 10 != 0 else 'pending',
                'timestamp': time.time() - (i * 3600)  # Hours ago
            })
        return transactions

    @staticmethod
    def generate_system_metrics_history(duration_seconds: int = 300) -> List[Dict[str, Any]]:
        """Generate historical system metrics for testing."""
        metrics_history = []
        start_time = time.time() - duration_seconds

        for i in range(duration_seconds // 10):  # Sample every 10 seconds
            metrics_history.append({
                'timestamp': start_time + (i * 10),
                'cpu_usage': 40.0 + (i % 20),  # Vary between 40-60%
                'memory_usage': 50.0 + (i % 30),  # Vary between 50-80%
                'disk_usage': 35.0 + (i % 15),  # Vary between 35-50%
                'network_io': 100.0 + (i % 50),  # Vary network usage
                'active_connections': 10 + (i % 20)
            })

        return metrics_history

# Shared test utilities
class SharedTestUtils:
    """Shared utility functions for operational testing."""

    @staticmethod
    def create_temp_file(content: str = "test content", suffix: str = ".tmp") -> str:
        """Create a temporary file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
            f.write(content)
            return f.name

    @staticmethod
    def create_temp_directory() -> str:
        """Create a temporary directory for testing."""
        return tempfile.mkdtemp()

    @staticmethod
    def cleanup_temp_files(*file_paths: str) -> None:
        """Clean up temporary files."""
        for path in file_paths:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    os.rmdir(path)
            except OSError:
                pass  # Ignore cleanup errors in tests

    @staticmethod
    def simulate_network_delay(delay_seconds: float = 0.1) -> None:
        """Simulate network delay in tests."""
        time.sleep(delay_seconds)

    @staticmethod
    def wait_for_condition(condition_func: Callable[[], bool],
                          timeout: float = 5.0,
                          interval: float = 0.1) -> bool:
        """Wait for a condition to become true."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False

    @staticmethod
    def measure_execution_time(func: Callable, *args, **kwargs) -> tuple:
        """Measure execution time of a function."""
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        return result, execution_time

# Shared pytest fixtures
@pytest.fixture
def mock_monitoring_dashboard():
    """Shared fixture for mock monitoring dashboard."""
    return SharedMockClasses.create_mock_monitoring_dashboard()

@pytest.fixture
def mock_health_check_system():
    """Shared fixture for mock health check system."""
    return SharedMockClasses.create_mock_health_check_system()

@pytest.fixture
def mock_logging_system():
    """Shared fixture for mock logging system."""
    return SharedMockClasses.create_mock_logging_system()

@pytest.fixture
def mock_database_connection():
    """Shared fixture for mock database connection."""
    return SharedMockClasses.create_mock_database_connection()

@pytest.fixture
def mock_message_queue():
    """Shared fixture for mock message queue."""
    return SharedMockClasses.create_mock_message_queue()

@pytest.fixture
def sample_user_data():
    """Shared fixture for sample user data."""
    return SharedTestData.generate_user_data(10)

@pytest.fixture
def sample_transaction_data():
    """Shared fixture for sample transaction data."""
    return SharedTestData.generate_transaction_data(20)

@pytest.fixture
def system_metrics_history():
    """Shared fixture for system metrics history."""
    return SharedTestData.generate_system_metrics_history(300)

@pytest.fixture
def temp_file():
    """Shared fixture for temporary file."""
    file_path = SharedTestUtils.create_temp_file()
    yield file_path
    SharedTestUtils.cleanup_temp_files(file_path)

@pytest.fixture
def temp_directory():
    """Shared fixture for temporary directory."""
    dir_path = SharedTestUtils.create_temp_directory()
    yield dir_path
    SharedTestUtils.cleanup_temp_files(dir_path)

@pytest.fixture
def performance_timer():
    """Shared fixture for measuring performance."""
    class PerformanceTimer:
        def __init__(self):
            self.start_time = None
            self.end_time = None

        def start(self):
            self.start_time = time.time()

        def stop(self):
            self.end_time = time.time()

        @property
        def duration(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return 0

        def measure(self, func, *args, **kwargs):
            """Measure execution time of a function."""
            self.start()
            result = func(*args, **kwargs)
            self.stop()
            return result, self.duration

    return PerformanceTimer()

# Context managers for testing
class SharedTestContexts:
    """Shared context managers for testing scenarios."""

    @staticmethod
    def high_cpu_context():
        """Context manager for simulating high CPU usage."""
        class HighCpuContext:
            def __enter__(self):
                self.original_cpu_percent = psutil.cpu_percent
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                # Restore original CPU monitoring
                pass

        return HighCpuContext()

    @staticmethod
    def network_failure_context():
        """Context manager for simulating network failures."""
        class NetworkFailureContext:
            def __enter__(self):
                self.patches = [
                    patch('socket.socket.connect', side_effect=ConnectionError("Network unreachable")),
                    patch('urllib.request.urlopen', side_effect=Exception("Connection failed"))
                ]
                for p in self.patches:
                    p.start()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                for p in self.patches:
                    p.stop()

        return NetworkFailureContext()

    @staticmethod
    def database_failure_context():
        """Context manager for simulating database failures."""
        class DatabaseFailureContext:
            def __enter__(self):
                self.patches = [
                    patch('sqlite3.connect', side_effect=Exception("Database connection failed")),
                    patch('psycopg2.connect', side_effect=Exception("PostgreSQL connection failed"))
                ]
                for p in self.patches:
                    p.start()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                for p in self.patches:
                    p.stop()

        return DatabaseFailureContext()

# Performance baseline utilities
class SharedPerformanceBaselines:
    """Shared utilities for establishing performance baselines."""

    @staticmethod
    def establish_cpu_baseline(duration: int = 10) -> Dict[str, float]:
        """Establish CPU usage baseline."""
        cpu_readings = []

        for _ in range(duration):
            cpu_readings.append(psutil.cpu_percent(interval=1))

        return {
            'mean': sum(cpu_readings) / len(cpu_readings),
            'min': min(cpu_readings),
            'max': max(cpu_readings),
            'readings': cpu_readings
        }

    @staticmethod
    def establish_memory_baseline(duration: int = 10) -> Dict[str, float]:
        """Establish memory usage baseline."""
        memory_readings = []

        for _ in range(duration):
            memory_readings.append(psutil.virtual_memory().percent)

        return {
            'mean': sum(memory_readings) / len(memory_readings),
            'min': min(memory_readings),
            'max': max(memory_readings),
            'readings': memory_readings
        }

    @staticmethod
    def establish_disk_baseline(duration: int = 10) -> Dict[str, float]:
        """Establish disk usage baseline."""
        disk_readings = []

        for _ in range(duration):
            disk_readings.append(psutil.disk_usage('/').percent)

        return {
            'mean': sum(disk_readings) / len(disk_readings),
            'min': min(disk_readings),
            'max': max(disk_readings),
            'readings': disk_readings
        }

# Export shared resources for other agents
__all__ = [
    'SharedMockClasses',
    'SharedTestData',
    'SharedTestUtils',
    'SharedTestContexts',
    'SharedPerformanceBaselines',
    # Fixtures are automatically available when this module is imported
]
