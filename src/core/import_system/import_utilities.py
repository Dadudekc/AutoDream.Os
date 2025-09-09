"""
Import System Utilities - V2 Compliance Module
=============================================

Utility functions for unified import system.

V2 Compliance: < 300 lines, single responsibility, utility functions.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import sys
from pathlib import Path


class ImportUtilities:
    """Utility functions for import system."""

    def __init__(self):
        """Initialize import utilities."""
        self._cache = {}

    def get_module_path(self, module_name: str) -> str | None:
        """Get the path to a module."""
        try:
            module = sys.modules.get(module_name)
            if module and hasattr(module, "__file__"):
                return module.__file__
            return None
        except Exception:
            return None

    def is_module_available(self, module_name: str) -> bool:
        """Check if a module is available."""
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False

    def get_import_path(self, module_name: str) -> str | None:
        """Get the import path for a module."""
        if module_name in self._cache:
            return self._cache[module_name]

        try:
            module = __import__(module_name)
            path = getattr(module, "__file__", None)
            if path:
                self._cache[module_name] = path
            return path
        except ImportError:
            return None

    def resolve_relative_import(self, base_module: str, relative_path: str) -> str:
        """Resolve a relative import path."""
        try:
            base_path = Path(base_module).parent
            target_path = base_path / relative_path
            return str(target_path.resolve())
        except Exception:
            return relative_path

    def get_package_root(self, module_name: str) -> str | None:
        """Get the root package directory for a module."""
        try:
            module = __import__(module_name)
            if hasattr(module, "__file__"):
                path = Path(module.__file__)
                # Walk up to find __init__.py
                for parent in path.parents:
                    if (parent / "__init__.py").exists():
                        return str(parent)
            return None
        except Exception:
            return None

    def list_module_contents(self, module_name: str) -> list[str]:
        """List the contents of a module."""
        try:
            module = __import__(module_name)
            return [name for name in dir(module) if not name.startswith("_")]
        except ImportError:
            return []

    def get_module_docstring(self, module_name: str) -> str | None:
        """Get the docstring of a module."""
        try:
            module = __import__(module_name)
            return getattr(module, "__doc__", None)
        except ImportError:
            return None

    def validate_import_syntax(self, import_statement: str) -> bool:
        """Validate import statement syntax."""
        try:
            compile(import_statement, "<string>", "exec")
            return True
        except SyntaxError:
            return False

    def get_import_dependencies(self, module_name: str) -> list[str]:
        """Get the dependencies of a module."""
        try:
            module = __import__(module_name)
            if hasattr(module, "__file__"):
                # This is a simplified version - in practice, you'd parse the AST
                return []
            return []
        except ImportError:
            return []

    def create_import_alias(self, module_name: str, alias: str) -> str:
        """Create an import alias statement."""
        return f"import {module_name} as {alias}"

    def create_from_import(self, module_name: str, item: str, alias: str = None) -> str:
        """Create a from import statement."""
        if alias:
            return f"from {module_name} import {item} as {alias}"
        return f"from {module_name} import {item}"
