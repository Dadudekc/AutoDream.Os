from pathlib import Path
from typing import List

from src.utils.logger import get_logger

logger = get_logger(__name__)

def collect_tests(tests_dir: Path) -> List[Path]:
    """Gather test files from the given directory."""
    test_files = sorted(Path(tests_dir).glob("test_*.py"))
    logger.info("Collected %d test file(s)", len(test_files))
    return test_files
