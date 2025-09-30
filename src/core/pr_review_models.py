"""
PR Review Protocol Models - Data structures for agent-to-agent PR reviews.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ReviewStatus(Enum):
    """Status of a PR review."""

    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_CHANGES = "needs_changes"


class ReviewPriority(Enum):
    """Priority level for reviews."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class CodeChange:
    """Represents a code change in a PR."""

    file_path: str
    change_type: str  # added, modified, deleted
    old_content: str = ""
    new_content: str = ""
    line_start: int = 0
    line_end: int = 0


@dataclass
class PullRequest:
    """Represents a pull request for agent review."""

    pr_id: str
    title: str
    description: str
    author: str
    reviewer: str
    status: ReviewStatus
    priority: ReviewPriority
    created_at: str
    updated_at: str
    changes: list[CodeChange]
    review_comments: list[str] = None
    approval_criteria: list[str] = None

    def __post_init__(self):
        if self.review_comments is None:
            self.review_comments = []
        if self.approval_criteria is None:
            self.approval_criteria = [
                "Code follows project design patterns",
                "No duplication with existing components",
                "Passes vibe check (complexity, simplicity)",
                "Proper error handling implemented",
                "Documentation updated if needed",
            ]


@dataclass
class ReviewResult:
    """Result of a PR review."""

    pr_id: str
    reviewer: str
    status: ReviewStatus
    feedback: str
    violations_found: list[str]
    suggestions: list[str]
    approved: bool
    timestamp: str
    vibe_check_result: Any = None  # VibeCheckReport | None
