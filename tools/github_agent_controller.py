#!/usr/bin/env python3
"""
GitHub Agent Controller - Full GitHub Operations Tool
====================================================

Comprehensive GitHub control tool enabling agents to fully operate and control
GitHub repositories, issues, pull requests, and all GitHub operations.

V2 Compliance: ≤400 lines, comprehensive GitHub automation
Author: Agent-1 (Architecture Foundation Specialist)
"""

import logging
import os
from dataclasses import dataclass
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


@dataclass
class GitHubRepository:
    """GitHub repository data model."""

    name: str
    full_name: str
    description: str
    private: bool
    html_url: str
    clone_url: str
    default_branch: str
    created_at: str
    updated_at: str
    language: str | None = None
    stars: int = 0
    forks: int = 0
    open_issues: int = 0


@dataclass
class GitHubIssue:
    """GitHub issue data model."""

    number: int
    title: str
    body: str
    state: str
    labels: list[str]
    assignees: list[str]
    created_at: str
    updated_at: str
    html_url: str
    user: str


@dataclass
class GitHubPullRequest:
    """GitHub pull request data model."""

    number: int
    title: str
    body: str
    state: str
    head_branch: str
    base_branch: str
    created_at: str
    updated_at: str
    html_url: str
    user: str
    mergeable: bool = False


class GitHubAgentController:
    """
    Comprehensive GitHub control tool for agent operations.

    Provides full CRUD operations for:
    - Repository management
    - Issue tracking
    - Pull request management
    - Branch operations
    - File operations
    - Webhook management
    """

    def __init__(self, token: str, base_url: str = "https://api.github.com"):
        """Initialize GitHub controller."""
        self.token = token
        self.base_url = base_url
        self.session = self._create_session()
        self.logger = logging.getLogger(f"{__name__}.GitHubAgentController")

        # Validate token
        if not self._validate_token():
            raise ValueError("Invalid GitHub token")

    def _create_session(self) -> requests.Session:
        """Create configured requests session."""
        session = requests.Session()

        # Set up authentication
        session.auth = HTTPBasicAuth(self.token, "")
        session.headers.update(
            {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Agent-Cellphone-V2-GitHub-Controller",
            }
        )

        # Set up retry strategy
        retry_strategy = Retry(
            total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _validate_token(self) -> bool:
        """Validate GitHub token."""
        try:
            response = self.session.get(f"{self.base_url}/user")
            return response.status_code == 200
        except Exception:
            return False

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make authenticated GitHub API request."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"GitHub API request failed: {e}")
            raise

    # Repository Operations
    def _create_repository_from_data(self, repo_data: dict[str, Any]) -> GitHubRepository:
        """Create GitHubRepository from API data."""
        return GitHubRepository(
            name=repo_data["name"],
            full_name=repo_data["full_name"],
            description=repo_data["description"] or "",
            private=repo_data["private"],
            html_url=repo_data["html_url"],
            clone_url=repo_data["clone_url"],
            default_branch=repo_data["default_branch"],
            created_at=repo_data["created_at"],
            updated_at=repo_data["updated_at"],
            language=repo_data.get("language"),
            stars=repo_data["stargazers_count"],
            forks=repo_data["forks_count"],
            open_issues=repo_data["open_issues_count"],
        )

    def create_repository(
        self, name: str, description: str = "", private: bool = False, auto_init: bool = True
    ) -> GitHubRepository:
        """Create a new GitHub repository."""
        data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init,
        }
        response = self._make_request("POST", "/user/repos", json=data)
        return self._create_repository_from_data(response.json())

    def get_repository(self, owner: str, repo: str) -> GitHubRepository:
        """Get repository information."""
        response = self._make_request("GET", f"/repos/{owner}/{repo}")
        return self._create_repository_from_data(response.json())

    def list_repositories(self, owner: str = None) -> list[GitHubRepository]:
        """List repositories."""
        endpoint = f"/users/{owner}/repos" if owner else "/user/repos"
        response = self._make_request("GET", endpoint)
        return [self._create_repository_from_data(repo_data) for repo_data in response.json()]

    # Issue Operations
    def _create_issue_from_data(self, issue_data: dict[str, Any]) -> GitHubIssue:
        """Create GitHubIssue from API data."""
        return GitHubIssue(
            number=issue_data["number"],
            title=issue_data["title"],
            body=issue_data["body"] or "",
            state=issue_data["state"],
            labels=[label["name"] for label in issue_data["labels"]],
            assignees=[assignee["login"] for assignee in issue_data["assignees"]],
            created_at=issue_data["created_at"],
            updated_at=issue_data["updated_at"],
            html_url=issue_data["html_url"],
            user=issue_data["user"]["login"],
        )

    def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str = "",
        labels: list[str] = None,
        assignees: list[str] = None,
    ) -> GitHubIssue:
        """Create a new GitHub issue."""
        data = {"title": title, "body": body, "labels": labels or [], "assignees": assignees or []}
        response = self._make_request("POST", f"/repos/{owner}/{repo}/issues", json=data)
        return self._create_issue_from_data(response.json())

    def get_issue(self, owner: str, repo: str, issue_number: int) -> GitHubIssue:
        """Get issue information."""
        response = self._make_request("GET", f"/repos/{owner}/{repo}/issues/{issue_number}")
        return self._create_issue_from_data(response.json())

    def list_issues(self, owner: str, repo: str, state: str = "open") -> list[GitHubIssue]:
        """List repository issues."""
        params = {"state": state}
        response = self._make_request("GET", f"/repos/{owner}/{repo}/issues", params=params)
        return [self._create_issue_from_data(issue_data) for issue_data in response.json()]

    # Pull Request Operations
    def create_pull_request(
        self, owner: str, repo: str, title: str, head_branch: str, base_branch: str, body: str = ""
    ) -> GitHubPullRequest:
        """Create a new pull request."""
        data = {"title": title, "head": head_branch, "base": base_branch, "body": body}
        response = self._make_request("POST", f"/repos/{owner}/{repo}/pulls", json=data)
        pr_data = response.json()

        return GitHubPullRequest(
            number=pr_data["number"],
            title=pr_data["title"],
            body=pr_data["body"] or "",
            state=pr_data["state"],
            head_branch=pr_data["head"]["ref"],
            base_branch=pr_data["base"]["ref"],
            created_at=pr_data["created_at"],
            updated_at=pr_data["updated_at"],
            html_url=pr_data["html_url"],
            user=pr_data["user"]["login"],
            mergeable=pr_data.get("mergeable", False),
        )

    def merge_pull_request(
        self, owner: str, repo: str, pr_number: int, merge_method: str = "merge"
    ) -> bool:
        """Merge a pull request."""
        try:
            data = {"merge_method": merge_method}
            response = self._make_request(
                "PUT", f"/repos/{owner}/{repo}/pulls/{pr_number}/merge", json=data
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    # File Operations
    def _file_operation(
        self, owner: str, repo: str, path: str, method: str, data: dict[str, Any]
    ) -> bool:
        """Generic file operation handler."""
        try:
            self._make_request(method, f"/repos/{owner}/{repo}/contents/{path}", json=data)
            return True
        except requests.exceptions.RequestException:
            return False

    def create_file(
        self, owner: str, repo: str, path: str, content: str, message: str, branch: str = None
    ) -> bool:
        """Create a new file in repository."""
        data = {
            "message": message,
            "content": content.encode("utf-8").decode("base64"),
            "branch": branch,
        }
        return self._file_operation(owner, repo, path, "PUT", data)

    def update_file(
        self,
        owner: str,
        repo: str,
        path: str,
        content: str,
        message: str,
        sha: str,
        branch: str = None,
    ) -> bool:
        """Update an existing file."""
        data = {
            "message": message,
            "content": content.encode("utf-8").decode("base64"),
            "sha": sha,
            "branch": branch,
        }
        return self._file_operation(owner, repo, path, "PUT", data)

    def delete_file(
        self, owner: str, repo: str, path: str, message: str, sha: str, branch: str = None
    ) -> bool:
        """Delete a file from repository."""
        data = {"message": message, "sha": sha, "branch": branch}
        return self._file_operation(owner, repo, path, "DELETE", data)

    # Branch Operations
    def create_branch(
        self, owner: str, repo: str, branch_name: str, from_branch: str = "main"
    ) -> bool:
        """Create a new branch."""
        try:
            ref_response = self._make_request(
                "GET", f"/repos/{owner}/{repo}/git/refs/heads/{from_branch}"
            )
            sha = ref_response.json()["object"]["sha"]
            data = {"ref": f"refs/heads/{branch_name}", "sha": sha}
            self._make_request("POST", f"/repos/{owner}/{repo}/git/refs", json=data)
            return True
        except requests.exceptions.RequestException:
            return False

    def delete_branch(self, owner: str, repo: str, branch_name: str) -> bool:
        """Delete a branch."""
        try:
            self._make_request("DELETE", f"/repos/{owner}/{repo}/git/refs/heads/{branch_name}")
            return True
        except requests.exceptions.RequestException:
            return False

    # Utility Methods
    def get_user_info(self) -> dict[str, Any]:
        """Get authenticated user information."""
        response = self._make_request("GET", "/user")
        return response.json()

    def search_repositories(self, query: str, sort: str = "stars") -> list[GitHubRepository]:
        """Search repositories."""
        params = {"q": query, "sort": sort}
        response = self._make_request("GET", "/search/repositories", params=params)
        return [
            self._create_repository_from_data(repo_data) for repo_data in response.json()["items"]
        ]


def create_github_controller(token: str) -> GitHubAgentController:
    """Create GitHub controller instance."""
    return GitHubAgentController(token)


if __name__ == "__main__":
    # Example usage
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        exit(1)

    controller = create_github_controller(token)

    # Test basic functionality
    try:
        user_info = controller.get_user_info()
        print(f"✅ Connected as: {user_info['login']}")

        repos = controller.list_repositories()
        print(f"📁 Found {len(repos)} repositories")

    except Exception as e:
        print(f"❌ Error: {e}")
