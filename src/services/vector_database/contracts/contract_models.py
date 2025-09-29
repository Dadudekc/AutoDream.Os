#!/usr/bin/env python3
"""
Contract Models
===============

Data models and enums for V3 contract system.
V2 Compliance: ≤100 lines, focused responsibility, KISS principle.
"""

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class ContractPriority(Enum):
    """Contract priority enumeration - KISS principle compliant."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ContractStatus(Enum):
    """Contract status enumeration - simplified design."""

    AVAILABLE = "available"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class V3Contract:
    """V3 contract structure - simplified design."""

    contract_id: str
    title: str
    description: str
    priority: ContractPriority
    cycles_required: int
    status: ContractStatus
    assigned_agent: str | None
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "contract_id": self.contract_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "cycles_required": self.cycles_required,
            "status": self.status.value,
            "assigned_agent": self.assigned_agent,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


def create_default_contracts() -> list:
    """Create default V3 contracts."""

    return [
        V3Contract(
            contract_id="V3-003",
            title="Database Architecture Setup",
            description="Set up comprehensive database architecture with V3 compliance",
            priority=ContractPriority.HIGH,
            cycles_required=1,
            status=ContractStatus.AVAILABLE,
            assigned_agent=None,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        ),
        V3Contract(
            contract_id="V3-006",
            title="Performance Analytics Dashboard",
            description="Create performance analytics dashboard with real-time monitoring",
            priority=ContractPriority.MEDIUM,
            cycles_required=1,
            status=ContractStatus.AVAILABLE,
            assigned_agent=None,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        ),
        V3Contract(
            contract_id="V3-009",
            title="Natural Language Processing System",
            description="Implement NLP system for vector database operations",
            priority=ContractPriority.MEDIUM,
            cycles_required=1,
            status=ContractStatus.AVAILABLE,
            assigned_agent=None,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        ),
        V3Contract(
            contract_id="V3-012",
            title="Mobile Application Development",
            description="Develop mobile application for vector database access",
            priority=ContractPriority.MEDIUM,
            cycles_required=1,
            status=ContractStatus.AVAILABLE,
            assigned_agent=None,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        ),
    ]
