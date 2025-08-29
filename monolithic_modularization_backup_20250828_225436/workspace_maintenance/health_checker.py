"""Basic workspace health checks."""

from pathlib import Path
from typing import Any, Dict, Iterable


class WorkspaceHealthChecker:
    """Evaluate simple health metrics for a workspace."""

    def check(self, files: Iterable[Path]) -> Dict[str, Any]:
        """Return a health summary for the provided files."""
        file_count = len(list(files))
        status = "healthy" if file_count > 0 else "empty"
        return {"status": status, "file_count": file_count}
