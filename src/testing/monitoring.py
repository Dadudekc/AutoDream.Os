from typing import Dict, Any

from .logging_utils import setup_logger

logger = setup_logger(__name__)

def summarize(result: Dict[str, Any]) -> Dict[str, Any]:
    """Log and return execution results."""
    logger.info("Tests passed: %s", result.get("passed"))
    logger.info("Coverage: %.2f", result.get("coverage", 0.0))
    return result
