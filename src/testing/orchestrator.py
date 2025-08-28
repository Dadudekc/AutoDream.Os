from pathlib import Path
from typing import Dict, Any

from src.utils.logger import get_logger
from . import planning, execution, monitoring

logger = get_logger(__name__)

class TestOrchestrator:
    """Lightweight orchestrator sequencing planning, execution, and monitoring."""
    __test__ = False  # Prevent pytest from collecting this class

    def __init__(self, source_dir: Path, tests_dir: Path):
        self.source_dir = Path(source_dir)
        self.tests_dir = Path(tests_dir)

    def run(self) -> Dict[str, Any]:
        test_plan = planning.collect_tests(self.tests_dir)
        result = execution.run_tests(test_plan, self.source_dir)
        return monitoring.summarize(result)
