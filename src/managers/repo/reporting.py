"""Repository reporting helpers."""

from __future__ import annotations

from typing import Dict, Any


def generate_report(scans: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a simple summary report from *scans*.

    The report aggregates basic statistics across all scanned repositories.
    """
    total_repositories = len(scans)
    total_files = sum(data.get("file_count", 0) for data in scans.values())
    total_size = sum(data.get("total_size", 0) for data in scans.values())
    return {
        "total_repositories": total_repositories,
        "total_files": total_files,
        "total_size": total_size,
        "repositories": list(scans.values()),
    }
