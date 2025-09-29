#!/usr/bin/env python3
"""
V3-011: API Gateway Core Implementation
=======================================

Core API Gateway functionality with V2 compliance.
Maintains essential features while staying under 400 lines.
"""

import hashlib
import logging
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


class AuthMethod(Enum):
    """Authentication methods."""

    JWT = "jwt"
    API_KEY = "api_key"
    BASIC = "basic"
    NONE = "none"


class RateLimitType(Enum):
    """Rate limiting types."""

    PER_MINUTE = "per_minute"
    PER_HOUR = "per_hour"
    PER_DAY = "per_day"


@dataclass
class EndpointConfig:
    """API endpoint configuration."""

    path: str
    method: str
    handler: callable
    auth_required: bool = True
    rate_limit: int | None = None
    rate_limit_type: RateLimitType = RateLimitType.PER_MINUTE


@dataclass
class RequestContext:
    """Request context information."""

    path: str
    method: str
    headers: dict[str, str]
    body: str | None
    client_ip: str
    timestamp: datetime
    request_id: str


@dataclass
class Response:
    """API response structure."""

    status_code: int
    body: dict[str, Any]
    headers: dict[str, str]
    timestamp: datetime


class RateLimiter:
    """Rate limiting implementation."""

    def __init__(self):
        self.requests = {}  # client_ip -> list of timestamps

    def is_allowed(self, client_ip: str, limit: int, window_seconds: int) -> bool:
        """Check if request is allowed based on rate limit."""
        now = time.time()
        window_start = now - window_seconds

        # Clean old requests
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip] if req_time > window_start
            ]
        else:
            self.requests[client_ip] = []

        # Check limit
        if len(self.requests[client_ip]) >= limit:
            return False

        # Add current request
        self.requests[client_ip].append(now)
        return True


class Authenticator:
    """Authentication handler."""

    def __init__(self):
        self.api_keys = {}  # In production, use secure storage
        self.jwt_secret = "v3_api_gateway_secret"  # Use environment variable

    def authenticate(self, headers: dict[str, str], method: AuthMethod) -> bool:
        """Authenticate request based on method."""
        if method == AuthMethod.NONE:
            return True

        if method == AuthMethod.API_KEY:
            api_key = headers.get("X-API-Key")
            return api_key in self.api_keys

        if method == AuthMethod.JWT:
            token = headers.get("Authorization", "").replace("Bearer ", "")
            return self._validate_jwt(token)

        return False

    def _validate_jwt(self, token: str) -> bool:
        """Validate JWT token (simplified)."""
        # In production, use proper JWT validation
        return len(token) > 10


class APIGateway:
    """Main API Gateway implementation."""

    def __init__(self):
        self.endpoints = {}
        self.rate_limiter = RateLimiter()
        self.authenticator = Authenticator()
        self.request_count = 0
        self.start_time = datetime.now()

    def register_endpoint(
        self,
        path: str,
        method: str,
        handler: callable,
        auth_required: bool = True,
        rate_limit: int | None = None,
    ):
        """Register API endpoint."""
        key = f"{method.upper()}:{path}"
        self.endpoints[key] = EndpointConfig(
            path=path,
            method=method.upper(),
            handler=handler,
            auth_required=auth_required,
            rate_limit=rate_limit,
        )
        logger.info(f"Registered endpoint: {key}")

    def handle_request(
        self,
        path: str,
        method: str,
        headers: dict[str, str],
        body: str | None = None,
        client_ip: str = "127.0.0.1",
    ) -> Response:
        """Handle incoming API request."""
        self.request_count += 1
        request_id = self._generate_request_id()

        context = RequestContext(
            path=path,
            method=method.upper(),
            headers=headers,
            body=body,
            client_ip=client_ip,
            timestamp=datetime.now(),
            request_id=request_id,
        )

        # Find endpoint
        key = f"{method.upper()}:{path}"
        endpoint = self.endpoints.get(key)

        if not endpoint:
            return self._create_error_response(404, "Endpoint not found")

        # Check rate limiting
        if endpoint.rate_limit:
            if not self.rate_limiter.is_allowed(client_ip, endpoint.rate_limit, 60):
                return self._create_error_response(429, "Rate limit exceeded")

        # Check authentication
        if endpoint.auth_required:
            if not self.authenticator.authenticate(headers, AuthMethod.API_KEY):
                return self._create_error_response(401, "Authentication required")

        # Execute handler
        try:
            result = endpoint.handler(path, method, headers, body)
            return Response(
                status_code=result.get("status_code", 200),
                body=result.get("body", {}),
                headers=result.get("headers", {}),
                timestamp=datetime.now(),
            )
        except Exception as e:
            logger.error(f"Handler error: {e}")
            return self._create_error_response(500, "Internal server error")

    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        return hashlib.md5(f"{self.request_count}{time.time()}".encode()).hexdigest()[:8]

    def _create_error_response(self, status_code: int, message: str) -> Response:
        """Create error response."""
        return Response(
            status_code=status_code,
            body={"error": message, "timestamp": datetime.now().isoformat()},
            headers={"Content-Type": "application/json"},
            timestamp=datetime.now(),
        )

    def get_health_status(self) -> dict[str, Any]:
        """Get API Gateway health status."""
        uptime = (datetime.now() - self.start_time).total_seconds()

        return {
            "status": "healthy",
            "uptime_seconds": uptime,
            "endpoints_registered": len(self.endpoints),
            "total_requests": self.request_count,
            "authentication_enabled": True,
            "rate_limiting_enabled": True,
            "timestamp": datetime.now().isoformat(),
        }

    def generate_api_documentation(self) -> dict[str, Any]:
        """Generate API documentation."""
        endpoints = []

        for key, endpoint in self.endpoints.items():
            endpoints.append(
                {
                    "path": endpoint.path,
                    "method": endpoint.method,
                    "auth_required": endpoint.auth_required,
                    "rate_limit": endpoint.rate_limit,
                }
            )

        return {
            "title": "V3 API Gateway",
            "version": "1.0.0",
            "endpoints": endpoints,
            "total_endpoints": len(endpoints),
            "generated_at": datetime.now().isoformat(),
        }


def main():
    """Main execution function."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    try:
        # Initialize API Gateway
        gateway = APIGateway()

        # Register sample endpoints
        def sample_handler(
            path: str, method: str, headers: dict[str, str], body: str | None
        ) -> dict[str, Any]:
            return {
                "status_code": 200,
                "body": {"message": f"Hello from {path}", "method": method},
                "headers": {"Content-Type": "application/json"},
            }

        gateway.register_endpoint("/health", "GET", sample_handler, auth_required=False)
        gateway.register_endpoint("/status", "GET", sample_handler)
        gateway.register_endpoint("/agents", "GET", sample_handler)

        # Generate documentation
        docs = gateway.generate_api_documentation()

        # Get health status
        health = gateway.get_health_status()

        print("✅ V3-011 API Gateway Core completed successfully!")
        print(f"📊 Endpoints registered: {health['endpoints_registered']}")
        print(f"📚 API documentation generated: {len(docs['endpoints'])} endpoints")
        print(f"🔒 Authentication: {health['authentication_enabled']}")
        print(f"⚡ Rate limiting: {health['rate_limiting_enabled']}")

        return 0

    except Exception as e:
        logger.error(f"V3-011 implementation error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
