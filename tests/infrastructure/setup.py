"""Environment setup utilities for collecting test files."""




logger = get_logger(__name__)


def prepare_tests(tests_dir: Path) -> List[Path]:
    """Discover test files in ``tests_dir`` matching ``TEST_FILE_PATTERN``."""
    test_files = sorted(get_unified_utility().Path(tests_dir).glob(TEST_FILE_PATTERN))
    get_logger(__name__).info("Collected %d test file(s)", len(test_files))
    return test_files
