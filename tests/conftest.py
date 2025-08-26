"""
🧪 PYTEST CONFIGURATION - AGENT_CELLPHONE_V2
Foundation & Testing Specialist - TDD Integration Project

This file provides shared fixtures, test utilities, and testing infrastructure
for all test modules in the Agent_Cellphone_V2 testing framework.
"""

import os
import sys
import tempfile
import shutil

# Stability improvements are available but not auto-imported to avoid circular imports
# from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, Any, Generator, Optional
from unittest.mock import Mock, MagicMock, patch

import pytest
from pytest import FixtureRequest
import coverage

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))
from utils.stability_improvements import StabilityManager

# Testing configuration
TEST_TIMEOUT = 30  # seconds
TEST_COVERAGE_THRESHOLD = 80  # percentage


class TestConfig:
    """Test configuration and constants."""

    # V2 Standards Compliance (Updated 2024 - Balanced Approach)
    MAX_LOC_STANDARD = 400  # Standard files: balanced for maintainability
    MAX_LOC_GUI = 600       # GUI files: generous for UI while maintaining structure
    MAX_LOC_CORE = 400      # Core files: focused and testable business logic

    # Testing thresholds
    MIN_COVERAGE = 80
    MAX_TEST_DURATION = 30

    # Test data paths
    TEST_DATA_DIR = Path(__file__).parent / "test_data"
    TEMP_DIR = Path(tempfile.gettempdir()) / "agent_cellphone_v2_tests"

    # Component categories for testing
    COMPONENTS = {
        "core": "Core system components",
        "services": "Service layer components",
        "launchers": "Launcher components",
        "utils": "Utility components",
        "web": "Web interface components",
    }


@pytest.fixture(scope="session")
def test_config() -> TestConfig:
    """Provide test configuration for all tests."""
    return TestConfig()


@pytest.fixture(scope="session")
def temp_test_dir(test_config: TestConfig) -> Generator[Path, None, None]:
    """Create and provide temporary test directory."""
    test_config.TEMP_DIR.mkdir(parents=True, exist_ok=True)
    yield test_config.TEMP_DIR
    # Cleanup after all tests
    if test_config.TEMP_DIR.exists():
        shutil.rmtree(test_config.TEMP_DIR)


@pytest.fixture(scope="function")
def clean_temp_dir(temp_test_dir: Path) -> Generator[Path, None, None]:
    """Provide clean temporary directory for each test."""
    # Clean before test
    for item in temp_test_dir.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)
    yield temp_test_dir


@pytest.fixture(scope="session")
def coverage_obj() -> Generator[coverage.Coverage, None, None]:
    """Provide coverage object for testing."""
    cov = coverage.Coverage()
    cov.start()
    yield cov
    cov.stop()
    cov.save()


@pytest.fixture(scope="function")
def mock_logger() -> Generator[Mock, None, None]:
    """Provide mock logger for testing."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        yield mock_logger


@pytest.fixture(scope="function")
def sample_test_data() -> Dict[str, Any]:
    """Provide sample test data for testing."""
    return {
        "agent_id": "test_agent_001",
        "task_id": "test_task_001",
        "priority": "NORMAL",
        "status": "PENDING",
        "metadata": {
            "created_by": "test_user",
            "created_at": "2024-01-01T00:00:00Z",
            "tags": ["test", "automation"],
        },
        "config": {"timeout": 30, "retries": 3, "debug": False},
    }


@pytest.fixture(scope="function")
def mock_cli_args() -> Mock:
    """Provide mock CLI arguments for testing."""
    mock_args = Mock()
    mock_args.test = True
    mock_args.operation = None
    mock_args.verbose = False
    mock_args.config = None
    mock_args.output = None
    return mock_args


@pytest.fixture(scope="function")
def mock_environment() -> Generator[Dict[str, str], None, None]:
    """Provide mock environment variables for testing."""
    original_env = os.environ.copy()

    test_env = {
        "AGENT_CELLPHONE_V2_ENV": "test",
        "AGENT_CELLPHONE_V2_DEBUG": "true",
        "AGENT_CELLPHONE_V2_LOG_LEVEL": "DEBUG",
        "AGENT_CELLPHONE_V2_CONFIG_PATH": "/tmp/test_config",
        "AGENT_CELLPHONE_V2_DATA_PATH": "/tmp/test_data",
    }

    os.environ.update(test_env)
    yield test_env

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture(scope="function")
def stability_manager() -> StabilityManager:
    """Provide a StabilityManager instance for tests."""
    return StabilityManager()


# V2 Standards Compliance Fixtures
@pytest.fixture(scope="function")
def loc_checker() -> Generator[Any, None, None]:
    """Provide line count checker for V2 standards compliance."""

    def check_loc(file_path: Path, max_loc: int = TestConfig.MAX_LOC_CORE) -> bool:
        """Check if file meets LOC requirements."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Filter out empty lines and comments
                code_lines = [
                    line
                    for line in lines
                    if line.strip() and not line.strip().startswith("#")
                ]
                return len(code_lines) <= max_loc
        except Exception:
            return False

    yield check_loc


@pytest.fixture(scope="function")
def oop_checker() -> Generator[Any, None, None]:
    """Provide OOP design checker for V2 standards compliance."""

    def check_oop_compliance(file_path: Path) -> Dict[str, bool]:
        """Check OOP design compliance."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                # Check for class definitions
                has_classes = "class " in content

                # Check for function definitions outside classes
                lines = content.split("\n")
                has_functions_outside_classes = False
                in_class = False

                for line in lines:
                    line = line.strip()
                    if line.startswith("class "):
                        in_class = True
                    elif line.startswith("def ") and not in_class:
                        has_functions_outside_classes = True
                    elif line == "" or line.startswith("#"):
                        continue
                    elif line.startswith("if __name__"):
                        break

                return {
                    "has_classes": has_classes,
                    "no_functions_outside_classes": not has_functions_outside_classes,
                    "is_oop_compliant": has_classes
                    and not has_functions_outside_classes,
                }
        except Exception:
            return {
                "has_classes": False,
                "no_functions_outside_classes": False,
                "is_oop_compliant": False,
            }

    yield check_oop_compliance


@pytest.fixture(scope="function")
def cli_checker() -> Generator[Any, None, None]:
    """Provide CLI interface checker for V2 standards compliance."""

    def check_cli_interface(file_path: Path) -> Dict[str, bool]:
        """Check CLI interface compliance."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                # Check for argparse usage
                has_argparse = "argparse" in content

                # Check for main function
                has_main = "def main(" in content or "if __name__" in content

                # Check for help documentation
                has_help = "help=" in content

                # Check for argument parsing
                has_argument_parsing = "add_argument" in content

                return {
                    "has_argparse": has_argparse,
                    "has_main": has_main,
                    "has_help": has_help,
                    "has_argument_parsing": has_argument_parsing,
                    "is_cli_compliant": all(
                        [has_argparse, has_main, has_help, has_argument_parsing]
                    ),
                }
        except Exception:
            return {
                "has_argparse": False,
                "has_main": False,
                "has_help": False,
                "has_argument_parsing": False,
                "is_cli_compliant": False,
            }

    yield check_cli_checker


# Test utilities
def assert_v2_standards_compliance(
    file_path: Path, max_loc: int = TestConfig.MAX_LOC_CORE
) -> None:
    """Assert V2 coding standards compliance for a file."""
    # Check line count
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        code_lines = [
            line for line in lines if line.strip() and not line.strip().startswith("#")
        ]
        assert (
            len(code_lines) <= max_loc
        ), f"File exceeds {max_loc} LOC limit: {len(code_lines)} lines"

    # Check OOP design
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert (
            "class " in content
        ), "File must contain class definitions (OOP requirement)"

    # Check CLI interface
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "argparse" in content, "File must have CLI interface (argparse usage)"
        assert (
            "def main(" in content or "if __name__" in content
        ), "File must have main function or entry point"


def create_test_component(
    component_type: str, component_name: str, test_config: TestConfig
) -> Path:
    """Create a test component file for testing."""
    component_dir = test_config.TEMP_DIR / component_type
    component_dir.mkdir(parents=True, exist_ok=True)

    component_file = component_dir / f"{component_name}.py"

    # Create minimal compliant component
    component_content = f'''"""
{component_type.title()} Component: {component_name}
V2 Standards Compliant Test Component
"""

import argparse
from typing import Optional, Dict, Any


class {component_name.title()}:
    """
    {component_name.title()} component following V2 coding standards.

    Single responsibility: {component_type} management
    LOC limit: ≤{test_config.MAX_LOC_CORE} lines
    OOP design: Proper class structure
    CLI interface: Comprehensive testing interface
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize {component_name.title()} component."""
        self.config = config or {{}}
        self.status = "INITIALIZED"

    def initialize(self) -> bool:
        """Initialize the component."""
        self.status = "READY"
        return True

    def test_functionality(self) -> bool:
        """Test basic functionality."""
        return self.status == "READY"

    def cleanup(self) -> None:
        """Cleanup resources."""
        self.status = "CLEANED_UP"


def main():
    """CLI interface for {component_name.title()} component."""
    parser = argparse.ArgumentParser(description="{component_name.title()} Component CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    parser.add_argument("--operation", type=str, help="Perform operation")

    args = parser.parse_args()

    component = {component_name.title()}()

    if args.test:
        print(f"Running smoke tests for {{component_name}}...")
        assert component.initialize()
        assert component.test_functionality()
        component.cleanup()
        print("✅ All smoke tests passed!")
    elif args.operation:
        print(f"Performing operation: {{args.operation}}")
        component.initialize()
        # Operation logic here
        component.cleanup()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
'''

    with open(component_file, "w", encoding="utf-8") as f:
        f.write(component_content)

    return component_file


# Pytest hooks
def pytest_configure(config):
    """Configure pytest with custom markers and options."""
    config.addinivalue_line("markers", "smoke: Smoke tests for basic functionality")
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line(
        "markers", "integration: Integration tests for component interaction"
    )
    config.addinivalue_line(
        "markers", "v2_standards: V2 coding standards compliance tests"
    )
    config.addinivalue_line("markers", "behavior: Behavior tree tests")
    config.addinivalue_line("markers", "decision: Decision engine tests")
    config.addinivalue_line("markers", "coordination: Multi-agent coordination tests")
    config.addinivalue_line("markers", "learning: Learning component tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add custom markers."""
    for item in items:
        # Add v2_standards marker to all tests
        item.add_marker(pytest.mark.v2_standards)

        # Add component-specific markers based on test path
        if "test_core" in str(item.fspath):
            item.add_marker(pytest.mark.core)
        elif "test_services" in str(item.fspath):
            item.add_marker(pytest.mark.services)
        elif "test_launchers" in str(item.fspath):
            item.add_marker(pytest.mark.launchers)
        elif "test_utils" in str(item.fspath):
            item.add_marker(pytest.mark.utils)
        elif "behavior_trees" in str(item.fspath):
            item.add_marker(pytest.mark.behavior)
        elif "decision_engines" in str(item.fspath):
            item.add_marker(pytest.mark.decision)
        elif "multi_agent" in str(item.fspath):
            item.add_marker(pytest.mark.coordination)
        elif "learning" in str(item.fspath):
            item.add_marker(pytest.mark.learning)
