"""Performance tuning utilities for AI agents.

The tuner analyses basic metrics and adjusts configuration parameters
such as learning rates.  It deliberately keeps the logic simple so
that sophisticated tuning algorithms can be plugged in later without
modifying the public interface.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class AIAgentPerformanceTuner:
    """Adjust runtime parameters to improve agent performance."""

    def __init__(self, threshold: float = 0.8) -> None:
        self.threshold = threshold

    def assess(self, metrics: Dict[str, float]) -> bool:
        """Return ``True`` if performance falls below the threshold."""

        score = metrics.get("score", 1.0)
        logger.debug("Assessing performance score %.3f against threshold %.3f", score, self.threshold)
        return score < self.threshold

    def tune(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Adjust configuration parameters to improve performance.

        Currently this function simply decreases the learning rate by ten
        percent if present.  Future versions can implement more
        sophisticated logic without changing the calling convention.
        """

        lr = config.get("learning_rate")
        if lr is not None:
            new_lr = lr * 0.9
            config["learning_rate"] = new_lr
            logger.debug("Tuned learning rate from %s to %s", lr, new_lr)
        return config
