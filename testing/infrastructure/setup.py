"""Environment setup utilities for collecting test files."""

from pathlib import Path
from typing import List

from src.utils.logger import get_logger

from .config import TEST_FILE_PATTERN

logger = get_logger(__name__)


def prepare_tests(tests_dir: Path) -> List[Path]:
    """Discover test files in ``tests_dir`` matching ``TEST_FILE_PATTERN``."""
    test_files = sorted(Path(tests_dir).glob(TEST_FILE_PATTERN))
    logger.info("Collected %d test file(s)", len(test_files))
    return test_files
