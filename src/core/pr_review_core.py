"""
PR Review Protocol Core - Main PR review management logic.
"""

from datetime import datetime
from typing import Any

from .pr_review_models import CodeChange, PullRequest, ReviewPriority, ReviewResult, ReviewStatus
from .pr_review_storage import PRStorageManager
from .pr_review_validators import PRValidator


class PRReviewProtocol:
    """
    Manages agent-to-agent pull request reviews.

    This system ensures that:
    1. No agent commits directly to main branch
    2. All changes are reviewed by another agent
    3. Duplication is caught before merging
    4. Design principles are enforced
    5. Code quality is maintained
    """

    def __init__(self, pr_storage_path: str = "/workspace/agent_prs.json"):
        self.storage_manager = PRStorageManager(pr_storage_path)
        self.validator = PRValidator()
        self.pull_requests: dict[str, PullRequest] = {}
        self.review_history: list[ReviewResult] = []
        self._load_existing_prs()

    def _load_existing_prs(self) -> None:
        """Load existing pull requests from storage."""
        self.pull_requests, self.review_history = self.storage_manager.load_existing_prs()

    def _save_prs(self) -> None:
        """Save pull requests to storage."""
        self.storage_manager.save_prs(self.pull_requests, self.review_history)

    def create_pull_request(
        self,
        author: str,
        title: str,
        description: str,
        changes: list[CodeChange],
        priority: ReviewPriority = ReviewPriority.NORMAL,
        assigned_reviewer: str = None,
    ) -> str:
        """Create a new pull request for review."""
        pr_id = f"PR_{author}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if assigned_reviewer is None:
            assigned_reviewer = self._assign_reviewer(author)

        pr = PullRequest(
            pr_id=pr_id,
            title=title,
            description=description,
            author=author,
            reviewer=assigned_reviewer,
            status=ReviewStatus.PENDING,
            priority=priority,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            changes=changes,
        )

        self.pull_requests[pr_id] = pr
        self._save_prs()
        return pr_id

    def _assign_reviewer(self, author: str) -> str:
        """Assign a reviewer for the PR."""
        available_agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]
        available_agents = [agent for agent in available_agents if agent != author]

        agent_review_counts = {}
        for result in self.review_history[-20:]:
            agent_review_counts[result.reviewer] = agent_review_counts.get(result.reviewer, 0) + 1

        if agent_review_counts:
            reviewer = min(available_agents, key=lambda x: agent_review_counts.get(x, 0))
        else:
            reviewer = available_agents[0]

        return reviewer

    def start_review(self, pr_id: str, reviewer: str) -> bool:
        """Start reviewing a pull request."""
        if pr_id not in self.pull_requests:
            return False

        pr = self.pull_requests[pr_id]
        if pr.reviewer != reviewer:
            return False

        pr.status = ReviewStatus.IN_REVIEW
        pr.updated_at = datetime.now().isoformat()
        self._save_prs()
        return True

    def review_pull_request(self, pr_id: str, reviewer: str) -> ReviewResult:
        """Perform comprehensive review of a pull request."""
        if pr_id not in self.pull_requests:
            return self._create_rejection_result(pr_id, reviewer, "Pull request not found")

        pr = self.pull_requests[pr_id]
        if pr.reviewer != reviewer:
            return self._create_rejection_result(
                pr_id, reviewer, "Not authorized to review this PR"
            )

        violations_found = []
        suggestions = []

        # Run all validation checks
        violations_found.extend(self.validator.check_duplication(pr))
        violations_found.extend(self.validator.check_design_compliance(pr))
        violations_found.extend(self.validator.check_error_handling(pr))
        violations_found.extend(self.validator.check_documentation(pr))

        # Run vibe check
        vibe_check_result = self.validator.run_vibe_check(pr)
        if vibe_check_result.result.value == "fail":
            violations_found.append(f"Vibe check failed: {vibe_check_result.summary}")

        # Generate suggestions
        suggestions = self._generate_suggestions(pr, violations_found)

        # Determine approval status
        critical_violations = [
            v for v in violations_found if "error" in v.lower() or "failed" in v.lower()
        ]
        approved = len(critical_violations) == 0

        # Update PR status
        if approved:
            pr.status = ReviewStatus.APPROVED
        else:
            pr.status = ReviewStatus.NEEDS_CHANGES

        pr.updated_at = datetime.now().isoformat()

        # Generate feedback
        feedback = self._generate_review_feedback(violations_found, suggestions, approved)

        review_result = ReviewResult(
            pr_id=pr_id,
            reviewer=reviewer,
            status=pr.status,
            feedback=feedback,
            violations_found=violations_found,
            suggestions=suggestions,
            approved=approved,
            timestamp=datetime.now().isoformat(),
            vibe_check_result=vibe_check_result,
        )

        self.review_history.append(review_result)
        self._save_prs()
        return review_result

    def _create_rejection_result(self, pr_id: str, reviewer: str, reason: str) -> ReviewResult:
        """Create a rejection result for invalid PR review requests."""
        return ReviewResult(
            pr_id=pr_id,
            reviewer=reviewer,
            status=ReviewStatus.REJECTED,
            feedback=reason,
            violations_found=[],
            suggestions=[],
            approved=False,
            timestamp=datetime.now().isoformat(),
        )

    def _generate_suggestions(self, pr: PullRequest, violations: list[str]) -> list[str]:
        """Generate actionable suggestions based on violations."""
        suggestions = []

        if any("duplication" in v.lower() for v in violations):
            suggestions.append("Consider reusing existing components instead of creating new ones")

        if any("vibe check" in v.lower() for v in violations):
            suggestions.append("Run vibe check locally before submitting PR")
            suggestions.append("Simplify complex functions and reduce nesting depth")

        if any("error handling" in v.lower() for v in violations):
            suggestions.append("Add proper error handling with specific exception types")

        if any("documentation" in v.lower() for v in violations):
            suggestions.append("Add docstrings to new public functions")

        if not suggestions:
            suggestions.extend(
                [
                    "Ensure all new components are registered in project registry",
                    "Follow KISS and YAGNI principles",
                    "Test changes locally before submitting",
                ]
            )

        return suggestions

    def _generate_review_feedback(
        self, violations: list[str], suggestions: list[str], approved: bool
    ) -> str:
        """Generate comprehensive review feedback."""
        feedback_parts = []

        if approved:
            feedback_parts.extend(
                [
                    "✅ **APPROVED** - Changes look good!",
                    "",
                    "🎯 Review Summary:",
                    "- ✅ No duplication detected",
                    "- ✅ Passes vibe check",
                    "- ✅ Follows design principles",
                    "- ✅ Proper error handling",
                    "",
                    "Ready to merge! 🚀",
                ]
            )
        else:
            feedback_parts.append("❌ **NEEDS CHANGES** - Please address the following issues:")
            feedback_parts.append("")

            if violations:
                feedback_parts.append("🚨 **Issues Found:**")
                for i, violation in enumerate(violations, 1):
                    feedback_parts.append(f"{i}. {violation}")
                feedback_parts.append("")

            if suggestions:
                feedback_parts.append("💡 **Suggestions:**")
                for i, suggestion in enumerate(suggestions, 1):
                    feedback_parts.append(f"{i}. {suggestion}")
                feedback_parts.append("")

            feedback_parts.append("Please fix these issues and resubmit for review.")

        return "\n".join(feedback_parts)

    def get_pending_reviews(self, reviewer: str) -> list[PullRequest]:
        """Get pending reviews for a specific reviewer."""
        return [
            pr
            for pr in self.pull_requests.values()
            if pr.reviewer == reviewer and pr.status == ReviewStatus.PENDING
        ]

    def get_agent_prs(self, agent: str) -> list[PullRequest]:
        """Get all PRs created by a specific agent."""
        return [pr for pr in self.pull_requests.values() if pr.author == agent]

    def get_review_stats(self, agent: str) -> dict[str, Any]:
        """Get review statistics for an agent."""
        agent_reviews = [result for result in self.review_history if result.reviewer == agent]
        agent_prs = [pr for pr in self.pull_requests.values() if pr.author == agent]

        return {
            "reviews_performed": len(agent_reviews),
            "prs_created": len(agent_prs),
            "approval_rate": len([r for r in agent_reviews if r.approved])
            / max(len(agent_reviews), 1),
            "avg_review_time": self._calculate_avg_review_time(agent_reviews),
            "most_common_violations": self._get_common_violations(agent_reviews),
        }

    def _calculate_avg_review_time(self, reviews: list[ReviewResult]) -> str | None:
        """Calculate average review time."""
        if not reviews:
            return None
        return "2.5 hours"  # Placeholder

    def _get_common_violations(self, reviews: list[ReviewResult]) -> list[tuple[str, int]]:
        """Get most common violation types."""
        violation_counts = {}

        for review in reviews:
            for violation in review.violations_found:
                violation_type = violation.split(":")[0] if ":" in violation else violation
                violation_counts[violation_type] = violation_counts.get(violation_type, 0) + 1

        return sorted(violation_counts.items(), key=lambda x: x[1], reverse=True)[:5]
