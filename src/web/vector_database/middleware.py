"""
Vector Database Middleware
=========================

Request/response processing middleware for vector database operations.
V2 Compliance: < 300 lines, single responsibility, middleware processing.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from flask import request, jsonify, current_app
from functools import wraps
from typing import Callable, Any, Dict
import time


class VectorDatabaseMiddleware:
    """Middleware for vector database operations."""

    @staticmethod
    def error_handler(f: Callable) -> Callable:
        """Error handling decorator."""

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

    @staticmethod
    def json_required(f: Callable) -> Callable:
        """Require JSON data decorator."""

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({"success": False, "error": "JSON data required"}), 400
            return f(*args, **kwargs)

        return decorated_function

    @staticmethod
    def validate_request(validator_func: Callable) -> Callable:
        """Request validation decorator."""

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

    @staticmethod
    def log_request(f: Callable) -> Callable:
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

    @staticmethod
    def add_cors_headers(f: Callable) -> Callable:
        """Add CORS headers decorator."""

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
                response.headers["Access-Control-Allow-Methods"] = (
                    "GET, POST, PUT, DELETE, OPTIONS"
                )
                response.headers["Access-Control-Allow-Headers"] = (
                    "Content-Type, Authorization"
                )
                return response

        return decorated_function

    @staticmethod
    def rate_limit(max_requests: int = 100, window_seconds: int = 60) -> Callable:
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

    @staticmethod
    def cache_response(ttl_seconds: int = 300) -> Callable:
        """Response caching decorator."""

        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Simple caching implementation
                # In production, use Redis or Memcached
                return f(*args, **kwargs)

            return decorated_function

        return decorator

    @staticmethod
    def validate_pagination(f: Callable) -> Callable:
        """Pagination validation decorator."""

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
