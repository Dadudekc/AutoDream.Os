#!/usr/bin/env python3
"""
Context Results Models - V2 Compliance
=======================================

Search and retrieval result structures.

Extracted from intelligent_context_models.py for V2 compliance.
Part of 13→≤5 class consolidation (ROI 90.00).

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Captain Agent-4 - Strategic Oversight
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .mission_models import MissionContext


@dataclass
class SearchResult:
    """Search result structure."""

    result_id: str
    content: str
    relevance_score: float
    source_type: str
    source_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "result_id": self.result_id,
            "content": self.content,
            "relevance_score": self.relevance_score,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ContextRetrievalResult:
    """Result of context retrieval operation."""

    success: bool
    mission_context: MissionContext | None = None
    search_results: list[SearchResult] = field(default_factory=list)
    agent_recommendations: list[dict[str, Any]] = field(default_factory=list)
    risk_assessment: dict[str, Any] | None = None
    success_prediction: dict[str, Any] | None = None
    execution_time_ms: float = 0.0
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "mission_context": (self.mission_context.to_dict() if self.mission_context else None),
            "search_results": [r.to_dict() for r in self.search_results],
            "agent_recommendations": self.agent_recommendations,
            "risk_assessment": self.risk_assessment,
            "success_prediction": self.success_prediction,
            "execution_time_ms": self.execution_time_ms,
            "error_message": self.error_message,
        }


__all__ = ["SearchResult", "ContextRetrievalResult"]
