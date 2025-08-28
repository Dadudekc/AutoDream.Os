from typing import Dict, Any

from src.utils.logger import get_logger

logger = get_logger(__name__)

def summarize(result: Dict[str, Any]) -> Dict[str, Any]:
    """Log and return execution results."""
    logger.info("Tests passed: %s", result.get("passed"))
    logger.info("Coverage: %.2f", result.get("coverage", 0.0))
    return result
