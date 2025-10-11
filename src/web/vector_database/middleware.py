"""
Vector Database Middleware
=========================

Request/response processing middleware for vector database operations.
V2 Compliance: < 300 lines, single responsibility, middleware processing.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring

CONSOLIDATED: 4 middleware files unified into unified_middleware.py (Agent-7, 2025-10-10)
- ErrorHandlerMiddleware: Error handling decorators
- RequestHandlerMiddleware: Request processing decorators
- ResponseHandlerMiddleware: Response processing decorators
- ValidationMiddleware: Validation decorators
"""

from .unified_middleware import UnifiedVectorMiddleware

# Backward compatibility exports
ErrorHandlerMiddleware = UnifiedVectorMiddleware
RequestHandlerMiddleware = UnifiedVectorMiddleware
ResponseHandlerMiddleware = UnifiedVectorMiddleware
ValidationMiddleware = UnifiedVectorMiddleware


class VectorDatabaseMiddleware:
    """Main middleware orchestrator for vector database operations.

    V2 Compliance: < 100 lines, facade pattern, single responsibility.
    This class orchestrates all middleware components.

    Provides both instance methods and class-level shortcuts for decorator usage.
    """

    # Module-level instance for class decorator usage
    _instance = None

    def __init__(self):
        """Initialize middleware components - now using unified implementation."""
        self.middleware = UnifiedVectorMiddleware()

    @classmethod
    def _get_instance(cls):
        """Get or create module-level instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # Instance methods
    def error_handler_decorator(self, f):
        """Apply error handling to a function."""
        return self.middleware.error_handler(f)

    def json_required_decorator(self, f):
        """Apply JSON requirement to a function."""
        return self.middleware.json_required(f)

    def validate_request_decorator(self, validator_func):
        """Apply request validation to a function."""
        return self.middleware.validate_request(validator_func)

    def log_request_decorator(self, f):
        """Apply request logging to a function."""
        return self.middleware.log_request(f)

    def cors_headers_decorator(self, f):
        """Apply CORS headers to a function."""
        return self.middleware.add_cors_headers(f)

    def rate_limit_decorator(self, max_requests=100, window_seconds=60):
        """Apply rate limiting to a function."""
        return self.middleware.rate_limit(max_requests, window_seconds)

    def cache_response_decorator(self, ttl_seconds=300):
        """Apply response caching to a function."""
        return self.middleware.cache_response(ttl_seconds)

    def validate_pagination_decorator(self, f):
        """Apply pagination validation to a function."""
        return self.middleware.validate_pagination(f)

    # Class-level shortcuts for decorator usage in routes
    @classmethod
    def add_cors_headers(cls, f):
        """Class-level CORS decorator."""
        return cls._get_instance().cors_headers_decorator(f)

    @classmethod
    def error_handler(cls, f):
        """Class-level error handler decorator."""
        return cls._get_instance().error_handler_decorator(f)

    @classmethod
    def json_required(cls, f):
        """Class-level JSON required decorator."""
        return cls._get_instance().json_required_decorator(f)
