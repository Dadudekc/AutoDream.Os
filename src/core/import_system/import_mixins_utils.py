"""
Import System Mixins - Utility Methods
======================================

Utility methods mixin for unified import system.
Extracted from unified_import_system.py to reduce complexity.

V2 Compliance: Mixin pattern for modularity
SOLID Principles: Single Responsibility, Delegation

Author: Agent-2 (Architecture & Design Specialist) - ROI 10.75 Task
Created: 2025-10-13
License: MIT
"""

from __future__ import annotations


class ImportUtilitiesMixin:
    """Mixin providing import utility methods via delegation.

    Provides module introspection, validation, and path resolution utilities.
    """

    def __init__(self):
        """Initialize import utilities mixin."""
        from .import_utilities import ImportUtilities

        if not hasattr(self, "_utilities"):
            self._utilities = ImportUtilities()

    def get_module_path(self, module_name: str):
        """Get the path to a module."""
        return self._utilities.get_module_path(module_name)

    def is_module_available(self, module_name: str) -> bool:
        """Check if a module is available."""
        return self._utilities.is_module_available(module_name)

    def get_import_path(self, module_name: str):
        """Get the import path for a module."""
        return self._utilities.get_import_path(module_name)

    def resolve_relative_import(self, base_module: str, relative_path: str) -> str:
        """Resolve a relative import path."""
        return self._utilities.resolve_relative_import(base_module, relative_path)

    def get_package_root(self, module_name: str):
        """Get the root package directory for a module."""
        return self._utilities.get_package_root(module_name)

    def list_module_contents(self, module_name: str):
        """List the contents of a module."""
        return self._utilities.list_module_contents(module_name)

    def get_module_docstring(self, module_name: str):
        """Get the docstring of a module."""
        return self._utilities.get_module_docstring(module_name)

    def validate_import_syntax(self, import_statement: str) -> bool:
        """Validate import statement syntax."""
        return self._utilities.validate_import_syntax(import_statement)

    def get_import_dependencies(self, module_name: str):
        """Get the dependencies of a module."""
        return self._utilities.get_import_dependencies(module_name)

    def create_import_alias(self, module_name: str, alias: str) -> str:
        """Create an import alias statement."""
        return self._utilities.create_import_alias(module_name, alias)

    def create_from_import(self, module_name: str, item: str, alias: str = None) -> str:
        """Create a from import statement."""
        return self._utilities.create_from_import(module_name, item, alias)


__all__ = ["ImportUtilitiesMixin"]
