"""Response formatting helpers for the portal API."""

from __future__ import annotations

from typing import Any, Tuple
from flask import jsonify


def json_response(data: Any, status: int = 200) -> Tuple[Any, int]:
    """Return a JSON response with status code."""
    return jsonify(data), status


def error_response(message: str, status: int = 400) -> Tuple[Any, int]:
    """Return a standardized error response."""
    return jsonify({"error": message}), status
