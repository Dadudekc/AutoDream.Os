#!/usr/bin/env python3
"""
GitHub Repository Scanner - Team Delta Evaluation Tool
======================================================

Scans GitHub repositories to identify integration candidates for Team Delta.
Uses GitHub API to list repositories and analyze their characteristics.

Author: Agent-7 - Repository Cloning Specialist
License: MIT
"""

from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

# Add src to path if running as script
if __name__ == "__main__":
    src_path = Path(__file__).resolve().parents[2]
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

logger = logging.getLogger(__name__)


def get_setting(key: str, default: str | None = None) -> str | None:
    """Get setting from environment (inline for standalone use)."""
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    return os.getenv(key, default)


@dataclass
class RepositoryInfo:
    """Information about a GitHub repository."""

    name: str
    full_name: str
    description: str | None
    size_kb: int
    language: str | None
    stars: int
    forks: int
    open_issues: int
    last_updated: datetime
    url: str
    clone_url: str
    is_private: bool
    topics: list[str]


class GitHubScanner:
    """GitHub API client for repository scanning."""

    def __init__(self, token: str | None = None):
        """
        Initialize GitHub scanner.

        Args:
            token: GitHub personal access token (reads from .env if not provided)
        """
        # Load token from parameter or environment
        if token:
            self.token = token
        else:
            self.token = get_setting("GITHUB_TOKEN")

        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN in .env or pass as parameter")

        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def list_user_repositories(
        self, username: str | None = None, include_private: bool = True
    ) -> list[RepositoryInfo]:
        """
        List all repositories for authenticated user or specific username.

        Args:
            username: GitHub username (uses authenticated user if None)
            include_private: Include private repositories

        Returns:
            List of repository information objects
        """
        if username:
            url = f"{self.base_url}/users/{username}/repos"
        else:
            url = f"{self.base_url}/user/repos"

        params = {
            "per_page": 100,
            "sort": "updated",
            "direction": "desc",
        }

        if not include_private and username:
            params["type"] = "public"
        elif not username:
            params["type"] = "all"

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            repos = []
            for repo_data in response.json():
                repo_info = self._parse_repository(repo_data)
                repos.append(repo_info)

            logger.info(f"Found {len(repos)} repositories")
            return repos

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch repositories: {e}")
            raise

    def get_repository(self, owner: str, repo_name: str) -> RepositoryInfo:
        """
        Get detailed information about a specific repository.

        Args:
            owner: Repository owner username
            repo_name: Repository name

        Returns:
            Repository information object
        """
        url = f"{self.base_url}/repos/{owner}/{repo_name}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return self._parse_repository(response.json())

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch repository {owner}/{repo_name}: {e}")
            raise

    def get_repository_languages(self, owner: str, repo_name: str) -> dict[str, int]:
        """
        Get language breakdown for a repository.

        Args:
            owner: Repository owner username
            repo_name: Repository name

        Returns:
            Dictionary mapping language names to bytes of code
        """
        url = f"{self.base_url}/repos/{owner}/{repo_name}/languages"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch languages for {owner}/{repo_name}: {e}")
            return {}

    def _parse_repository(self, data: dict[str, Any]) -> RepositoryInfo:
        """
        Parse GitHub API repository response into RepositoryInfo.

        Args:
            data: Raw repository data from GitHub API

        Returns:
            Parsed repository information
        """
        updated_at = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))

        return RepositoryInfo(
            name=data["name"],
            full_name=data["full_name"],
            description=data.get("description"),
            size_kb=data["size"],
            language=data.get("language"),
            stars=data["stargazers_count"],
            forks=data["forks_count"],
            open_issues=data["open_issues_count"],
            last_updated=updated_at,
            url=data["html_url"],
            clone_url=data["clone_url"],
            is_private=data["private"],
            topics=data.get("topics", []),
        )

    def close(self) -> None:
        """Close the session."""
        self.session.close()

    def __enter__(self) -> GitHubScanner:
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()


def filter_integration_candidates(
    repos: list[RepositoryInfo],
    min_size_kb: int = 10,
    max_size_kb: int = 50000,
    exclude_names: list[str] | None = None,
    primary_language: str | None = None,
) -> list[RepositoryInfo]:
    """
    Filter repositories to identify integration candidates.

    Args:
        repos: List of repository information objects
        min_size_kb: Minimum repository size in KB
        max_size_kb: Maximum repository size in KB
        exclude_names: Repository names to exclude
        primary_language: Filter by primary language (e.g., "Python")

    Returns:
        Filtered list of candidate repositories
    """
    exclude_names = exclude_names or []
    candidates = []

    for repo in repos:
        # Skip excluded repositories
        if repo.name in exclude_names:
            continue

        # Size filter
        if not (min_size_kb <= repo.size_kb <= max_size_kb):
            continue

        # Language filter
        if primary_language and repo.language != primary_language:
            continue

        candidates.append(repo)

    return candidates


def print_repository_summary(repos: list[RepositoryInfo]) -> None:
    """
    Print formatted summary of repositories.

    Args:
        repos: List of repository information objects
    """
    print(f"\n{'='*80}")
    print(f"REPOSITORY SUMMARY ({len(repos)} repositories)")
    print(f"{'='*80}\n")

    for idx, repo in enumerate(repos, 1):
        print(f"{idx}. {repo.name}")
        print(f"   Description: {repo.description or 'No description'}")
        print(f"   Language: {repo.language or 'Unknown'}")
        print(f"   Size: {repo.size_kb:,} KB")
        print(f"   Stars: {repo.stars} | Forks: {repo.forks} | Issues: {repo.open_issues}")
        print(f"   Last Updated: {repo.last_updated.strftime('%Y-%m-%d')}")
        print(f"   URL: {repo.url}")
        print(f"   Private: {'Yes' if repo.is_private else 'No'}")
        if repo.topics:
            print(f"   Topics: {', '.join(repo.topics)}")
        print()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Example usage
    try:
        with GitHubScanner() as scanner:
            # List all repositories
            repos = scanner.list_user_repositories()

            # Filter for Python repositories (excluding known integrations)
            exclude_list = [
                "Agent_Cellphone_V2_Repository",
                "Chat_Mate",
                "Dream.OS",
                "DreamVault",
                "trading-platform",
                "Jarvis",
                "OSRS_Swarm_Agents",
            ]

            candidates = filter_integration_candidates(
                repos,
                min_size_kb=50,  # At least 50KB
                max_size_kb=20000,  # Max 20MB
                exclude_names=exclude_list,
                primary_language="Python",
            )

            # Print summary
            print_repository_summary(candidates)

            # Save to file for analysis
            print(f"Found {len(candidates)} integration candidates")
            print("Suitable for Team Delta evaluation (repos 9-12)")

    except Exception as e:
        logger.error(f"Error scanning repositories: {e}")
        raise
