"""
Design Authority Core - V2 Compliant
====================================

Core design authority functionality.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from .design_authority_knowledge import get_design_knowledge_base


class DecisionSeverity(Enum):
    """Severity levels for design decisions."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class DesignReview:
    """Represents a design review decision."""

    request_id: str
    component_name: str
    decision: str
    severity: DecisionSeverity
    reasoning: str
    timestamp: datetime
    reviewer: str


class DesignAuthorityCore:
    """Core design authority functionality."""

    def __init__(self):
        """Initialize design authority core."""
        self.knowledge_base = get_design_knowledge_base()
        self.reviews = []

    def review_component_plan(self, requester: str, component_name: str, plan: str) -> DesignReview:
        """Review component implementation plan."""
        # Simplified review logic for V2 compliance
        if len(plan) > 1000:
            decision = "REJECT: Plan too complex"
            severity = DecisionSeverity.ERROR
            reasoning = "Plans should be concise and focused"
        elif "abstract" in plan.lower():
            decision = "WARN: Avoid abstractions"
            severity = DecisionSeverity.WARNING
            reasoning = "Prefer concrete implementations"
        else:
            decision = "APPROVE: Plan looks good"
            severity = DecisionSeverity.INFO
            reasoning = "Plan follows KISS principles"

        review = DesignReview(
            request_id=f"plan_{component_name}_{datetime.now().timestamp()}",
            component_name=component_name,
            decision=decision,
            severity=severity,
            reasoning=reasoning,
            timestamp=datetime.now(),
            reviewer="DesignAuthorityCore",
        )

        self.reviews.append(review)
        return review

    def review_code_complexity(
        self, requester: str, component_name: str, code_snippet: str
    ) -> DesignReview:
        """Review code complexity."""
        # Simplified complexity review for V2 compliance
        lines = len(code_snippet.split("\n"))

        if lines > 400:
            decision = "REJECT: File too large"
            severity = DecisionSeverity.ERROR
            reasoning = "Files must be ≤400 lines"
        elif lines > 200:
            decision = "WARN: Consider splitting"
            severity = DecisionSeverity.WARNING
            reasoning = "Large files should be modularized"
        else:
            decision = "APPROVE: Good size"
            severity = DecisionSeverity.INFO
            reasoning = "File size is appropriate"

        review = DesignReview(
            request_id=f"complexity_{component_name}_{datetime.now().timestamp()}",
            component_name=component_name,
            decision=decision,
            severity=severity,
            reasoning=reasoning,
            timestamp=datetime.now(),
            reviewer="DesignAuthorityCore",
        )

        self.reviews.append(review)
        return review

    def get_review_history(self) -> list[DesignReview]:
        """Get review history."""
        return self.reviews

    def get_knowledge_base(self) -> dict[str, Any]:
        """Get design knowledge base."""
        return self.knowledge_base


def review_component_plan(requester: str, component_name: str, plan: str) -> DesignReview:
    """Review component implementation plan."""
    authority = DesignAuthorityCore()
    return authority.review_component_plan(requester, component_name, plan)


def review_code_complexity(requester: str, component_name: str, code_snippet: str) -> DesignReview:
    """Review code complexity."""
    authority = DesignAuthorityCore()
    return authority.review_code_complexity(requester, component_name, code_snippet)

