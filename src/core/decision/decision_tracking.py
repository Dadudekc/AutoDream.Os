"""Decision tracking utilities.

This module centralizes logic for tracking active, pending and
historical decisions to avoid duplication across the codebase."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Any, Optional

from .decision_types import DecisionRequest, DecisionResult, DecisionConfidence


class DecisionTracker:
    """Track active and historical decisions."""

    def __init__(self) -> None:
        self.active_decisions: Dict[str, Dict[str, Any]] = {}
        self.decision_history: List[DecisionResult] = []
        self.pending_decisions: Dict[str, DecisionRequest] = {}
        self.last_cleanup_time: Optional[datetime] = None

    # ------------------------------------------------------------------
    # Tracking helpers
    # ------------------------------------------------------------------
    def start_decision(
        self,
        request: DecisionRequest,
        algorithm_id: Optional[str],
        workflow_id: Optional[str],
    ) -> None:
        """Record a new active decision."""
        self.pending_decisions[request.decision_id] = request
        self.active_decisions[request.decision_id] = {
            "request": request,
            "start_time": datetime.now(),
            "status": "processing",
            "algorithm_id": algorithm_id,
            "workflow_id": workflow_id,
        }

    def complete_decision(
        self, decision_id: str, result: DecisionResult, execution_time: float
    ) -> None:
        """Mark a decision as completed and move to history."""
        data = self.active_decisions.get(decision_id)
        if data:
            data.update(
                {
                    "status": "completed",
                    "result": result,
                    "execution_time": execution_time,
                }
            )
        self.decision_history.append(result)
        self.pending_decisions.pop(decision_id, None)

    def record_failure(
        self, decision_id: str, result: DecisionResult, error: str
    ) -> None:
        """Record a failed decision."""
        data = self.active_decisions.get(decision_id)
        if data:
            data.update({"status": "failed", "result": result, "error": error})

    # ------------------------------------------------------------------
    # Maintenance helpers
    # ------------------------------------------------------------------
    def check_timeouts(self, timeout_seconds: int, logger) -> None:
        """Update any decisions that exceed the timeout threshold."""
        current_time = datetime.now()
        for decision_id, info in list(self.active_decisions.items()):
            if info["status"] != "processing":
                continue
            elapsed = (current_time - info["start_time"]).total_seconds()
            if elapsed > timeout_seconds:
                info["status"] = "timeout"
                info["result"] = DecisionResult(
                    decision_id=decision_id,
                    outcome="decision_timeout",
                    confidence=DecisionConfidence.VERY_LOW,
                    reasoning="Decision exceeded timeout limit",
                )
                logger.warning(f"Decision {decision_id} timed out")
