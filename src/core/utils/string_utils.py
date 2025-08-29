"""String helper utilities for core components."""
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict


def generate_hash(data: Any, algorithm: str = "md5", encoding: str = "utf-8") -> str:
    """Generate a hash for arbitrary data using the specified algorithm."""
    try:
        if isinstance(data, (dict, list, tuple, set)):
            json_data = json.dumps(data, sort_keys=True, default=str)
        else:
            json_data = str(data)

        data_bytes = json_data.encode(encoding)
        algo = algorithm.lower()
        if algo == "md5":
            return hashlib.md5(data_bytes).hexdigest()
        if algo == "sha1":
            return hashlib.sha1(data_bytes).hexdigest()
        if algo == "sha256":
            return hashlib.sha256(data_bytes).hexdigest()
        if algo == "sha512":
            return hashlib.sha512(data_bytes).hexdigest()
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    except Exception:
        return ""


def get_current_timestamp() -> str:
    """Return the current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def format_response(data: Any, status: str = "success", message: str = "") -> Dict[str, Any]:
    """Format a standard response dictionary."""
    return {
        "status": status,
        "message": message,
        "data": data,
        "timestamp": get_current_timestamp(),
    }
