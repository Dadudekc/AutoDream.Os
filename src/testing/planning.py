from pathlib import Path
from typing import List

from .logging_utils import setup_logger

logger = setup_logger(__name__)

def collect_tests(tests_dir: Path) -> List[Path]:
    """Gather test files from the given directory."""
    test_files = sorted(Path(tests_dir).glob("test_*.py"))
    logger.info("Collected %d test file(s)", len(test_files))
    return test_files
