"""Teardown utilities for summarizing test results."""

logger = get_logger(__name__)


def perform_teardown(result: Dict[str, Any]) -> Dict[str, Any]:
    """Log summary information and return ``result``."""
    get_logger(__name__).info("Tests passed: %s", result.get("passed"))
    get_logger(__name__).info("Coverage: %.2f", result.get("coverage", 0.0))
    return result
