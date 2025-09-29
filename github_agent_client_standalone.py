"""
GitHub Agent Client - Standalone Version
========================================

Simple GitHub API client for agents to access GitHub repositories and data.
Provides authentication and basic GitHub operations.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


@dataclass
class GitHubConfig:
    """GitHub configuration data."""

    username: str
    token: str
    setup_date: str
    wizard_version: str


@dataclass
class GitHubRepository:
    """GitHub repository information."""

    name: str
    full_name: str
    description: str | None
    url: str
    clone_url: str
    language: str | None
    stars: int
    forks: int
    size: int
    updated_at: str
    private: bool


class GitHubAgentClient:
    """GitHub API client for agents."""

    def __init__(self, config_path: str = None):
        """Initialize GitHub client with configuration."""
        self.base_url = "https://api.github.com"
        self.config = self._load_config(config_path)
        self.headers = {
            "Authorization": f"token {self.config.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Agent-Cellphone-V2",
        }

    def _load_config(self, config_path: str = None) -> GitHubConfig:
        """Load GitHub configuration from file."""
        if config_path is None:
            # Try default locations
            default_paths = [
                "D:/projectscanner/config/github_config.json",
                "config/github_config.json",
                "github_config.json",
            ]

            for path in default_paths:
                if Path(path).exists():
                    config_path = path
                    break

        if not config_path or not Path(config_path).exists():
            raise FileNotFoundError("GitHub configuration file not found")

        with open(config_path) as f:
            config_data = json.load(f)

        return GitHubConfig(
            username=config_data["username"],
            token=config_data["token"],
            setup_date=config_data["setup_date"],
            wizard_version=config_data["wizard_version"],
        )

    def test_connection(self) -> dict[str, Any]:
        """Test GitHub API connection."""
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers, timeout=10)

            if response.status_code == 200:
                user_data = response.json()
                return {
                    "status": "success",
                    "authenticated": True,
                    "username": user_data.get("login"),
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                    "public_repos": user_data.get("public_repos"),
                    "private_repos": user_data.get("total_private_repos"),
                }
            else:
                return {
                    "status": "error",
                    "authenticated": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                }
        except Exception as e:
            return {"status": "error", "authenticated": False, "error": str(e)}

    def get_repositories(self, username: str = None, per_page: int = 30) -> list[GitHubRepository]:
        """Get repositories for a user."""
        if username is None:
            username = self.config.username

        try:
            response = requests.get(
                f"{self.base_url}/users/{username}/repos",
                headers=self.headers,
                params={"per_page": per_page, "sort": "updated"},
                timeout=10,
            )

            if response.status_code == 200:
                repos_data = response.json()
                repositories = []

                for repo in repos_data:
                    repositories.append(
                        GitHubRepository(
                            name=repo["name"],
                            full_name=repo["full_name"],
                            description=repo.get("description"),
                            url=repo["html_url"],
                            clone_url=repo["clone_url"],
                            language=repo.get("language"),
                            stars=repo["stargazers_count"],
                            forks=repo["forks_count"],
                            size=repo["size"],
                            updated_at=repo["updated_at"],
                            private=repo["private"],
                        )
                    )

                return repositories
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            raise Exception(f"Failed to get repositories: {str(e)}")

    def get_repository_info(self, owner: str, repo: str) -> dict[str, Any]:
        """Get detailed information about a specific repository."""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}", headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            raise Exception(f"Failed to get repository info: {str(e)}")

    def get_repository_contents(
        self, owner: str, repo: str, path: str = ""
    ) -> list[dict[str, Any]]:
        """Get contents of a repository directory."""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}/contents/{path}",
                headers=self.headers,
                timeout=10,
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            raise Exception(f"Failed to get repository contents: {str(e)}")

    def get_file_content(self, owner: str, repo: str, path: str) -> str:
        """Get content of a specific file."""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}/contents/{path}",
                headers=self.headers,
                timeout=10,
            )

            if response.status_code == 200:
                file_data = response.json()
                if file_data.get("type") == "file":
                    import base64

                    content = base64.b64decode(file_data["content"]).decode("utf-8")
                    return content
                else:
                    raise Exception("Path is not a file")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            raise Exception(f"Failed to get file content: {str(e)}")

    def search_repositories(self, query: str, per_page: int = 30) -> list[GitHubRepository]:
        """Search for repositories."""
        try:
            response = requests.get(
                f"{self.base_url}/search/repositories",
                headers=self.headers,
                params={"q": query, "per_page": per_page, "sort": "updated"},
                timeout=10,
            )

            if response.status_code == 200:
                search_data = response.json()
                repositories = []

                for repo in search_data["items"]:
                    repositories.append(
                        GitHubRepository(
                            name=repo["name"],
                            full_name=repo["full_name"],
                            description=repo.get("description"),
                            url=repo["html_url"],
                            clone_url=repo["clone_url"],
                            language=repo.get("language"),
                            stars=repo["stargazers_count"],
                            forks=repo["forks_count"],
                            size=repo["size"],
                            updated_at=repo["updated_at"],
                            private=repo["private"],
                        )
                    )

                return repositories
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            raise Exception(f"Failed to search repositories: {str(e)}")

    def get_user_info(self, username: str = None) -> dict[str, Any]:
        """Get user information."""
        if username is None:
            username = self.config.username

        try:
            response = requests.get(
                f"{self.base_url}/users/{username}", headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            raise Exception(f"Failed to get user info: {str(e)}")

    def get_rate_limit(self) -> dict[str, Any]:
        """Get API rate limit information."""
        try:
            response = requests.get(f"{self.base_url}/rate_limit", headers=self.headers, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            raise Exception(f"Failed to get rate limit: {str(e)}")


def main():
    """CLI interface for GitHub Agent Client."""
    import argparse

    parser = argparse.ArgumentParser(description="GitHub Agent Client")
    parser.add_argument("--config", help="Path to GitHub config file")
    parser.add_argument("--test", action="store_true", help="Test connection")
    parser.add_argument("--repos", help="Get repositories for username")
    parser.add_argument("--user", help="Get user info")
    parser.add_argument("--search", help="Search repositories")
    parser.add_argument("--rate-limit", action="store_true", help="Check rate limit")

    args = parser.parse_args()

    try:
        client = GitHubAgentClient(args.config)

        if args.test:
            result = client.test_connection()
            print(json.dumps(result, indent=2))

        elif args.repos:
            repos = client.get_repositories(args.repos)
            print(f"Found {len(repos)} repositories:")
            for repo in repos[:10]:  # Show first 10
                print(f"  {repo.full_name} - {repo.stars} stars - {repo.language or 'No language'}")

        elif args.user:
            user_info = client.get_user_info(args.user)
            print(f"User: {user_info['name']} (@{user_info['login']})")
            print(f"Public repos: {user_info['public_repos']}")
            print(f"Followers: {user_info['followers']}")

        elif args.search:
            repos = client.search_repositories(args.search)
            print(f"Found {len(repos)} repositories:")
            for repo in repos[:10]:  # Show first 10
                print(f"  {repo.full_name} - {repo.stars} stars")

        elif args.rate_limit:
            rate_limit = client.get_rate_limit()
            core = rate_limit["rate"]
            print(f"Rate limit: {core['remaining']}/{core['limit']} requests")
            print(f"Resets at: {core['reset']}")

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
