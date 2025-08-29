from typing import Dict, Callable, Any


class RequestRouter:
    """Route requests to the appropriate financial service"""

    def __init__(self, service_map: Dict[str, Callable[[str, Dict[str, Any]], Any]]):
        self._service_map = service_map

    def route(self, target_service: str, request_type: str, request_data: Dict[str, Any]) -> Any:
        if target_service not in self._service_map:
            raise ValueError(f"Unknown service: {target_service}")
        handler = self._service_map[target_service]
        return handler(request_type, request_data)
