"""Data models and enums for contract management system."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


class TaskStatus(Enum):
    """Possible states for a contract task."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW_NEEDED = "REVIEW_NEEDED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BOUNCED_BACK = "BOUNCED_BACK"


class ValidationLevel(Enum):
    """Levels of validation strictness."""

    BASIC = "BASIC"
    STANDARD = "STANDARD"
    STRICT = "STRICT"


@dataclass
class ContractRequirement:
    """Individual contract requirement entry."""

    requirement_id: str
    description: str
    required: bool
    completed: bool = False
    validation_notes: str = ""
    completion_timestamp: Optional[str] = None


@dataclass
class ContractValidation:
    """Results of contract validation."""

    is_valid: bool
    missing_requirements: List[str]
    validation_errors: List[str]
    warnings: List[str]
    score: float
    timestamp: str


@dataclass
class ContractStatus:
    """Status tracking information for a contract."""

    contract_id: str
    agent_id: str
    current_status: TaskStatus
    progress_percentage: float
    last_updated: str
    requirements_completed: int
    total_requirements: int
    validation_result: Optional[ContractValidation] = None

    def update_timestamp(self) -> None:
        """Update the last_updated field to current time."""
        self.last_updated = datetime.now().isoformat()
