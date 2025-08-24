import logging
from .models import CrossAgentRequest, CrossAgentResponse

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Create standardized error responses and logging."""

    def handle(self, error: Exception, request: CrossAgentRequest, response_time: float) -> CrossAgentResponse:
        logger.error(f"Error processing request {request.request_id}: {error}")
        return CrossAgentResponse(
            request_id=request.request_id,
            response_data=None,
            response_time=response_time,
            status="ERROR",
            error_message=str(error),
        )
