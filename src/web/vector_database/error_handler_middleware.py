"""
Error Handler Middleware
=======================

Error handling decorators for vector database operations.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

from collections.abc import Callable
from functools import wraps

from flask import current_app, jsonify


class ErrorHandlerMiddleware:
    """Error handling middleware decorators."""

    def error_handler(self, f: Callable) -> Callable:
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
