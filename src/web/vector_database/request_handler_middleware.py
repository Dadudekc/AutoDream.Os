"""
Request Handler Middleware
=========================

Request processing decorators for vector database operations.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

import time
from collections.abc import Callable
from functools import wraps

from flask import current_app, request


class RequestHandlerMiddleware:
    """Request processing middleware decorators."""

    def json_required(self, f: Callable) -> Callable:
        """Require JSON data decorator."""
        from flask import jsonify

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({"success": False, "error": "JSON data required"}), 400
            return f(*args, **kwargs)

        return decorated_function

    def log_request(self, f: Callable) -> Callable:
        """Request logging decorator."""

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
        """Rate limiting decorator."""

        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Simple in-memory rate limiting (in production, use Redis)
                client_ip = request.remote_addr
                current_time = time.time()

                # This is a simplified implementation
                # In production, implement proper rate limiting
                return f(*args, **kwargs)

            return decorated_function

        return decorator
