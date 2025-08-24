"""Data aggregation module for unified financial API."""
from typing import Any, Dict


class DataAggregator:
    """Aggregate data from financial services.

    This implementation is intentionally lightweight. It simulates aggregation
    by bundling the service, request type and payload together. Real
    implementations would contain the logic for communicating with the various
    financial services.
    """

    def aggregate(
        self, target_service: str, request_type: str, request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Aggregate data for a service request."""
        return {
            "service": target_service,
            "type": request_type,
            "payload": request_data,
        }
