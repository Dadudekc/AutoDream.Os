"""
Design Authority - V2 Compliant Main Interface
==============================================

Main interface for design authority functionality.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

from .design_authority_core import DesignAuthorityCore, DesignReview


class DesignAuthority:
    """Main design authority interface."""

    def __init__(self):
        """Initialize design authority."""
        self.core = DesignAuthorityCore()

    def review_component_plan(self, requester: str, component_name: str, plan: str) -> DesignReview:
        """Review component implementation plan."""
        return self.core.review_component_plan(requester, component_name, plan)

    def review_code_complexity(
        self, requester: str, component_name: str, code_snippet: str
    ) -> DesignReview:
        """Review code complexity."""
        return self.core.review_code_complexity(requester, component_name, code_snippet)

    def get_review_history(self) -> list[DesignReview]:
        """Get review history."""
        return self.core.get_review_history()

    def get_knowledge_base(self) -> dict:
        """Get design knowledge base."""
        return self.core.get_knowledge_base()


# Global instance for backward compatibility
design_authority = DesignAuthority()


def review_component_plan(requester: str, component_name: str, plan: str) -> DesignReview:
    """Review component implementation plan."""
    return design_authority.review_component_plan(requester, component_name, plan)


def review_code_complexity(requester: str, component_name: str, code_snippet: str) -> DesignReview:
    """Review code complexity."""
    return design_authority.review_code_complexity(requester, component_name, code_snippet)
