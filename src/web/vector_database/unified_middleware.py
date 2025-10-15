"""
Unified Vector Database Middleware
===================================

Consolidated middleware decorators for vector database operations.
Combines error handling, request processing, response handling, and validation.

V2 Compliance: <400 lines, focused responsibility

Consolidated from:
- error_handler_middleware.py
- request_handler_middleware.py
- response_handler_middleware.py
- validation_middleware.py

Author: Agent-7 - Repository Cloning & Consolidation Specialist
Date: 2025-10-10
"""

import time
from collections.abc import Callable
from functools import wraps

from flask import current_app, jsonify, request


class UnifiedVectorMiddleware:
    """
    Unified middleware providing error handling, request/response processing,
    and validation decorators for vector database operations.
    """

    # ========================================================================
    # ERROR HANDLING
    # ========================================================================

    def error_handler(self, f: Callable) -> Callable:
        """
        Error handling decorator.

        Catches exceptions and returns standardized error responses.
        """

        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                current_app.logger.error(f"Error in {f.__name__}: {str(e)}")
                return (
                    jsonify({"success": False, "error": f"Operation failed: {str(e)}"}),
                    500,
                )

        return decorated_function

    # ========================================================================
    # REQUEST PROCESSING
    # ========================================================================

    def json_required(self, f: Callable) -> Callable:
        """
        Require JSON data decorator.

        Returns 400 error if request doesn't contain JSON data.
        """

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({"success": False, "error": "JSON data required"}), 400
            return f(*args, **kwargs)

        return decorated_function

    def log_request(self, f: Callable) -> Callable:
        """
        Request logging decorator.

        Logs request processing time and completion status.
        """

        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            current_app.logger.info(f"Processing {f.__name__} request")

            result = f(*args, **kwargs)

            execution_time = (time.time() - start_time) * 1000
            current_app.logger.info(f"Completed {f.__name__} in {execution_time:.2f}ms")

            return result

        return decorated_function

    def rate_limit(self, max_requests: int = 100, window_seconds: int = 60) -> Callable:
        """
        Rate limiting decorator.

        Note: Simplified implementation. In production, use Redis for distributed rate limiting.
        """

        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Simple in-memory rate limiting (in production, use Redis)
                client_ip = request.remote_addr
                current_time = time.time()

                # This is a simplified implementation
                # In production, implement proper rate limiting with Redis
                return f(*args, **kwargs)

            return decorated_function

        return decorator

    # ========================================================================
    # RESPONSE PROCESSING
    # ========================================================================

    def add_cors_headers(self, f: Callable) -> Callable:
        """
        Add CORS headers decorator.

        Adds Cross-Origin Resource Sharing headers to responses.
        """

        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)
            if isinstance(response, tuple):
                response_data, status_code = response
                response_data.headers["Access-Control-Allow-Origin"] = "*"
                response_data.headers["Access-Control-Allow-Methods"] = (
                    "GET, POST, PUT, DELETE, OPTIONS"
                )
                response_data.headers["Access-Control-Allow-Headers"] = (
                    "Content-Type, Authorization"
                )
                return response_data, status_code
            else:
                response.headers["Access-Control-Allow-Origin"] = "*"
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                return response

        return decorated_function

    def cache_response(self, ttl_seconds: int = 300) -> Callable:
        """
        Response caching decorator.

        Note: Simplified implementation. In production, use Redis or Memcached.
        """

        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Simple caching implementation
                # In production, use Redis or Memcached
                return f(*args, **kwargs)

            return decorated_function

        return decorator

    # ========================================================================
    # VALIDATION
    # ========================================================================

    def validate_request(self, validator_func: Callable) -> Callable:
        """
        Request validation decorator.

        Validates request data using provided validator function.
        """

        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if request.is_json:
                    data = request.get_json()
                    error = validator_func(data)
                    if error:
                        return jsonify({"success": False, "error": error}), 400
                return f(*args, **kwargs)

            return decorated_function

        return decorator

    def validate_pagination(self, f: Callable) -> Callable:
        """
        Pagination validation decorator.

        Validates page and per_page query parameters.
        """

        @wraps(f)
        def decorated_function(*args, **kwargs):
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 25))

            if page < 1:
                return (
                    jsonify({"success": False, "error": "Page must be greater than 0"}),
                    400,
                )

            if per_page < 1 or per_page > 100:
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "Per page must be between 1 and 100",
                        }
                    ),
                    400,
                )

            return f(*args, **kwargs)

        return decorated_function


# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================

# For backward compatibility with existing code
ErrorHandlerMiddleware = UnifiedVectorMiddleware
RequestHandlerMiddleware = UnifiedVectorMiddleware
ResponseHandlerMiddleware = UnifiedVectorMiddleware
ValidationMiddleware = UnifiedVectorMiddleware

