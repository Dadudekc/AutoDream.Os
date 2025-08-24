"""Simple dependency management utilities."""
from __future__ import annotations

import importlib
from typing import Dict, Iterable


class DependencyManager:
    """Check for required Python modules."""

    @staticmethod
    def check_dependency(module_name: str) -> bool:
        """Return True if ``module_name`` can be imported."""
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False

    def ensure(self, modules: Iterable[str]) -> Dict[str, bool]:
        """Check multiple ``modules`` and return their availability."""
        return {m: self.check_dependency(m) for m in modules}
