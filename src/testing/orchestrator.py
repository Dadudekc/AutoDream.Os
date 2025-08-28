"""Testing orchestrator coordinating setup, execution, and teardown stages."""

from pathlib import Path
from typing import Any, Dict

from src.utils.logger import get_logger

from . import execution_stage, setup_stage, teardown_stage

logger = get_logger(__name__)


class TestOrchestrator:
    """Lightweight orchestrator sequencing setup, execution, and teardown."""

    __test__ = False  # Prevent pytest from collecting this class

    def __init__(self, source_dir: Path, tests_dir: Path) -> None:
        self.source_dir = Path(source_dir)
        self.tests_dir = Path(tests_dir)

    def run(self) -> Dict[str, Any]:
        """Run all orchestration stages and return aggregated results."""
        test_plan = setup_stage.prepare_tests(self.tests_dir)
        result = execution_stage.run_tests(test_plan, self.source_dir)
        return teardown_stage.perform_teardown(result)

