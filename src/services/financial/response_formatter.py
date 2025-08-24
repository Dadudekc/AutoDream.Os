"""Response formatting module for unified financial API."""
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CrossAgentResponse:
    """Standardised response object for API calls."""

    request_id: str
    response_data: Any
    response_time: float
    status: str
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ResponseFormatter:
    """Format data into :class:`CrossAgentResponse` objects."""

    def format(
        self,
        request_id: str,
        data: Any,
        response_time: float,
        status: str = "SUCCESS",
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CrossAgentResponse:
        return CrossAgentResponse(
            request_id=request_id,
            response_data=data,
            response_time=response_time,
            status=status,
            error_message=error_message,
            metadata=metadata or {},
        )
