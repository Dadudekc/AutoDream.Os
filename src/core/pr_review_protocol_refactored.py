"""
Agent-to-Agent PR Review Protocol - Refactored main interface.
Ensures code quality and prevents duplication through structured review process.
"""

from .pr_review_core import PRReviewProtocol
from .pr_review_models import CodeChange, PullRequest, ReviewPriority, ReviewResult

# Global PR review protocol instance
pr_review_protocol = PRReviewProtocol()


def create_pull_request(
    author: str,
    title: str,
    description: str,
    changes: list[CodeChange],
    priority: ReviewPriority = ReviewPriority.NORMAL,
    assigned_reviewer: str = None,
) -> str:
    """Create a new pull request."""
    return pr_review_protocol.create_pull_request(
        author, title, description, changes, priority, assigned_reviewer
    )


def review_pull_request(pr_id: str, reviewer: str) -> ReviewResult:
    """Review a pull request."""
    return pr_review_protocol.review_pull_request(pr_id, reviewer)


def get_pending_reviews(reviewer: str) -> list[PullRequest]:
    """Get pending reviews for a reviewer."""
    return pr_review_protocol.get_pending_reviews(reviewer)


def get_agent_prs(agent: str) -> list[PullRequest]:
    """Get all PRs created by a specific agent."""
    return pr_review_protocol.get_agent_prs(agent)


def get_review_stats(agent: str) -> dict:
    """Get review statistics for an agent."""
    return pr_review_protocol.get_review_stats(agent)


def start_review(pr_id: str, reviewer: str) -> bool:
    """Start reviewing a pull request."""
    return pr_review_protocol.start_review(pr_id, reviewer)
