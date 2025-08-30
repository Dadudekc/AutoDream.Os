#!/usr/bin/env python3
"""
Integrity Issues Data Models.

This module contains data structures for tracking and managing integrity issues:
- Issue categorization and severity levels
- Problem tracking and resolution status
- Issue metadata and timestamps
"""

from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class IssueSeverity(Enum):
    """Issue severity levels."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IssueStatus(Enum):
    """Issue resolution status."""

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    IGNORED = "IGNORED"


@dataclass
class IntegrityIssues:
    """Individual integrity issue tracking."""

    issue_id: str
    title: str
    description: str
    severity: IssueSeverity
    status: IssueStatus
    category: str
    affected_files: List[str]
    detected_at: str
    resolved_at: Optional[str] = None
    resolution_notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    @property
    def is_resolved(self) -> bool:
        """Check if issue is resolved."""
        return self.status in [IssueStatus.RESOLVED, IssueStatus.CLOSED]

    @property
    def is_critical(self) -> bool:
        """Check if issue is critical."""
        return self.severity == IssueSeverity.CRITICAL

    @property
    def age_hours(self) -> float:
        """Get issue age in hours."""
        detected_time = datetime.fromisoformat(self.detected_at)
        current_time = datetime.now()
        delta = current_time - detected_time
        return delta.total_seconds() / 3600

    def resolve(self, resolution_notes: str = None):
        """Mark issue as resolved."""
        self.status = IssueStatus.RESOLVED
        self.resolved_at = datetime.now().isoformat()
        if resolution_notes:
            self.resolution_notes = resolution_notes

    def close(self):
        """Close the issue."""
        if self.is_resolved:
            self.status = IssueStatus.CLOSED
        else:
            raise ValueError("Cannot close unresolved issue")

    def ignore(self, reason: str = None):
        """Mark issue as ignored."""
        self.status = IssueStatus.IGNORED
        if reason:
            self.resolution_notes = reason

    def update_status(self, new_status: IssueStatus, notes: str = None):
        """Update issue status."""
        self.status = new_status
        if notes:
            self.resolution_notes = notes

        if new_status == IssueStatus.RESOLVED:
            self.resolved_at = datetime.now().isoformat()
