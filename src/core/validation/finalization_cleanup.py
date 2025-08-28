"""Cleanup helpers for validation system finalization."""

from .validation_manager import ValidationManager


def cleanup_resources(validation_manager: ValidationManager) -> None:
    """Cleanup transient validation data."""
    validation_manager.validation_history.clear()
