#!/usr/bin/env python3
"""
Context Metrics Models - V2 Compliance
=======================================

Metrics tracking for context retrieval operations.

Extracted from intelligent_context_models.py for V2 compliance.
Part of 13→≤5 class consolidation (ROI 90.00).

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Captain Agent-4 - Strategic Oversight
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ContextMetrics:
    """Metrics for context retrieval operations."""

    total_retrievals: int = 0
    successful_retrievals: int = 0
    failed_retrievals: int = 0
    average_execution_time_ms: float = 0.0
    total_execution_time_ms: float = 0.0
    emergency_interventions: int = 0
    agent_optimizations: int = 0
    risk_assessments: int = 0
    success_predictions: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_retrievals": self.total_retrievals,
            "successful_retrievals": self.successful_retrievals,
            "failed_retrievals": self.failed_retrievals,
            "average_execution_time_ms": self.average_execution_time_ms,
            "total_execution_time_ms": self.total_execution_time_ms,
            "emergency_interventions": self.emergency_interventions,
            "agent_optimizations": self.agent_optimizations,
            "risk_assessments": self.risk_assessments,
            "success_predictions": self.success_predictions,
            "last_updated": self.last_updated.isoformat(),
        }


__all__ = ["ContextMetrics"]
