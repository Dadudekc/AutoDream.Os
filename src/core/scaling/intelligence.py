"""Intelligent scaling strategy utilities."""

import logging
import time
from typing import Any, Dict

from .types import ScalingStatus

logger = logging.getLogger(__name__)


def create_intelligent_scaling_strategy(
    manager: Any, strategy_type: str, parameters: Dict[str, Any]
) -> str:
    """Create an intelligent scaling strategy with adaptive parameters."""
    try:
        strategy_id = f"intelligent_scaling_{strategy_type}_{int(time.time())}"
        if strategy_type == "adaptive_threshold":
            strategy_config = {
                "id": strategy_id,
                "type": "adaptive_threshold",
                "description": "Dynamically adjust scaling thresholds based on performance patterns",
                "parameters": {
                    **parameters,
                    "learning_rate": parameters.get("learning_rate", 0.1),
                    "adaptation_window": parameters.get("adaptation_window", 3600),
                    "threshold_variance": parameters.get("threshold_variance", 0.2),
                },
            }
        elif strategy_type == "predictive_scaling":
            strategy_config = {
                "id": strategy_id,
                "type": "predictive_scaling",
                "description": "Predict scaling needs based on historical patterns and trends",
                "parameters": {
                    **parameters,
                    "prediction_horizon": parameters.get("prediction_horizon", 1800),
                    "confidence_threshold": parameters.get("confidence_threshold", 0.8),
                    "pattern_recognition": parameters.get("pattern_recognition", True),
                },
            }
        elif strategy_type == "cost_optimized":
            strategy_config = {
                "id": strategy_id,
                "type": "cost_optimized",
                "description": "Optimize scaling decisions based on cost-performance trade-offs",
                "parameters": {
                    **parameters,
                    "cost_per_instance": parameters.get("cost_per_instance", 1.0),
                    "performance_target": parameters.get("performance_target", 0.9),
                    "budget_constraint": parameters.get("budget_constraint", 100.0),
                },
            }
        else:
            raise ValueError(f"Unknown scaling strategy type: {strategy_type}")

        if not hasattr(manager, "intelligent_strategies"):
            manager.intelligent_strategies = {}
        manager.intelligent_strategies[strategy_id] = strategy_config
        logger.info("Created intelligent scaling strategy: %s", strategy_id)
        return strategy_id
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to create intelligent scaling strategy: %s", exc)
        raise


def execute_intelligent_scaling(
    manager: Any, strategy_id: str, current_metrics: Any
) -> Dict[str, Any]:
    """Execute intelligent scaling strategy using manager components."""
    try:
        decision = manager.scaling_decider.decide(current_metrics, manager.scaling_config)
        new_instances, status = manager.scaling_executor.execute(
            decision.action, manager.current_instances, manager.scaling_config
        )
        manager.current_instances = new_instances
        manager.scaling_status = status
        manager.decision_history.append(decision)
        result = {
            "strategy_id": strategy_id,
            "strategy_type": "rule_based",
            "scaling_action": decision.action,
            "reasoning": decision.reason,
            "confidence": decision.confidence,
            "performance_impact": {},
            "execution_success": status != ScalingStatus.IDLE,
        }
        logger.info("Intelligent scaling executed: %s", strategy_id)
        return result
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to execute intelligent scaling: %s", exc)
        raise
