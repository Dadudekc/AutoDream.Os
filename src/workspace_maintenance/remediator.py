"""Workspace remediation actions."""

from typing import Iterable, List
from pathlib import Path


class WorkspaceRemediator:
    """Apply basic remediation to a workspace."""

    def remediate(self, files: Iterable[Path]) -> List[str]:
        """Return a list of remediation actions taken.

        This placeholder implementation simply reports the number of
        files provided. In a real system, this would attempt to fix issues
        detected by health checks.
        """
        count = len(list(files))
        if count == 0:
            return ["no_files_found"]
        return [f"checked_{count}_files"]
