"""Orchestrator for workspace maintenance tasks."""

from pathlib import Path
from typing import Any, Dict

from .scanner import WorkspaceScanner
from .health_checker import WorkspaceHealthChecker
from .remediator import WorkspaceRemediator


class WorkspaceMaintenanceOrchestrator:
    """Coordinate workspace scanning, health checks and remediation."""

    def __init__(self, workspace_path: Path) -> None:
        self.workspace_path = Path(workspace_path)
        self.scanner = WorkspaceScanner(self.workspace_path)
        self.health_checker = WorkspaceHealthChecker()
        self.remediator = WorkspaceRemediator()

    def run(self) -> Dict[str, Any]:
        """Execute a full maintenance cycle and return a report."""
        files = self.scanner.scan()
        health = self.health_checker.check(files)
        remediation_actions = self.remediator.remediate(files)
        return {
            "files_scanned": len(files),
            "health": health,
            "remediation": remediation_actions,
        }
