"""Task scheduling for orchestrated test execution."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, List

from . import planning, execution, monitoring
from .logging_utils import setup_logger


class TaskScheduler:
    """Schedule test tasks and aggregate results."""

    def __init__(self, source_dir: Path, tests_dir: Path) -> None:
        self.source_dir = Path(source_dir)
        self.tests_dir = Path(tests_dir)
        self.logger = setup_logger(__name__)

    def execute(self) -> Dict[str, Any]:
        """Plan, run, and summarize tests."""
        test_plan: List[Path] = planning.collect_tests(self.tests_dir)
        result = execution.run_tests(test_plan, self.source_dir)
        self.logger.info("Scheduled %d test(s)", len(test_plan))
        return monitoring.summarize(result)
