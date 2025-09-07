"""
Shared Utilities Package
========================

Contains utilities shared across all layers of the architecture.
These should be framework-agnostic and domain-agnostic.
"""

from .result import (
    Result, Success, Failure,
    success, failure, try_catch
)

__all__ = [
    "Result", "Success", "Failure",
    "success", "failure", "try_catch"
]
