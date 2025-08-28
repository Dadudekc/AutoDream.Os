"""Centralised test configuration and reusable fixtures."""

import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest


class TestConfig:
    """Test configuration and constants."""

    MAX_LOC_STANDARD = 400  # Standard files
    MAX_LOC_GUI = 600  # GUI files
    MAX_LOC_CORE = 400  # Core files

    MIN_COVERAGE = 80
    MAX_TEST_DURATION = 30

    TEST_DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"
    TEMP_DIR = Path(tempfile.gettempdir()) / "agent_cellphone_v2_tests"


@pytest.fixture(scope="session")
def test_config() -> TestConfig:
    """Provide test configuration for all tests."""
    return TestConfig()


@pytest.fixture(scope="session")
def temp_test_dir(test_config: TestConfig) -> Generator[Path, None, None]:
    """Create and provide temporary test directory."""
    test_config.TEMP_DIR.mkdir(parents=True, exist_ok=True)
    yield test_config.TEMP_DIR
    if test_config.TEMP_DIR.exists():
        shutil.rmtree(test_config.TEMP_DIR)


@pytest.fixture(scope="function")
def clean_temp_dir(temp_test_dir: Path) -> Generator[Path, None, None]:
    """Provide clean temporary directory for each test."""
    for item in temp_test_dir.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)
    yield temp_test_dir
