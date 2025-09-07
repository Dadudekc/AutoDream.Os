"""Preparation helpers for validation execution."""

from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


def prepare_validation_data(raw_data: Any) -> Dict[str, Any]:
    """Normalize raw input for the validation pipeline.

    Parameters
    ----------
    raw_data: Any
        Incoming data that should be validated.

    Returns
    -------
    Dict[str, Any]
        A dictionary ready for validation. Non-dict inputs yield an
        empty dictionary and trigger a warning.
    """
    if isinstance(raw_data, dict):
        return raw_data

    logger.warning("Validation data expected dict, got %s", type(raw_data).__name__)
    return {}
