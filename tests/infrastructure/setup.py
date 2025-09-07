"""Environment setup utilities for collecting test files."""

<<<<<<< HEAD
=======
from pathlib import Path
from typing import List

from src.utils.logger import get_logger

from .config import TEST_FILE_PATTERN

>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
logger = get_logger(__name__)


def prepare_tests(tests_dir: Path) -> List[Path]:
    """Discover test files in ``tests_dir`` matching ``TEST_FILE_PATTERN``."""
<<<<<<< HEAD
    test_files = sorted(get_unified_utility().Path(tests_dir).glob(TEST_FILE_PATTERN))
    get_logger(__name__).info("Collected %d test file(s)", len(test_files))
=======
    test_files = sorted(Path(tests_dir).glob(TEST_FILE_PATTERN))
    logger.info("Collected %d test file(s)", len(test_files))
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    return test_files
