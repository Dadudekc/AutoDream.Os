from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class TestConfig:
    """Configuration for test discovery."""
    test_directory: str = "tests"


def discover_tests(config: TestConfig) -> List[str]:
    """Locate test files within the configured directory.

    Parameters
    ----------
    config: TestConfig
        Configuration specifying where tests reside.

    Returns
    -------
    list[str]
        Paths to discovered test files.
    """
    test_path = Path(config.test_directory)
    if not test_path.exists():
        return []
    return [str(p) for p in test_path.rglob("test_*.py")]
