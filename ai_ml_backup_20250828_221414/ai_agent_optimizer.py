from typing import Any, Dict
import logging

from ..core.learning import UnifiedLearningEngine, LearningManager
from .ai_agent_performance_tuner import AIAgentPerformanceTuner
from .ai_agent_resource_manager import AIAgentResourceManager
from __future__ import annotations

"""High level orchestrator for AI agent optimization - MIGRATED TO UNIFIED LEARNING ENGINE.

This module wires together the unified learning engine optimization capabilities.
It exposes a simple ``optimize`` method that can be used by other components.
"""



# MIGRATED: Using unified learning engine instead of local implementation

logger = logging.getLogger(__name__)


class AIAgentOptimizer:
    """Coordinate optimization using unified learning engine - MIGRATED TO UNIFIED ENGINE."""

    def __init__(self) -> None:
        # MIGRATED: Using unified learning engine instead of local AIAgentOptimizerCore
        self.learning_engine = UnifiedLearningEngine()
        self.learning_manager = LearningManager()
        self.tuner = AIAgentPerformanceTuner()
        self.resources = AIAgentResourceManager()

    def optimize(self, state: Dict[str, Any], metrics: Dict[str, float]) -> Dict[str, Any]:
        """Optimize an agent state based on current metrics - MIGRATED TO UNIFIED ENGINE.

        The method allocates minimal resources, applies unified learning engine
        optimization strategies and optionally performs performance tuning
        if metrics indicate sub‑optimal behaviour.  Resources are released
        after processing regardless of success.
        """

        self.resources.allocate({"cpu": 1})
        try:
            # MIGRATED: Using unified learning engine optimization
            optimized = self.learning_engine.optimize_agent_state(state, metrics)
            if self.tuner.assess(metrics):
                optimized = self.tuner.tune(optimized)
            return optimized
        finally:  # pragma: no cover - ensure release even on failure
            self.resources.release({"cpu": 1})
