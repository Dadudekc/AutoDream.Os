from pathlib import Path
from typing import Dict, Any

from .logging_utils import setup_logger
from .resource import ResourceOrchestrator
from .scheduler import TaskScheduler

logger = setup_logger(__name__)

class TestOrchestrator:
    """Lightweight orchestrator sequencing planning, execution, and monitoring."""
    __test__ = False  # Prevent pytest from collecting this class

    def __init__(self, source_dir: Path, tests_dir: Path) -> None:
        self.resources = ResourceOrchestrator(source_dir)
        self.scheduler = TaskScheduler(source_dir, tests_dir)

    def run(self) -> Dict[str, Any]:
        """Prepare resources and execute scheduled tests."""
        self.resources.prepare()
        result = self.scheduler.execute()
        logger.info("Test execution completed")
        return result
