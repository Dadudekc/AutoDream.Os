"""Coordinator module invoking setup, execution, and teardown steps."""

from pathlib import Path
from typing import Any, Dict

from src.utils.logger import get_logger

from .infrastructure import executor, setup, teardown

logger = get_logger(__name__)


class TestCoordinator:
    """Sequence test setup, execution, and teardown."""

    __test__ = False  # Prevent pytest from collecting this class

    def __init__(self, source_dir: Path, tests_dir: Path) -> None:
        self.source_dir = Path(source_dir)
        self.tests_dir = Path(tests_dir)

    def run(self) -> Dict[str, Any]:
        """Run all coordination steps and return aggregated results."""
        test_plan = setup.prepare_tests(self.tests_dir)
        result = executor.run_tests(test_plan, self.source_dir)
        return teardown.perform_teardown(result)
