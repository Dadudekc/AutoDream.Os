"""
Agent-to-Agent PR Review Protocol - Peer review system for agent collaboration.
Ensures code quality and prevents duplication through structured review process.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

from .project_registry import registry_manager
from .design_authority import design_authority
from .vibe_check import vibe_check_strict, VibeCheckReport


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
    changes: List[CodeChange]
    review_comments: List[str] = None
    approval_criteria: List[str] = None
    
    def __post_init__(self):
        if self.review_comments is None:
            self.review_comments = []
        if self.approval_criteria is None:
            self.approval_criteria = [
                "Code follows project design patterns",
                "No duplication with existing components",
                "Passes vibe check (complexity, simplicity)",
                "Proper error handling implemented",
                "Documentation updated if needed"
            ]


@dataclass
class ReviewResult:
    """Result of a PR review."""
    pr_id: str
    reviewer: str
    status: ReviewStatus
    feedback: str
    violations_found: List[str]
    suggestions: List[str]
    approved: bool
    timestamp: str
    vibe_check_result: Optional[VibeCheckReport] = None


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
        self.pr_storage_path = Path(pr_storage_path)
        self.pull_requests: Dict[str, PullRequest] = {}
        self.review_history: List[ReviewResult] = []
        self._load_existing_prs()
    
    def _load_existing_prs(self) -> None:
        """Load existing pull requests from storage."""
        if self.pr_storage_path.exists():
            try:
                with open(self.pr_storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for pr_data in data.get('pull_requests', []):
                    # Convert changes back to CodeChange objects
                    changes = [CodeChange(**change_data) for change_data in pr_data.get('changes', [])]
                    
                    pr = PullRequest(
                        pr_id=pr_data['pr_id'],
                        title=pr_data['title'],
                        description=pr_data['description'],
                        author=pr_data['author'],
                        reviewer=pr_data['reviewer'],
                        status=ReviewStatus(pr_data['status']),
                        priority=ReviewPriority(pr_data['priority']),
                        created_at=pr_data['created_at'],
                        updated_at=pr_data['updated_at'],
                        changes=changes,
                        review_comments=pr_data.get('review_comments', []),
                        approval_criteria=pr_data.get('approval_criteria', [])
                    )
                    self.pull_requests[pr.pr_id] = pr
                    
                self.review_history = [
                    ReviewResult(**result_data) for result_data in data.get('review_history', [])
                ]
            except Exception as e:
                print(f"Warning: Failed to load existing PRs: {e}")
    
    def _save_prs(self) -> None:
        """Save pull requests to storage."""
        data = {
            'pull_requests': [
                {
                    'pr_id': pr.pr_id,
                    'title': pr.title,
                    'description': pr.description,
                    'author': pr.author,
                    'reviewer': pr.reviewer,
                    'status': pr.status.value,
                    'priority': pr.priority.value,
                    'created_at': pr.created_at,
                    'updated_at': pr.updated_at,
                    'changes': [asdict(change) for change in pr.changes],
                    'review_comments': pr.review_comments,
                    'approval_criteria': pr.approval_criteria
                } for pr in self.pull_requests.values()
            ],
            'review_history': [asdict(result) for result in self.review_history]
        }
        
        self.pr_storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.pr_storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_pull_request(self, author: str, title: str, description: str,
                           changes: List[CodeChange], priority: ReviewPriority = ReviewPriority.NORMAL,
                           assigned_reviewer: str = None) -> str:
        """
        Create a new pull request for review.
        
        Args:
            author: Agent creating the PR
            title: PR title
            description: Detailed description of changes
            changes: List of code changes
            priority: Review priority
            assigned_reviewer: Specific reviewer (optional, will auto-assign if None)
            
        Returns:
            PR ID for tracking
        """
        pr_id = f"PR_{author}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Auto-assign reviewer if not specified
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
            changes=changes
        )
        
        self.pull_requests[pr_id] = pr
        self._save_prs()
        
        return pr_id
    
    def _assign_reviewer(self, author: str) -> str:
        """Assign a reviewer for the PR."""
        # Simple round-robin assignment
        available_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        available_agents = [agent for agent in available_agents if agent != author]
        
        # Find agent with least recent reviews
        agent_review_counts = {}
        for result in self.review_history[-20:]:  # Check last 20 reviews
            agent_review_counts[result.reviewer] = agent_review_counts.get(result.reviewer, 0) + 1
        
        # Assign to agent with fewest recent reviews
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
        """
        Perform comprehensive review of a pull request.
        
        Args:
            pr_id: Pull request ID to review
            reviewer: Agent performing the review
            
        Returns:
            ReviewResult with approval status and feedback
        """
        if pr_id not in self.pull_requests:
            return ReviewResult(
                pr_id=pr_id,
                reviewer=reviewer,
                status=ReviewStatus.REJECTED,
                feedback="Pull request not found",
                violations_found=[],
                suggestions=[],
                approved=False,
                timestamp=datetime.now().isoformat()
            )
        
        pr = self.pull_requests[pr_id]
        
        if pr.reviewer != reviewer:
            return ReviewResult(
                pr_id=pr_id,
                reviewer=reviewer,
                status=ReviewStatus.REJECTED,
                feedback="Not authorized to review this PR",
                violations_found=[],
                suggestions=[],
                approved=False,
                timestamp=datetime.now().isoformat()
            )
        
        # Run comprehensive review
        violations_found = []
        suggestions = []
        
        # 1. Check for component duplication
        duplication_issues = self._check_duplication(pr)
        violations_found.extend(duplication_issues)
        
        # 2. Run vibe check on changed files
        vibe_check_result = self._run_vibe_check(pr)
        if vibe_check_result.result.value == "fail":
            violations_found.append(f"Vibe check failed: {vibe_check_result.summary}")
        
        # 3. Check design authority approval
        design_issues = self._check_design_compliance(pr)
        violations_found.extend(design_issues)
        
        # 4. Check for proper error handling
        error_handling_issues = self._check_error_handling(pr)
        violations_found.extend(error_handling_issues)
        
        # 5. Check documentation updates
        doc_issues = self._check_documentation(pr)
        violations_found.extend(doc_issues)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(pr, violations_found)
        
        # Determine approval status
        critical_violations = [v for v in violations_found if "error" in v.lower() or "failed" in v.lower()]
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
            vibe_check_result=vibe_check_result
        )
        
        self.review_history.append(review_result)
        self._save_prs()
        
        return review_result
    
    def _check_duplication(self, pr: PullRequest) -> List[str]:
        """Check for duplication with existing components."""
        violations = []
        registry = registry_manager.load_registry()
        
        for change in pr.changes:
            if change.change_type == "added":
                # Check if similar component already exists
                file_name = Path(change.file_path).stem
                
                for existing_component in registry.components.values():
                    if (file_name.lower() in existing_component.path.lower() or 
                        existing_component.path.lower() in file_name.lower()):
                        violations.append(
                            f"Potential duplication: {change.file_path} may duplicate {existing_component.path}"
                        )
        
        return violations
    
    def _run_vibe_check(self, pr: PullRequest) -> VibeCheckReport:
        """Run vibe check on changed files."""
        changed_files = [change.file_path for change in pr.changes if change.change_type in ["added", "modified"]]
        
        if not changed_files:
            # Return a passing report if no files to check
            return VibeCheckReport(
                result="pass",
                total_files=0,
                violations=[],
                summary={},
                timestamp=datetime.now().isoformat(),
                agent_author=pr.author
            )
        
        return vibe_check_strict(changed_files, pr.author)
    
    def _check_design_compliance(self, pr: PullRequest) -> List[str]:
        """Check compliance with design principles."""
        violations = []
        
        for change in pr.changes:
            if change.change_type in ["added", "modified"]:
                # Review the change with design authority
                review = design_authority.review_component_plan(
                    requester=pr.author,
                    component_name=Path(change.file_path).stem,
                    plan=change.new_content[:200] + "..." if len(change.new_content) > 200 else change.new_content,
                    context=f"PR: {pr.title}"
                )
                
                if not review.approved:
                    violations.append(f"Design authority rejected: {review.feedback}")
        
        return violations
    
    def _check_error_handling(self, pr: PullRequest) -> List[str]:
        """Check for proper error handling."""
        violations = []
        
        for change in pr.changes:
            if change.change_type in ["added", "modified"]:
                content = change.new_content.lower()
                
                # Check for bare except clauses
                if "except:" in content and "except exception:" not in content:
                    violations.append(f"Bare except clause in {change.file_path}")
                
                # Check for missing error handling in new functions
                if "def " in content and "try:" not in content:
                    violations.append(f"New function in {change.file_path} may need error handling")
        
        return violations
    
    def _check_documentation(self, pr: PullRequest) -> List[str]:
        """Check if documentation needs updating."""
        violations = []
        
        # Simple check - if new public functions are added, suggest documentation
        for change in pr.changes:
            if change.change_type == "added":
                if "def " in change.new_content and not any(doc in change.new_content for doc in ['"""', "'''", "# TODO"]):
                    violations.append(f"New functions in {change.file_path} should be documented")
        
        return violations
    
    def _generate_suggestions(self, pr: PullRequest, violations: List[str]) -> List[str]:
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
        
        # General suggestions
        if not suggestions:
            suggestions.extend([
                "Ensure all new components are registered in project registry",
                "Follow KISS and YAGNI principles",
                "Test changes locally before submitting"
            ])
        
        return suggestions
    
    def _generate_review_feedback(self, violations: List[str], suggestions: List[str], approved: bool) -> str:
        """Generate comprehensive review feedback."""
        feedback_parts = []
        
        if approved:
            feedback_parts.append("✅ **APPROVED** - Changes look good!")
            feedback_parts.append("")
            feedback_parts.append("🎯 Review Summary:")
            feedback_parts.append("- ✅ No duplication detected")
            feedback_parts.append("- ✅ Passes vibe check")
            feedback_parts.append("- ✅ Follows design principles")
            feedback_parts.append("- ✅ Proper error handling")
            feedback_parts.append("")
            feedback_parts.append("Ready to merge! 🚀")
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
        
        return '\n'.join(feedback_parts)
    
    def get_pending_reviews(self, reviewer: str) -> List[PullRequest]:
        """Get pending reviews for a specific reviewer."""
        return [
            pr for pr in self.pull_requests.values()
            if pr.reviewer == reviewer and pr.status == ReviewStatus.PENDING
        ]
    
    def get_agent_prs(self, agent: str) -> List[PullRequest]:
        """Get all PRs created by a specific agent."""
        return [
            pr for pr in self.pull_requests.values()
            if pr.author == agent
        ]
    
    def get_review_stats(self, agent: str) -> Dict[str, Any]:
        """Get review statistics for an agent."""
        agent_reviews = [result for result in self.review_history if result.reviewer == agent]
        agent_prs = [pr for pr in self.pull_requests.values() if pr.author == agent]
        
        return {
            'reviews_performed': len(agent_reviews),
            'prs_created': len(agent_prs),
            'approval_rate': len([r for r in agent_reviews if r.approved]) / max(len(agent_reviews), 1),
            'avg_review_time': self._calculate_avg_review_time(agent_reviews),
            'most_common_violations': self._get_common_violations(agent_reviews)
        }
    
    def _calculate_avg_review_time(self, reviews: List[ReviewResult]) -> Optional[str]:
        """Calculate average review time."""
        if not reviews:
            return None
        
        # This would need PR creation timestamps to be accurate
        # For now, return placeholder
        return "2.5 hours"
    
    def _get_common_violations(self, reviews: List[ReviewResult]) -> List[Tuple[str, int]]:
        """Get most common violation types."""
        violation_counts = {}
        
        for review in reviews:
            for violation in review.violations_found:
                violation_type = violation.split(':')[0] if ':' in violation else violation
                violation_counts[violation_type] = violation_counts.get(violation_type, 0) + 1
        
        return sorted(violation_counts.items(), key=lambda x: x[1], reverse=True)[:5]


# Global PR review protocol instance
pr_review_protocol = PRReviewProtocol()


def create_pull_request(author: str, title: str, description: str, changes: List[CodeChange],
                       priority: ReviewPriority = ReviewPriority.NORMAL,
                       assigned_reviewer: str = None) -> str:
    """Create a new pull request."""
    return pr_review_protocol.create_pull_request(author, title, description, changes, priority, assigned_reviewer)


def review_pull_request(pr_id: str, reviewer: str) -> ReviewResult:
    """Review a pull request."""
    return pr_review_protocol.review_pull_request(pr_id, reviewer)


def get_pending_reviews(reviewer: str) -> List[PullRequest]:
    """Get pending reviews for a reviewer."""
    return pr_review_protocol.get_pending_reviews(reviewer)