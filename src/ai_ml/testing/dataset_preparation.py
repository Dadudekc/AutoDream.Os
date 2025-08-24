import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class DatasetPreparer:
    """Prepare test datasets by discovering and generating test files."""

    def __init__(self, test_dir: str):
        self.test_dir = Path(test_dir)
        self.generated_tests: List[str] = []

    def discover_tests(self) -> List[str]:
        """Return a list of discovered test files."""
        tests = [str(p) for p in self.test_dir.rglob('test_*.py') if p.is_file()]
        logger.info("Discovered %d test files", len(tests))
        return tests

    def generate_test_file(self, name: str = "test_generated.py") -> str:
        """Generate a simple passing test file for evaluation."""
        path = self.test_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("""import pytest\n\n\ndef test_placeholder():\n    assert True\n""")
        self.generated_tests.append(str(path))
        logger.info("Generated test file: %s", path)
        return str(path)
