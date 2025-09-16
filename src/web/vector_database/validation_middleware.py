import logging
logger = logging.getLogger(__name__)
"""
Validation Middleware
====================

Validation decorators for vector database operations.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

from collections.abc import Callable
from functools import wraps

from flask import jsonify, request


class ValidationMiddleware:
    """Validation middleware decorators."""

    def validate_request(self, validator_func: Callable) -> Callable:
        """Decorator to validate request data."""
        def wrapper(*args, **kwargs):
            # Validate request
            return validator_func(*args, **kwargs)
        return wrapper

# Initialize and use
instance = Validation_Middleware()
result = instance.execute()
logger.info(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Validation_Middleware(config)
advanced_result = instance.execute_advanced()
logger.info(f"Advanced result: {advanced_result}")

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

    def validate_pagination(self, f: Callable) -> Callable:
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
