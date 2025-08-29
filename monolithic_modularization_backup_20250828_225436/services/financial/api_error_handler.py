from datetime import datetime
from typing import Any, Dict, TYPE_CHECKING

    from .unified_financial_api import CrossAgentRequest, CrossAgentResponse
from __future__ import annotations


"""Error handling utilities for UnifiedFinancialAPI."""


if TYPE_CHECKING:  # pragma: no cover


class APIErrorHandler:
    """Provides standardized error handling for service execution."""

    def handle(
        self,
        request_id: str,
        error: Exception,
        request: "CrossAgentRequest",
        performance_metrics: Dict[str, Dict[str, Any]],
        response_cls,
    ) -> "CrossAgentResponse":
        """Update tracking data and create error response."""
        request.status = "ERROR"
        source_agent = request.source_agent
        if source_agent in performance_metrics:
            performance_metrics[source_agent]["failed_requests"] += 1
            performance_metrics[source_agent]["last_updated"] = datetime.now().isoformat()

        return response_cls(
            request_id=request_id,
            response_data=None,
            response_time=0.0,
            status="ERROR",
            error_message=str(error),
        )
