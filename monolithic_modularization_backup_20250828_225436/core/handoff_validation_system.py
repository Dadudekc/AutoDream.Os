"""Backward compatible wrapper for the new handoff validation package."""
from .handoff_validation import HandoffValidationSystem, get_handoff_validation_system

__all__ = ["HandoffValidationSystem", "get_handoff_validation_system"]
