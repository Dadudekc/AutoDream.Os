"""
Coordinator Status Parser - V2 Compliance Module
================================================

Parses coordinator status information following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from typing import Any

from .coordinator_interfaces import ICoordinatorStatusParser


class CoordinatorStatusParser(ICoordinatorStatusParser):
    """Parses coordinator status information."""

    def parse_status(self, coordinator: Any) -> dict[str, Any]:
        """Parse status from coordinator."""
        try:
            if hasattr(coordinator, "get_status"):
                status = coordinator.get_status()
                if hasattr(status, "to_dict"):
                    return status.to_dict()
                elif isinstance(status, dict):
                    return status
                else:
                    return {"status": status}
            else:
                return {
                    "name": getattr(coordinator, "name", "unknown"),
                    "status": "unknown",
                    "error": "No get_status method available",
                }
        except Exception as e:
            return {
                "name": getattr(coordinator, "name", "unknown"),
                "status": "error",
                "error": str(e)
            }

    def can_parse_status(self, coordinator: Any) -> bool:
        """Check if coordinator status can be parsed."""
        return hasattr(coordinator, "get_status")


class CoordinatorStatusFilter:
    """Filters coordinators by status."""

    def __init__(self, status_parser: ICoordinatorStatusParser):
        """Initialize with status parser."""
        self.status_parser = status_parser

    def get_coordinators_by_status(
        self,
        coordinators: dict[str, Any],
        status: str
    ) -> dict[str, Any]:
        """Get coordinators filtered by status."""
        filtered = {}

        for name, coordinator in coordinators.items():
            try:
                status_info = self.status_parser.parse_status(coordinator)
                if self._matches_status(status_info, status):
                    filtered[name] = coordinator
            except Exception:
                continue

        return filtered

    def _matches_status(self, status_info: dict[str, Any], target_status: str) -> bool:
        """Check if status info matches target status."""
        # Check coordination_status field
        if "coordination_status" in status_info:
            coord_status = status_info["coordination_status"]
            if hasattr(coord_status, "value"):
                return coord_status.value == target_status
            elif isinstance(coord_status, str):
                return coord_status == target_status

        # Check direct status field
        if "status" in status_info:
            return status_info["status"] == target_status

        return False
