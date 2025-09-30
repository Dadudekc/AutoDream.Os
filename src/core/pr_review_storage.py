"""
PR Review Protocol Storage - Handles persistence of PR data.
"""

import json
from dataclasses import asdict
from pathlib import Path

from .pr_review_models import CodeChange, PullRequest, ReviewPriority, ReviewResult, ReviewStatus


class PRStorageManager:
    """Manages storage and retrieval of PR data."""

    def __init__(self, pr_storage_path: str = "/workspace/agent_prs.json"):
        self.pr_storage_path = Path(pr_storage_path)

    def load_existing_prs(self) -> tuple[dict[str, PullRequest], list[ReviewResult]]:
        """Load existing pull requests from storage."""
        pull_requests = {}
        review_history = []

        if self.pr_storage_path.exists():
            try:
                with open(self.pr_storage_path, encoding="utf-8") as f:
                    data = json.load(f)

                for pr_data in data.get("pull_requests", []):
                    changes = [
                        CodeChange(**change_data) for change_data in pr_data.get("changes", [])
                    ]

                    pr = PullRequest(
                        pr_id=pr_data["pr_id"],
                        title=pr_data["title"],
                        description=pr_data["description"],
                        author=pr_data["author"],
                        reviewer=pr_data["reviewer"],
                        status=ReviewStatus(pr_data["status"]),
                        priority=ReviewPriority(pr_data["priority"]),
                        created_at=pr_data["created_at"],
                        updated_at=pr_data["updated_at"],
                        changes=changes,
                        review_comments=pr_data.get("review_comments", []),
                        approval_criteria=pr_data.get("approval_criteria", []),
                    )
                    pull_requests[pr.pr_id] = pr

                review_history = [
                    ReviewResult(**result_data) for result_data in data.get("review_history", [])
                ]
            except Exception as e:
                print(f"Warning: Failed to load existing PRs: {e}")

        return pull_requests, review_history

    def save_prs(
        self, pull_requests: dict[str, PullRequest], review_history: list[ReviewResult]
    ) -> None:
        """Save pull requests to storage."""
        data = {
            "pull_requests": [
                {
                    "pr_id": pr.pr_id,
                    "title": pr.title,
                    "description": pr.description,
                    "author": pr.author,
                    "reviewer": pr.reviewer,
                    "status": pr.status.value,
                    "priority": pr.priority.value,
                    "created_at": pr.created_at,
                    "updated_at": pr.updated_at,
                    "changes": [asdict(change) for change in pr.changes],
                    "review_comments": pr.review_comments,
                    "approval_criteria": pr.approval_criteria,
                }
                for pr in pull_requests.values()
            ],
            "review_history": [asdict(result) for result in review_history],
        }

        self.pr_storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.pr_storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
