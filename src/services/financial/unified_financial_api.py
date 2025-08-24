"""Simplified unified financial API orchestrating dedicated modules."""
from typing import Any, Dict

from .data_aggregator import DataAggregator
from .data_normalizer import DataNormalizer
from .request_handler import RequestHandler
from .response_formatter import ResponseFormatter, CrossAgentResponse


class UnifiedFinancialAPI:
    """High level facade coordinating request flow."""

    def __init__(self) -> None:
        self.aggregator = DataAggregator()
        self.normalizer = DataNormalizer()
        self.formatter = ResponseFormatter()
        self.request_handler = RequestHandler(
            self.aggregator, self.normalizer, self.formatter
        )

    def handle_request(
        self,
        source_agent: str,
        target_service: str,
        request_type: str,
        request_data: Dict[str, Any],
        priority: str = "MEDIUM",
    ) -> CrossAgentResponse:
        """Create and execute a request through the API layer."""
        request_id = self.request_handler.create_request(
            source_agent, target_service, request_type, request_data, priority
        )
        return self.request_handler.execute_request(request_id)
