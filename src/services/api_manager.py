"""
API Management System for Agent_Cellphone_V2_Repository
Handles API endpoints, middleware, and service discovery for integration infrastructure.
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Union
from pathlib import Path
import time
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIMethod(Enum):
    """HTTP methods supported by the API system."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class APIEndpoint:
    """Represents an API endpoint configuration."""

    path: str
    method: APIMethod
    handler: Callable
    description: str = ""
    requires_auth: bool = False
    rate_limit: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    response_schema: Optional[Dict[str, Any]] = None


@dataclass
class APIMiddleware:
    """Represents middleware configuration."""

    name: str
    handler: Callable
    priority: int = 0
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


class BaseMiddleware(ABC):
    """Abstract base class for all middleware."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.enabled = True

    @abstractmethod
    async def process(
        self, request: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process the request through this middleware."""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(enabled={self.enabled})"


class AuthenticationMiddleware(BaseMiddleware):
    """Handles authentication for protected endpoints."""

    async def process(
        self, request: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        if not self.enabled:
            return request

        # Check if endpoint requires authentication
        if request.get("requires_auth", False):
            token = request.get("headers", {}).get("Authorization")
            if not token or not self._validate_token(token):
                raise ValueError("Authentication required")

        return request

    def _validate_token(self, token: str) -> bool:
        # Simple token validation - can be enhanced
        return token.startswith("Bearer ") and len(token) > 10


class RateLimitMiddleware(BaseMiddleware):
    """Handles rate limiting for endpoints."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.request_counts: Dict[str, List[float]] = {}
        self.default_limit = config.get("default_limit", 100)
        self.window_size = config.get("window_size", 60)  # seconds

    async def process(
        self, request: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        if not self.enabled:
            return request

        endpoint = request.get("endpoint", "default")
        client_id = request.get("client_id", "anonymous")
        key = f"{client_id}:{endpoint}"

        current_time = time.time()
        limit = request.get("rate_limit", self.default_limit)

        # Clean old requests
        if key in self.request_counts:
            self.request_counts[key] = [
                req_time
                for req_time in self.request_counts[key]
                if current_time - req_time < self.window_size
            ]
        else:
            self.request_counts[key] = []

        # Check rate limit
        if len(self.request_counts[key]) >= limit:
            raise ValueError(f"Rate limit exceeded for {endpoint}")

        # Add current request
        self.request_counts[key].append(current_time)

        return request


class LoggingMiddleware(BaseMiddleware):
    """Logs all API requests and responses."""

    async def process(
        self, request: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        if not self.enabled:
            return request

        request_id = str(uuid.uuid4())
        context["request_id"] = request_id

        logger.info(
            f"API Request [{request_id}]: {request.get('method', 'UNKNOWN')} {request.get('path', 'UNKNOWN')}"
        )

        # Log request details
        if self.config.get("log_request_body", False):
            logger.debug(f"Request Body: {request.get('body', {})}")

        return request


class APIManager:
    """Manages API endpoints, middleware, and request processing."""

    def __init__(self):
        self.endpoints: Dict[str, APIEndpoint] = {}
        self.middleware: List[APIMiddleware] = []
        self.middleware_chain: List[BaseMiddleware] = []
        self._setup_default_middleware()

    def _setup_default_middleware(self):
        """Setup default middleware chain."""
        self.add_middleware(LoggingMiddleware({"log_request_body": True}), priority=100)
        self.add_middleware(AuthenticationMiddleware(), priority=200)
        self.add_middleware(
            RateLimitMiddleware({"default_limit": 100, "window_size": 60}), priority=300
        )

    def register_endpoint(self, endpoint: APIEndpoint):
        """Register a new API endpoint."""
        key = f"{endpoint.method.value}:{endpoint.path}"
        self.endpoints[key] = endpoint
        logger.info(f"Registered endpoint: {key}")

    def add_middleware(self, middleware: BaseMiddleware, priority: int = 0):
        """Add middleware to the processing chain."""
        middleware_config = APIMiddleware(
            name=middleware.__class__.__name__,
            handler=middleware,
            priority=priority,
            enabled=middleware.enabled,
        )

        self.middleware.append(middleware_config)
        self.middleware.sort(key=lambda x: x.priority)

        # Update middleware chain
        self.middleware_chain = [mw.handler for mw in self.middleware if mw.enabled]

        logger.info(
            f"Added middleware: {middleware_config.name} (priority: {priority})"
        )

    async def process_request(
        self,
        method: str,
        path: str,
        headers: Dict[str, str] = None,
        body: Any = None,
        client_id: str = None,
    ) -> Dict[str, Any]:
        """Process an API request through the middleware chain."""

        # Find endpoint
        endpoint_key = f"{method}:{path}"
        if endpoint_key not in self.endpoints:
            raise ValueError(f"Endpoint not found: {endpoint_key}")

        endpoint = self.endpoints[endpoint_key]

        # Prepare request context
        request = {
            "method": method,
            "path": path,
            "headers": headers or {},
            "body": body,
            "endpoint": path,
            "requires_auth": endpoint.requires_auth,
            "rate_limit": endpoint.rate_limit,
            "client_id": client_id,
        }

        context = {"endpoint": endpoint, "start_time": time.time()}

        try:
            # Process through middleware chain
            for middleware in self.middleware_chain:
                request = await middleware.process(request, context)

            # Execute endpoint handler
            result = await self._execute_handler(endpoint.handler, request, context)

            # Log response
            duration = time.time() - context["start_time"]
            logger.info(f"Request completed in {duration:.3f}s")

            return {
                "success": True,
                "data": result,
                "duration": duration,
                "request_id": context.get("request_id"),
            }

        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "request_id": context.get("request_id"),
            }

    async def _execute_handler(
        self, handler: Callable, request: Dict[str, Any], context: Dict[str, Any]
    ) -> Any:
        """Execute the endpoint handler."""
        if asyncio.iscoroutinefunction(handler):
            return await handler(request, context)
        else:
            return handler(request, context)

    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get list of all registered endpoints."""
        return [
            {
                "path": endpoint.path,
                "method": endpoint.method.value,
                "description": endpoint.description,
                "requires_auth": endpoint.requires_auth,
                "tags": endpoint.tags,
            }
            for endpoint in self.endpoints.values()
        ]

    def get_middleware_status(self) -> List[Dict[str, Any]]:
        """Get status of all middleware."""
        return [
            {"name": mw.name, "enabled": mw.enabled, "priority": mw.priority}
            for mw in self.middleware
        ]


# Service discovery and registration
class ServiceRegistry:
    """Manages service discovery and registration."""

    def __init__(self):
        self.services: Dict[str, Dict[str, Any]] = {}
        self.health_checks: Dict[str, Callable] = {}

    def register_service(self, name: str, config: Dict[str, Any]):
        """Register a new service."""
        self.services[name] = {
            "config": config,
            "registered_at": time.time(),
            "last_health_check": time.time(),
            "status": "healthy",
        }
        logger.info(f"Registered service: {name}")

    def unregister_service(self, name: str):
        """Unregister a service."""
        if name in self.services:
            del self.services[name]
            logger.info(f"Unregistered service: {name}")

    def get_service(self, name: str) -> Optional[Dict[str, Any]]:
        """Get service configuration."""
        return self.services.get(name)

    def list_services(self) -> List[str]:
        """List all registered services."""
        return list(self.services.keys())

    def set_health_check(self, name: str, health_check: Callable):
        """Set health check function for a service."""
        self.health_checks[name] = health_check

    async def check_service_health(self, name: str) -> bool:
        """Check health of a specific service."""
        if name not in self.health_checks:
            return True

        try:
            health_check = self.health_checks[name]
            if asyncio.iscoroutinefunction(health_check):
                result = await health_check()
            else:
                result = health_check()

            self.services[name]["last_health_check"] = time.time()
            self.services[name]["status"] = "healthy" if result else "unhealthy"

            return result
        except Exception as e:
            logger.error(f"Health check failed for {name}: {str(e)}")
            self.services[name]["status"] = "error"
            return False


# Global instances
api_manager = APIManager()
service_registry = ServiceRegistry()


# Example usage and testing
async def example_handler(
    request: Dict[str, Any], context: Dict[str, Any]
) -> Dict[str, Any]:
    """Example endpoint handler."""
    return {
        "message": "Hello from API Manager!",
        "timestamp": time.time(),
        "request_data": request,
    }


def setup_example_endpoints():
    """Setup example endpoints for testing."""
    # Register example endpoint
    example_endpoint = APIEndpoint(
        path="/api/hello",
        method=APIMethod.GET,
        handler=example_handler,
        description="Example hello endpoint",
        requires_auth=False,
        tags=["example", "hello"],
    )

    api_manager.register_endpoint(example_endpoint)

    # Register health check endpoint
    health_endpoint = APIEndpoint(
        path="/api/health",
        method=APIMethod.GET,
        handler=lambda req, ctx: {
            "status": "healthy",
            "services": service_registry.list_services(),
        },
        description="System health check",
        requires_auth=False,
        tags=["health", "monitoring"],
    )

    api_manager.register_endpoint(health_endpoint)


if __name__ == "__main__":
    # Setup example endpoints
    setup_example_endpoints()

    # Test the API manager
    async def test_api_manager():
        # Test request processing
        result = await api_manager.process_request(
            method="GET", path="/api/hello", client_id="test_client"
        )

        print("API Test Result:", json.dumps(result, indent=2))
        print("\nRegistered Endpoints:", api_manager.get_endpoints())
        print("\nMiddleware Status:", api_manager.get_middleware_status())

    # Run test
    asyncio.run(test_api_manager())
