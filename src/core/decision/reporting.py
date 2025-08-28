"""Reporting helpers for decision systems."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict, Any

from .decision_types import DecisionType, DecisionConfidence, DecisionMetrics


class DecisionReporter:
    """Generate metrics and status reports for decisions."""

    def __init__(self) -> None:
        self.decision_metrics: Dict[DecisionType, DecisionMetrics] = {}

    def update_execution_metrics(
        self,
        decision_type: DecisionType,
        success: bool,
        execution_time: float,
        confidence: DecisionConfidence,
    ) -> None:
        """Track execution metrics for a decision."""
        if decision_type not in self.decision_metrics:
            self.decision_metrics[decision_type] = DecisionMetrics(
                metrics_id=str(uuid.uuid4()), decision_type=decision_type
            )
        metrics = self.decision_metrics[decision_type]
        metrics.update_metrics(success, execution_time, confidence)

    def update_manager_metrics(self, core) -> None:
        """Refresh aggregate manager metrics."""
        core.metrics.operations_processed = core.total_decisions_made
        core.metrics.errors_count = core.failed_decisions
        if core.total_decisions_made > 0:
            success_rate = (
                core.successful_decisions / core.total_decisions_made
            ) * 100.0
            core.metrics.performance_score = success_rate
        core.metrics.last_operation = datetime.now()

    def build_status(self, core, base_status: Dict[str, Any]) -> Dict[str, Any]:
        """Return comprehensive decision status."""
        return {
            **base_status,
            "decision_algorithms": len(core.algorithm_executor.algorithms),
            "decision_workflows": len(core.workflow_executor.workflows),
            "decision_rules": len(core.rule_engine.rules),
            "active_decisions": len(core.tracker.active_decisions),
            "pending_decisions": len(core.tracker.pending_decisions),
            "decision_history_size": len(core.tracker.decision_history),
            "decision_operations": {
                "total": core.total_decisions_made,
                "successful": core.successful_decisions,
                "failed": core.failed_decisions,
                "success_rate": (
                    core.successful_decisions / max(1, core.total_decisions_made)
                )
                * 100.0,
                "average_execution_time": core.average_decision_time,
            },
            "cleanup_status": {
                "auto_cleanup_enabled": core.config.auto_cleanup_completed_decisions,
                "last_cleanup": core.tracker.last_cleanup_time.isoformat()
                if core.tracker.last_cleanup_time
                else None,
                "cleanup_interval_minutes": core.config.cleanup_interval_minutes,
            },
        }
