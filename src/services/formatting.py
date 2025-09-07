"""Formatting helpers for dashboard responses."""
from __future__ import annotations

from typing import Any, Dict
import time


def success(data: Any) -> Dict[str, Any]:
    """Format a successful response."""
    return {"status": "success", "data": data, "timestamp": time.time()}


def error(message: str) -> Dict[str, Any]:
    """Format an error response."""
    return {"status": "error", "message": message, "timestamp": time.time()}


def websocket_message(
    message_type: str, data: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    """Format a WebSocket message payload."""
    payload: Dict[str, Any] = {"type": message_type, "timestamp": time.time()}
    if data is not None:
        payload["data"] = data
    return payload
