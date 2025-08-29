"""Teardown stage utilities for the testing orchestrator."""

from typing import Any, Dict

from src.utils.logger import get_logger

logger = get_logger(__name__)


def perform_teardown(result: Dict[str, Any]) -> Dict[str, Any]:
    """Log summary information and return ``result``."""
    logger.info("Tests passed: %s", result.get("passed"))
    logger.info("Coverage: %.2f", result.get("coverage", 0.0))
    return result

