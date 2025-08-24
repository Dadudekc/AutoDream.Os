"""Utilities for configuring and discovering tests."""
from pathlib import Path
from typing import Any, Dict, List

# Default configuration used by the orchestrator.
DEFAULT_CONFIG: Dict[str, Any] = {
    "test_directory": "tests",
    "timeout": 30,
}


def initialize_config(overrides: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Return the test configuration with optional overrides."""
    config = DEFAULT_CONFIG.copy()
    if overrides:
        config.update(overrides)
    return config


def discover_tests(test_directory: str) -> List[str]:
    """Discover pytest files within ``test_directory``."""
    path = Path(test_directory)
    if not path.exists():
        return []
    return [str(p) for p in path.rglob("test_*.py")]
