"""Persistence utilities for report data."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol


class ReportStorageBackend(Protocol):
    """Protocol describing storage backends for reports."""

    def save_reports(self, reports: List[Dict[str, Any]]) -> None:
        """Persist a list of report dictionaries."""

    def load_reports(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retrieve report history."""


class InMemoryReportStorage:
    """Simple in-memory storage backend for reports."""

    def __init__(self) -> None:
        self._history: List[Dict[str, Any]] = []

    def save_reports(
        self, reports: List[Dict[str, Any]]
    ) -> None:  # pragma: no cover - trivial
        self._history.extend(reports)

    def load_reports(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if limit is None:
            return list(self._history)
        return self._history[-limit:]


def save_report_history(
    storage: ReportStorageBackend,
    report_history: List[Dict[str, Any]],
    reports_generated: int,
    last_report_time: Optional[str],
) -> None:
    """Persist report history using the configured storage backend."""
    payload = {
        "reports": list(report_history),
        "metadata": {
            "reports_generated": reports_generated,
            "last_report_time": last_report_time,
        },
    }
    storage.save_reports([payload])


def load_report_history(
    storage: ReportStorageBackend, limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Load report history from backend."""
    return storage.load_reports(limit)


__all__ = [
    "ReportStorageBackend",
    "InMemoryReportStorage",
    "save_report_history",
    "load_report_history",
]
