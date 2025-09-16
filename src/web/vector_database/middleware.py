import logging

logger = logging.getLogger(__name__)
"""
Vector Database Middleware
=========================

Request/response processing middleware for vector database operations.
V2 Compliance: < 300 lines, single responsibility, middleware processing.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring

REFACTORED: Split into focused middleware classes for V2 compliance
- ErrorHandlerMiddleware: Error handling decorators
- RequestHandlerMiddleware: Request processing decorators
- ResponseHandlerMiddleware: Response processing decorators
- ValidationMiddleware: Validation decorators
"""

from .error_handler_middleware import ErrorHandlerMiddleware
from .request_handler_middleware import RequestHandlerMiddleware
from .response_handler_middleware import ResponseHandlerMiddleware
from .validation_middleware import ValidationMiddleware


class VectorDatabaseMiddleware:
    """Main middleware orchestrator for vector database operations.

        V2 Compliance: < 100 lines, facade pattern, single responsibility.
        This class orchestrates all middleware components.

    EXAMPLE USAGE:
    ==============

    # Basic usage example
    from src.web.vector_database.middleware import Middleware

    # Initialize and use
    instance = Middleware()
    result = instance.execute()
    logger.info(f"Execution result: {result}")

    # Advanced configuration
    config = {
        "option1": "value1",
        "option2": True
    }

    instance = Middleware(config)
    advanced_result = instance.execute_advanced()
    logger.info(f"Advanced result: {advanced_result}")

    """

    def __init__(self):
        """Initialize middleware components."""
        self.error_handler = ErrorHandlerMiddleware()
        self.request_handler = RequestHandlerMiddleware()
        self.response_handler = ResponseHandlerMiddleware()
        self.validation = ValidationMiddleware()

    def error_handler_decorator(self, f):
        """Apply error handling to a function."""
        return self.error_handler.error_handler(f)

    def json_required_decorator(self, f):
        """Apply JSON requirement to a function."""
        return self.request_handler.json_required(f)

    def validate_request_decorator(self, validator_func):
        """Apply request validation to a function."""
        return self.validation.validate_request(validator_func)

    def log_request_decorator(self, f):
        """Apply request logging to a function."""
        return self.request_handler.log_request(f)

    def cors_headers_decorator(self, f):
        """Apply CORS headers to a function."""
        return self.response_handler.add_cors_headers(f)

    def rate_limit_decorator(self, max_requests=100, window_seconds=60):
        """Apply rate limiting to a function."""
        return self.request_handler.rate_limit(max_requests, window_seconds)

    def cache_response_decorator(self, ttl_seconds=300):
        """Apply response caching to a function."""
        return self.response_handler.cache_response(ttl_seconds)

    def validate_pagination_decorator(self, f):
        """Apply pagination validation to a function."""
        return self.validation.validate_pagination(f)
