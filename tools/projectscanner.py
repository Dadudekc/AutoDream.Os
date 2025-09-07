"""Minimal stub ProjectScanner for snapshot generation."""

from __future__ import annotations


class _DummyReport:
    def save_report(self) -> None:  # pragma: no cover - placeholder
        """Stubbed report generator."""


class ProjectScanner:
    """Stub implementation used for testing environments.

    The real ProjectScanner performs repository analysis and generates
    snapshot artifacts. This minimal version satisfies tooling contracts
    without external dependencies.
    """

    def __init__(self, project_root: str) -> None:  # pragma: no cover - trivial
        self.project_root = project_root
        self.report_generator = _DummyReport()

    def scan_project(self) -> None:  # pragma: no cover - placeholder
        """Scan project (no-op)."""

    def generate_init_files(self, overwrite: bool = False) -> None:  # pragma: no cover
        """Generate __init__ files (no-op)."""

    def categorize_agents(self) -> None:  # pragma: no cover - placeholder
        """Categorize agents (no-op)."""

    def export_chatgpt_context(self) -> None:  # pragma: no cover - placeholder
        """Export context (no-op)."""

