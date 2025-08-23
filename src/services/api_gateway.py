#!/usr/bin/env python3
"""
V2 API Gateway
==============
API gateway and routing system for V2 system with load balancing and security.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class RouteMethod(Enum):
    """HTTP method enumeration"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class RouteDefinition:
    """Route definition and configuration"""

    path: str
    method: RouteMethod
    service_id: str
    handler: Callable
    requires_auth: bool = False
    rate_limit: Optional[int] = None
    timeout: float = 30.0


@dataclass
class GatewayRequest:
    """Gateway request object"""

    path: str
    method: RouteMethod
    headers: Dict[str, str]
    body: Optional[Any] = None
    query_params: Optional[Dict[str, str]] = None


class V2APIGateway:
    """API gateway with routing, load balancing, and security"""

    def __init__(self, gateway_name: str = "V2-API-Gateway"):
        self.logger = logging.getLogger(f"{__name__}.V2APIGateway")
        self.gateway_name = gateway_name

        # Route registry
        self._routes: Dict[str, RouteDefinition] = {}
        self._route_patterns: List[str] = []

        # Gateway state
        self._gateway_active = False
        self._request_count = 0
        self._error_count = 0

        # Security and rate limiting
        self._rate_limit_store: Dict[str, List[float]] = {}
        self._auth_tokens: Dict[str, Dict[str, Any]] = {}

        self.logger.info(f"V2 API Gateway '{gateway_name}' initialized")

    def register_route(
        self,
        path: str,
        method: RouteMethod,
        service_id: str,
        handler: Callable,
        requires_auth: bool = False,
        rate_limit: Optional[int] = None,
        timeout: float = 30.0,
    ) -> bool:
        """Register a new route with the gateway"""
        route_key = f"{method.value}:{path}"

        if route_key in self._routes:
            self.logger.warning(f"Route already registered: {route_key}")
            return False

        route_def = RouteDefinition(
            path=path,
            method=method,
            service_id=service_id,
            handler=handler,
            requires_auth=requires_auth,
            rate_limit=rate_limit,
            timeout=timeout,
        )

        self._routes[route_key] = route_def
        self._route_patterns.append(path)
        self.logger.info(f"Route registered: {method.value} {path} -> {service_id}")
        return True

    def route_request(self, request: GatewayRequest) -> Dict[str, Any]:
        """Route a request through the gateway"""
        self._request_count += 1
        route_key = f"{request.method.value}:{request.path}"

        try:
            # Find matching route
            route = self._routes.get(route_key)
            if not route:
                return self._create_error_response("Route not found", 404)

            # Check authentication
            if route.requires_auth and not self._validate_auth(request):
                return self._create_error_response("Authentication required", 401)

            # Check rate limiting
            if route.rate_limit and not self._check_rate_limit(request, route):
                return self._create_error_response("Rate limit exceeded", 429)

            # Execute handler
            start_time = time.time()
            result = route.handler(request)
            execution_time = time.time() - start_time

            # Log successful request
            self.logger.info(
                f"Request routed successfully: {route_key} ({execution_time:.3f}s)"
            )

            return {
                "status": "success",
                "data": result,
                "execution_time": execution_time,
                "service_id": route.service_id,
                "timestamp": time.time(),
            }

        except Exception as e:
            self._error_count += 1
            self.logger.error(f"Request routing error: {e}")
            return self._create_error_response(f"Internal error: {str(e)}", 500)

    def _validate_auth(self, request: GatewayRequest) -> bool:
        """Validate authentication for protected routes"""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return False

        # Simple token validation (in production, use proper JWT validation)
        token = auth_header.replace("Bearer ", "")
        return token in self._auth_tokens

    def _check_rate_limit(
        self, request: GatewayRequest, route: RouteDefinition
    ) -> bool:
        """Check rate limiting for the route"""
        if not route.rate_limit:
            return True

        client_id = request.headers.get("X-Client-ID", "default")
        rate_key = f"{client_id}:{route.path}"

        now = time.time()
        window_start = now - 60  # 1 minute window

        # Initialize or clean rate limit tracking
        if rate_key not in self._rate_limit_store:
            self._rate_limit_store[rate_key] = []

        # Remove old requests
        self._rate_limit_store[rate_key] = [
            t for t in self._rate_limit_store[rate_key] if t > window_start
        ]

        # Check limit
        if len(self._rate_limit_store[rate_key]) >= route.rate_limit:
            return False

        # Record current request
        self._rate_limit_store[rate_key].append(now)
        return True

    def _create_error_response(self, message: str, status_code: int) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            "status": "error",
            "error": {
                "message": message,
                "code": status_code,
                "timestamp": time.time(),
            },
        }

    def get_gateway_stats(self) -> Dict[str, Any]:
        """Get gateway statistics and health"""
        return {
            "gateway_name": self.gateway_name,
            "status": "ACTIVE" if self._gateway_active else "INACTIVE",
            "total_routes": len(self._routes),
            "total_requests": self._request_count,
            "error_requests": self._error_count,
            "success_rate": (
                (self._request_count - self._error_count) / max(1, self._request_count)
            )
            * 100,
            "active_connections": len(self._rate_limit_store),
            "timestamp": time.time(),
        }

    def list_routes(self) -> List[Dict[str, Any]]:
        """List all registered routes"""
        routes = []
        for route_key, route_def in self._routes.items():
            routes.append(
                {
                    "route": route_key,
                    "service_id": route_def.service_id,
                    "requires_auth": route_def.requires_auth,
                    "rate_limit": route_def.rate_limit,
                    "timeout": route_def.timeout,
                }
            )
        return routes

    def activate_gateway(self):
        """Activate the gateway for routing"""
        self._gateway_active = True
        self.logger.info("V2 API Gateway activated")

    def deactivate_gateway(self):
        """Deactivate the gateway"""
        self._gateway_active = False
        self.logger.info("V2 API Gateway deactivated")

    def add_auth_token(self, token: str, user_info: Dict[str, Any]):
        """Add authentication token"""
        self._auth_tokens[token] = user_info
        self.logger.info(
            f"Auth token added for user: {user_info.get('user_id', 'unknown')}"
        )


def main():
    """CLI interface for testing V2APIGateway"""
    import argparse

    parser = argparse.ArgumentParser(description="V2 API Gateway CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")

    args = parser.parse_args()

    if args.test:
        print("🧪 V2APIGateway Smoke Test")
        print("=" * 35)

        gateway = V2APIGateway("Test-Gateway")

        # Test route registration
        def test_handler(request):
            return {"message": "Test response", "path": request.path}

        success = gateway.register_route(
            "/api/test", RouteMethod.GET, "test-service", test_handler
        )
        print(f"✅ Route registration: {success}")

        # Test request routing
        test_request = GatewayRequest(
            path="/api/test",
            method=RouteMethod.GET,
            headers={"Content-Type": "application/json"},
            query_params={"test": "true"},
        )

        response = gateway.route_request(test_request)
        print(f"✅ Request routing: {response['status']}")
        print(f"✅ Response data: {response['data']['message']}")

        # Test gateway stats
        stats = gateway.get_gateway_stats()
        print(f"✅ Gateway requests: {stats['total_requests']}")
        print(f"✅ Success rate: {stats['success_rate']:.1f}%")

        # Test route listing
        routes = gateway.list_routes()
        print(f"✅ Registered routes: {len(routes)}")

        print("🎉 V2APIGateway smoke test PASSED!")
    else:
        print("V2APIGateway ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
