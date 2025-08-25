"""High level orchestrator for AI agent optimization.

This module wires together the core optimizer, performance tuner and
resource manager.  It exposes a simple ``optimize`` method that can be
used by other components without needing to know about the underlying
modules.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from .ai_agent_optimizer_core import AIAgentOptimizerCore
from .ai_agent_performance_tuner import AIAgentPerformanceTuner
from .ai_agent_resource_manager import AIAgentResourceManager

logger = logging.getLogger(__name__)


class AIAgentOptimizer:
    """Coordinate optimization, tuning and resource management."""

    def __init__(self) -> None:
        self.core = AIAgentOptimizerCore()
        self.tuner = AIAgentPerformanceTuner()
        self.resources = AIAgentResourceManager()

    def optimize(self, state: Dict[str, Any], metrics: Dict[str, float]) -> Dict[str, Any]:
        """Optimize an agent state based on current metrics.

        The method allocates minimal resources, applies registered
        optimization strategies and optionally performs performance tuning
        if metrics indicate sub‑optimal behaviour.  Resources are released
        after processing regardless of success.
        """

        self.resources.allocate({"cpu": 1})
        try:
            optimized = self.core.optimize(state)
            if self.tuner.assess(metrics):
                optimized = self.tuner.tune(optimized)
            return optimized
        finally:  # pragma: no cover - ensure release even on failure
            self.resources.release({"cpu": 1})
