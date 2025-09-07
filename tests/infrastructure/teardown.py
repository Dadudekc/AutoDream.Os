"""Teardown utilities for summarizing test results."""

<<<<<<< HEAD
=======
from typing import Any, Dict

from src.utils.logger import get_logger

>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
logger = get_logger(__name__)


def perform_teardown(result: Dict[str, Any]) -> Dict[str, Any]:
    """Log summary information and return ``result``."""
<<<<<<< HEAD
    get_logger(__name__).info("Tests passed: %s", result.get("passed"))
    get_logger(__name__).info("Coverage: %.2f", result.get("coverage", 0.0))
=======
    logger.info("Tests passed: %s", result.get("passed"))
    logger.info("Coverage: %.2f", result.get("coverage", 0.0))
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
    return result
