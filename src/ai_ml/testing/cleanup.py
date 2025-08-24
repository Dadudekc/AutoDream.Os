import os
from typing import Iterable


class CleanupManager:
    """Remove generated test files and other artifacts."""

    def cleanup(self, paths: Iterable[str]) -> int:
        removed = 0
        for path in paths:
            try:
                os.remove(path)
                removed += 1
            except FileNotFoundError:
                continue
        return removed
