"""Request handling module for unified financial API."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict
import uuid

from .response_formatter import ResponseFormatter, CrossAgentResponse


@dataclass
class CrossAgentRequest:
    """Representation of a pending request."""

    request_id: str
    source_agent: str
    target_service: str
    request_type: str
    request_data: Dict[str, Any]
    timestamp: datetime
    priority: str
    status: str = "PENDING"


class RequestHandler:
    """Create and execute requests using the provided modules."""

    def __init__(self, aggregator, normalizer, formatter: ResponseFormatter):
        self.aggregator = aggregator
        self.normalizer = normalizer
        self.formatter = formatter
        self.active_requests: Dict[str, CrossAgentRequest] = {}

    def create_request(
        self,
        source_agent: str,
        target_service: str,
        request_type: str,
        request_data: Dict[str, Any],
        priority: str = "MEDIUM",
    ) -> str:
        request_id = str(uuid.uuid4())
        self.active_requests[request_id] = CrossAgentRequest(
            request_id=request_id,
            source_agent=source_agent,
            target_service=target_service,
            request_type=request_type,
            request_data=request_data,
            timestamp=datetime.now(),
            priority=priority,
        )
        return request_id

    def execute_request(self, request_id: str) -> CrossAgentResponse:
        request = self.active_requests[request_id]
        request.status = "PROCESSING"
        start = datetime.now().timestamp()
        raw_data = self.aggregator.aggregate(
            request.target_service, request.request_type, request.request_data
        )
        normalized = self.normalizer.normalize(raw_data)
        request.status = "COMPLETED"
        response_time = datetime.now().timestamp() - start
        return self.formatter.format(request_id, normalized, response_time)
