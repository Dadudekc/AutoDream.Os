from typing import Any

from .models import CrossAgentResponse


def create_success_response(request_id: str, data: Any, response_time: float) -> CrossAgentResponse:
    """Create a successful CrossAgentResponse."""
    return CrossAgentResponse(
        request_id=request_id,
        response_data=data,
        response_time=response_time,
        status="SUCCESS",
    )


def create_error_response(request_id: str, error: Exception, response_time: float) -> CrossAgentResponse:
    """Create an error CrossAgentResponse."""
    return CrossAgentResponse(
        request_id=request_id,
        response_data={"error": str(error)},
        response_time=response_time,
        status="ERROR",
    )
