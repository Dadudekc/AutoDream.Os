"""
Pytest Configuration and Shared Fixtures
========================================

Comprehensive test configuration for V2_SWARM codebase.
Provides shared fixtures, test utilities, and coverage configuration.
"""

import pytest
import tempfile
import shutil
import os
from pathlib import Path
from typing import Generator, Any


# Test configuration
@pytest.fixture(scope="session")
def test_config():
    """Global test configuration fixture."""
    return {
        "temp_dir": tempfile.gettempdir(),
        "test_data_dir": Path(__file__).parent / "fixtures",
        "coverage_target": 85,
        "timeout": 30,
        "retries": 3
    }


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment before all tests."""
    # Create test directories
    test_dirs = [
        Path(__file__).parent / "unit",
        Path(__file__).parent / "integration",
        Path(__file__).parent / "e2e",
        Path(__file__).parent / "performance",
        Path(__file__).parent / "fixtures"
    ]

    for test_dir in test_dirs:
        test_dir.mkdir(exist_ok=True)

    yield

    # Cleanup after all tests
    # Add cleanup logic here if needed


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_file(temp_directory):
    """Create a mock file for testing."""
    mock_file_path = os.path.join(temp_directory, "test_file.txt")
    with open(mock_file_path, 'w') as f:
        f.write("test content")
    return mock_file_path


@pytest.fixture
def sample_config():
    """Sample configuration data for testing."""
    return {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "test_db"
        },
        "logging": {
            "level": "DEBUG",
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        },
        "features": {
            "enable_cache": True,
            "max_connections": 10
        }
    }


@pytest.fixture
def mock_agent_data():
    """Mock agent data for testing."""
    return {
        "agent_id": "test_agent",
        "coordinates": [100, 200],
        "status": "active",
        "capabilities": ["test", "mock"],
        "last_updated": "2025-09-09T17:00:00Z"
    }


# Custom markers for test categorization
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "agent1: Agent-1 specific tests")
    config.addinivalue_line("markers", "agent2: Agent-2 specific tests")
    config.addinivalue_line("markers", "agent3: Agent-3 specific tests")
    config.addinivalue_line("markers", "agent4: Agent-4 specific tests")
    config.addinivalue_line("markers", "agent5: Agent-5 specific tests")
    config.addinivalue_line("markers", "agent6: Agent-6 specific tests")
    config.addinivalue_line("markers", "agent7: Agent-7 specific tests")
    config.addinivalue_line("markers", "agent8: Agent-8 specific tests")


# Coverage configuration
def pytest_configure_node(node):
    """Configure coverage for distributed testing."""
    node.config.option.cov_source = ["src"]
    node.config.option.cov_report = ["html", "term-missing"]
    node.config.option.cov_fail_under = 85


# Test utilities
class TestUtils:
    """Utility class for test operations."""

    @staticmethod
    def assert_file_exists(file_path: str):
        """Assert that a file exists."""
        assert os.path.exists(file_path), f"File {file_path} does not exist"

    @staticmethod
    def assert_file_contains(file_path: str, content: str):
        """Assert that a file contains specific content."""
        with open(file_path, 'r') as f:
            file_content = f.read()
        assert content in file_content, f"Content '{content}' not found in {file_path}"

    @staticmethod
    def create_temp_file(content: str = "", suffix: str = ".txt"):
        """Create a temporary file with content."""
        fd, path = tempfile.mkstemp(suffix=suffix)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)
            return path
        except:
            os.close(fd)
            raise

    @staticmethod
    def cleanup_temp_file(file_path: str):
        """Clean up a temporary file."""
        try:
            os.unlink(file_path)
        except OSError:
            pass


@pytest.fixture
def test_utils():
    """Test utilities fixture."""
    return TestUtils()


# Performance testing utilities
class PerformanceUtils:
    """Utilities for performance testing."""

    @staticmethod
    def measure_execution_time(func, *args, **kwargs):
        """Measure function execution time."""
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time

    @staticmethod
    def assert_performance(func, max_time: float, *args, **kwargs):
        """Assert function performance meets requirements."""
        _, execution_time = PerformanceUtils.measure_execution_time(func, *args, **kwargs)
        assert execution_time <= max_time, f"Function took {execution_time:.2f}s, max allowed: {max_time}s"


@pytest.fixture
def performance_utils():
    """Performance testing utilities fixture."""
    return PerformanceUtils()


# Mock data generators
class MockDataGenerator:
    """Generate mock data for testing."""

    @staticmethod
    def generate_agent_data(count: int = 1):
        """Generate mock agent data."""
        agents = []
        for i in range(count):
            agents.append({
                "agent_id": f"agent_{i}",
                "coordinates": [i * 100, i * 100],
                "status": "active",
                "capabilities": ["test", "mock"],
                "last_updated": "2025-09-09T17:00:00Z"
            })
        return agents if count > 1 else agents[0]

    @staticmethod
    def generate_task_data(count: int = 1):
        """Generate mock task data."""
        tasks = []
        for i in range(count):
            tasks.append({
                "task_id": f"task_{i}",
                "description": f"Test task {i}",
                "priority": "medium",
                "status": "pending",
                "assigned_agent": f"agent_{i}"
            })
        return tasks if count > 1 else tasks[0]


@pytest.fixture
def mock_data_generator():
    """Mock data generator fixture."""
    return MockDataGenerator()