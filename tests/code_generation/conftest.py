"""Fixtures for code generation tests."""

import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator

import pytest

MOCK_CODE_GENERATION_REQUESTS: Dict[str, Any] = {
    "simple_function": {
        "description": "Create a function to calculate fibonacci numbers",
        "language": "python",
        "framework": None,
        "requirements": ["recursive", "memoization"],
        "include_tests": True,
        "include_docs": True,
    }
}


@pytest.fixture(scope="session")
def mock_code_requests() -> Dict[str, Any]:
    """Provide mock code generation requests."""
    return MOCK_CODE_GENERATION_REQUESTS.copy()


@pytest.fixture(scope="function")
def temp_code_dir() -> Generator[Path, None, None]:
    """Create temporary directory for code generation tests."""
    temp_dir = Path(tempfile.mkdtemp(prefix="code_gen_test_"))
    yield temp_dir
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture(scope="function")
def sample_code_file(temp_code_dir: Path) -> Generator[Path, None, None]:
    """Create a sample code file for testing."""
    code_file = temp_code_dir / "sample_function.py"
    sample_code = '''
"""Sample Python code for testing"""

def fibonacci(n: int) -> int:
    """Calculate fibonacci number recursively."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def test_fibonacci():
    """Test fibonacci function."""
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(5) == 5
'''
    code_file.write_text(sample_code)
    yield code_file
