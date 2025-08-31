"""Common AI/ML utilities leveraging centralized implementations."""

from typing import Any, Dict
from src.utils.string_utils import generate_hash, format_response


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration - single implementation"""
    required_keys = ["name", "version", "status"]
    return all(key in config for key in required_keys)
