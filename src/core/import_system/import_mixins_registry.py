"""
Import System Mixins - Registry Methods
=======================================

Registry methods mixin for unified import system.
Extracted from unified_import_system.py to reduce complexity.

V2 Compliance: Mixin pattern for modularity
SOLID Principles: Single Responsibility, Delegation

Author: Agent-2 (Architecture & Design Specialist) - ROI 10.75 Task
Created: 2025-10-13
License: MIT
"""

from __future__ import annotations


class ImportRegistryMixin:
    """Mixin providing import registry methods via delegation.

    Provides import caching, history tracking, and pattern management.
    """

    def __init__(self):
        """Initialize import registry mixin."""
        from .import_registry import ImportRegistry

        if not hasattr(self, "_registry"):
            self._registry = ImportRegistry()

    def register_import(self, name: str, value) -> None:
        """Register an import in the cache."""
        self._registry.register_import(name, value)

    def get_import(self, name: str):
        """Get an import from the cache."""
        return self._registry.get_import(name)

    def has_import(self, name: str) -> bool:
        """Check if an import is cached."""
        return self._registry.has_import(name)

    def remove_import(self, name: str) -> bool:
        """Remove an import from the cache."""
        return self._registry.remove_import(name)

    def clear_cache(self) -> None:
        """Clear the import cache."""
        self._registry.clear_cache()

    def get_cache_stats(self):
        """Get cache statistics."""
        return self._registry.get_cache_stats()

    def mark_failed_import(self, name: str) -> None:
        """Mark an import as failed."""
        self._registry.mark_failed_import(name)

    def is_failed_import(self, name: str) -> bool:
        """Check if an import has failed."""
        return self._registry.is_failed_import(name)

    def clear_failed_imports(self) -> None:
        """Clear failed imports list."""
        self._registry.clear_failed_imports()

    def get_import_history(self, limit: int = 100):
        """Get import history."""
        return self._registry.get_import_history(limit)

    def cleanup_old_imports(self, max_age_hours: int = 24) -> int:
        """Clean up old imports from cache."""
        return self._registry.cleanup_old_imports(max_age_hours)

    def get_import_patterns(self):
        """Get common import patterns."""
        return self._registry.get_import_patterns()

    def validate_import_pattern(self, pattern: str) -> bool:
        """Validate an import pattern."""
        return self._registry.validate_import_pattern(pattern)


__all__ = ["ImportRegistryMixin"]
