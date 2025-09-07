"""Lightweight repository manager composing discovery, scanning and reporting."""

from __future__ import annotations

from typing import Dict, Any, List

from .repo import discovery, scanner, reporting


class RepositoryManager:
    """Coordinate repository discovery, scanning and reporting."""

    def __init__(self) -> None:
        self.repositories: List[str] = []
        self.scan_results: Dict[str, Dict[str, Any]] = {}

    def discover(self, root: str) -> List[str]:
        """Discover repositories under *root*."""
        self.repositories = discovery.discover_repositories(root)
        return self.repositories

    def scan(self) -> Dict[str, Dict[str, Any]]:
        """Scan all discovered repositories."""
        self.scan_results = {
            path: scanner.scan_repository(path) for path in self.repositories
        }
        return self.scan_results

    def report(self) -> Dict[str, Any]:
        """Generate a summary report from the scan results."""
        return reporting.generate_report(self.scan_results)
